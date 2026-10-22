#!/usr/bin/env python3
"""Build the love-mini games catalog: for every games/<id>/game.json that may be shared,
a zip laid out from the SD card's root, and manifest.json in the format of Mixtape's
catalogs (which Port Store reads from recipes/sources/), plus COMPATIBILITY.md.

    tools/build.py [--out dist] [--cache .cache] [--base URL] [id ...]

--base: the address the zips will be downloadable from (the release's, by its tag: the
manifest is read from the latest release, the zips it names stay where they are), as
written in manifest.json; by default the latest release of $GITHUB_REPOSITORY (or
l0st0npl4net/love-mini-games). With ids: only those games, their entries printed.

A game's zip holds:
    Roms/PORTS/Games/love-mini/games/<id>/game.love   (or its folder, "pack": "folder")
    Roms/PORTS/Games/love-mini/games/<id>/profile.lua (if the game has one)
    Roms/PORTS/Games/love-mini/games/<id>/LICENSE.txt
    Roms/PORTS/Shortcuts/LOVE games/<Name>.port       OnionOS's Ports entry
    Roms/PORTS/Imgs/<Name>.png                        its picture (games/<id>/cover.png)
Zips are made the same way every time (fixed dates, sorted), so a game's version, which
is its source commit and its zip's checksum, changes only when the game or its profile do.
Standard library only; git for the sources."""
import argparse
import hashlib
import io
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAMES = ROOT / "games"
RUNTIME = "love-mini"
DATE = (1980, 1, 1, 0, 0, 0)
SKIP_DIRS = {".git", ".github", ".vscode", ".idea"}
SKIP_EXT = (".dll", ".dylib", ".exe", ".zip", ".love", ".so")
LICENSES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "LICENCE.txt", "COPYING", "COPYING.txt")
# OnionOS's Ports entry: launch_standalone.sh runs love-mini's run.sh with the game's id
PORT = """#!/bin/sh
# {name} on love-mini (LÖVE 11.5 for the Miyoo Mini)
# Standalone Ports Script Template

GameName="{name}"
GameDir="love-mini"
GameExecutable="run.sh"
GameDataFile="run.sh"
KillAudioserver=0
PerformanceMode=0
Arguments="{id}"

/mnt/SDCARD/Emu/PORTS/launch_standalone.sh "$GameName" "$GameDir" "$GameExecutable" "$Arguments" "$GameDataFile" "$KillAudioserver" "$PerformanceMode"
"""
# A game the player owns: the entry checks their file in the game's own folder, and
# starts love-mini's run.sh from there.
PORT_OWNED = """#!/bin/sh
# {name} on love-mini (LÖVE 11.5 for the Miyoo Mini): the game is yours, see README.txt
# Standalone Ports Script Template

GameName="{name}"
GameDir="love-mini/games/{id}"
GameExecutable="../../run.sh"
GameDataFile="{data}"
KillAudioserver=0
PerformanceMode=0
Arguments="{id}"

/mnt/SDCARD/Emu/PORTS/launch_standalone.sh "$GameName" "$GameDir" "$GameExecutable" "$Arguments" "$GameDataFile" "$KillAudioserver" "$PerformanceMode"
"""
README_OWNED = """{name} on love-mini
{line}

The game is not included: it is yours. {what}:

  {hint}

Put it here, in Roms/PORTS/Games/love-mini/games/{id}/, keeping its name. Then start
{name} from Ports (or Games > MiyooPorts).
{store}
What is here (a love-mini profile and what it uses) only adjusts the game for the Mini, as
it loads: your file is never changed.
"""

GAME_FIELDS = {"id", "name", "love", "source", "owned", "wrapper", "license", "redistribute", "status", "categories",
               "controls", "tested", "notes", "skip", "pack", "porter", "attribution"}
OWNED_FIELDS = {"files", "what", "hint", "store", "search"}


def log(*a):
    print(*a, file=sys.stderr)


def load_games(ids):
    out = []
    for path in sorted(GAMES.glob("*/game.json")):
        g = json.loads(path.read_text(encoding="utf-8"))
        problems = check(g, path)
        if problems:
            raise SystemExit(f"{path}: " + "; ".join(problems))
        if ids and g["id"] not in ids:
            continue
        g["_dir"] = path.parent
        out.append(g)
    return out


def check(g, path):
    p = []
    if set(g) - GAME_FIELDS:
        p.append(f"unknown fields {sorted(set(g) - GAME_FIELDS)}")
    if g.get("id") != path.parent.name:
        p.append("`id` is the folder's name")
    for k in ("name", "license", "status"):
        if not isinstance(g.get(k), str) or not g[k]:
            p.append(f"`{k}` is text")
    if "owned" in g:
        o = g["owned"]
        if not (isinstance(o, dict) and not set(o) - OWNED_FIELDS and isinstance(o.get("files"), list) and o["files"]
                and all(isinstance(f, str) and f and "/" not in f for f in o["files"]) and isinstance(o.get("what"), str)):
            p.append("`owned` has `files` (the player's file names), `what`, and maybe `hint`, `store`")
        if "source" in g:
            p.append("a game the player owns has no `source`")
    else:
        src = g.get("source", {})
        if not (isinstance(src, dict) and isinstance(src.get("github"), str) and isinstance(src.get("commit"), str)
                and len(src["commit"]) == 40):
            p.append("`source` has `github` (owner/repo) and `commit` (a full hash)")
    if "wrapper" in g and not (path.parent / str(g["wrapper"])).is_dir():
        p.append("`wrapper`: a folder next to game.json")
    if not isinstance(g.get("redistribute"), bool):
        p.append("`redistribute` is true or false: may the game be shared from here (its license)")
    if g.get("pack", "love") not in ("love", "folder"):
        p.append("`pack` is love or folder")
    return p


def fetch(src, cache):
    """The source at its commit, in the cache (a shallow fetch of that commit)."""
    dest = cache / src["github"].replace("/", "__")
    if not (dest / ".git").is_dir():
        dest.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "-C", str(dest), "init", "-q"], check=True)
        subprocess.run(["git", "-C", str(dest), "remote", "add", "origin", f"https://github.com/{src['github']}"],
                       check=True)
    head = subprocess.run(["git", "-C", str(dest), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    if head != src["commit"]:
        subprocess.run(["git", "-C", str(dest), "fetch", "-q", "--depth", "1", "origin", src["commit"]], check=True)
        subprocess.run(["git", "-C", str(dest), "checkout", "-q", "--detach", "FETCH_HEAD"], check=True)
    return dest


def game_files(top, skip):
    """(path in the game, file) for what goes into its .love: no version control, no
    other systems' libraries, nothing the game.json skips."""
    skip = {s.strip("/") for s in skip}
    for base, dirs, names in os.walk(top):
        rel = os.path.relpath(base, top)
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS and os.path.normpath(os.path.join(rel, d)) not in skip)
        for n in sorted(names):
            r = os.path.normpath(os.path.join(rel, n))
            if n.lower().endswith(SKIP_EXT) or r in skip:
                continue
            yield r.replace(os.sep, "/"), Path(base) / n


def add(z, name, data, mode=0o644):
    info = zipfile.ZipInfo(name, DATE)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = (0o100000 | mode) << 16
    z.writestr(info, data, compresslevel=9)


def love_of(top, skip):
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for rel, f in game_files(top, skip):
            add(z, rel, f.read_bytes())
    return buf.getvalue()


def wrapper_members(g, base):
    w = g["_dir"] / g["wrapper"] if g.get("wrapper") else None
    if not w:
        return []
    return [(base + rel, f.read_bytes()) for rel, f in game_files(w, [])]


def build_owned(g, out):
    """A game the player owns: only what love-mini needs for it (its profile and what that
    uses, from the game's wrapper folder), an entry for Ports, a README."""
    o = g["owned"]
    base = f"Roms/PORTS/Games/{RUNTIME}/games/{g['id']}/"
    members = wrapper_members(g, base)
    profile = g["_dir"] / "profile.lua"
    if profile.is_file():
        members.append((base + "profile.lua", profile.read_bytes()))
    stem = o["files"][0].rsplit(".", 1)[0]
    data = f"{stem}.*" if all(f.rsplit(".", 1)[0] == stem for f in o["files"]) else o["files"][0]
    members.append((f"Roms/PORTS/Shortcuts/LOVE games/{g['name']}.port",
                    PORT_OWNED.format(name=g["name"], id=g["id"], data=data).encode()))
    readme = README_OWNED.format(name=g["name"], line="=" * (len(g["name"]) + 12), what=o["what"],
                                 hint=o.get("hint", ""), id=g["id"],
                                 store=f"\nTo buy it: {o['store']}\n" if o.get("store") else "")
    members.append((base + "README.txt", readme.encode()))
    cover = g["_dir"] / "cover.png"
    if cover.is_file():
        members.append((f"Roms/PORTS/Imgs/{g['name']}.png", cover.read_bytes()))
    return write_zip(out / f"{g['id']}.zip", members)


def write_zip(zpath, members):
    with zipfile.ZipFile(zpath, "w") as z:
        for name, data in sorted(members):
            add(z, name, data, 0o755 if name.endswith(".port") else 0o644)
    return zpath, hashlib.sha256(zpath.read_bytes()).hexdigest()


def build_game(g, cache, out):
    if "owned" in g:
        return build_owned(g, out)
    repo = fetch(g["source"], cache)
    top = repo / g["source"].get("dir", ".")
    if not (top / "main.lua").is_file():
        raise ValueError(f"no main.lua in {g['source'].get('dir', '.')}")
    base = f"Roms/PORTS/Games/{RUNTIME}/games/{g['id']}/"
    members = []
    if g.get("pack") == "folder":
        members += [(base + rel, f.read_bytes()) for rel, f in game_files(top, g.get("skip", []))]
    else:
        members.append((base + "game.love", love_of(top, g.get("skip", []))))
    profile = g["_dir"] / "profile.lua"
    if profile.is_file():
        # next to a .love: games/<id>/profile.lua; a folder may have one of its own
        where = base + "profile.lua" if g.get("pack") != "folder" else f"Roms/PORTS/Games/{RUNTIME}/profiles/{g['id']}.lua"
        members.append((where, profile.read_bytes()))
    lic = next((repo / n for n in LICENSES if (repo / n).is_file()), None)
    if lic is None:
        raise ValueError("the source has no license file")
    members.append((base + "LICENSE.txt", lic.read_bytes()))
    if g.get("attribution"):
        # credit the source does not give for what it uses (another's pictures)
        members.append((base + "ATTRIBUTION.txt", (g["attribution"] + "\n").encode()))
    for extra in ("LICENSE-MUSIC", "THIRD-PARTY-LICENSE.md"):
        if (repo / extra).is_file():
            members.append((base + extra, (repo / extra).read_bytes()))
    members.append((f"Roms/PORTS/Shortcuts/LOVE games/{g['name']}.port",
                    PORT.format(name=g["name"], id=g["id"]).encode()))
    cover = g["_dir"] / "cover.png"
    if cover.is_file():
        members.append((f"Roms/PORTS/Imgs/{g['name']}.png", cover.read_bytes()))
    members += wrapper_members(g, base)
    return write_zip(out / f"{g['id']}.zip", members)


def compatibility(games):
    lines = ["# Compatibility", "",
             "The games of this catalog on love-mini: under qemu (the Mini's build of love-mini, a test run",
             "of a few hundred frames) and on a Mini Plus (frame times from love-mini's log). Made by `tools/build.py`",
             "from `games/*/game.json`: change those, not this file.", "",
             "Shared: whether its license (code, pictures, sounds, fonts) lets this catalog share it; a",
             "game that is not is listed for its results only.", "",
             "| Game | Shared | qemu | Mini Plus | Controls | License | Notes |", "|---|---|---|---|---|---|---|"]
    for g in sorted(games, key=lambda g: g["name"].lower()):
        t = g.get("tested", {})
        link = g["owned"].get("store", "") if "owned" in g else f"https://github.com/{g['source']['github']}"
        lines.append(f"| [{g['name']}]({link}) | "
                     f"{'wrapper only (your copy)' if 'owned' in g else 'yes' if g['redistribute'] else 'no'} | {t.get('qemu', '—')} | "
                     f"{t.get('mini-plus', '—')} | {g.get('controls', '')} | {g['license']} | {g.get('notes', '')} |")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--out", default=str(ROOT / "dist"))
    ap.add_argument("--cache", default=str(ROOT / ".cache"))
    ap.add_argument("--base", default="")
    args = ap.parse_args()
    out, cache = Path(args.out), Path(args.cache)
    out.mkdir(parents=True, exist_ok=True)
    repo = os.environ.get("GITHUB_REPOSITORY", "l0st0npl4net/love-mini-games")
    base = args.base or f"https://github.com/{repo}/releases/latest/download"
    games = load_games(set(args.ids))
    ports, failed = [], []
    for g in games:
        if not g["redistribute"]:
            log(f"skip  {g['id']}: not to be shared from here")
            continue
        try:
            zpath, digest = build_game(g, cache, out)
        except Exception as e:  # noqa: BLE001  (one game's source down: the rest still build)
            failed.append(g["id"])
            log(f"FAIL  {g['id']}: {e}")
            continue
        version = f"own-{digest[:6]}" if "owned" in g else f"{g['source']['commit'][:7]}-{digest[:6]}"
        log(f"ok    {g['id']:14} {version} {zpath.stat().st_size >> 10} KB")
        entry = {
            "name": g["name"], "version": version, "url": f"{base}/{zpath.name}", "sha256": digest,
            "size": zpath.stat().st_size, "categories": g.get("categories", []), "status": g["status"],
            "assets": "owned" if "owned" in g else "free", "porter": g.get("porter", ["love-mini-games"]),
            "upstream": g["owned"].get("store", "") if "owned" in g else f"https://github.com/{g['source']['github']}",
            "notes": " ".join(x for x in (f"Controls: {g['controls']}." if g.get("controls") else "",
                                          f"License: {g['license']}.", g.get("notes", "")) if x),
            "requires": [RUNTIME],
        }
        if "owned" in g:
            o = g["owned"]
            entry["needs"] = [{"what": o["what"], "hint": o.get("hint", ""),
                               "check": [f"Roms/PORTS/Games/{RUNTIME}/games/{g['id']}/{f}" for f in o["files"]],
                               **({"search": o["search"]} if o.get("search") else {})}]
        if (g["_dir"] / "cover.png").is_file():
            entry["image"] = f"{base}/{g['id']}.png"
            (out / f"{g['id']}.png").write_bytes((g["_dir"] / "cover.png").read_bytes())
        ports.append(entry)
    manifest = {"name": "love-mini games", "ports": ports}
    text = json.dumps(manifest, indent=1, ensure_ascii=False) + "\n"
    if args.ids:
        # some games only: their entries said, the catalog's files left as they are
        print(text)
    else:
        (out / "manifest.json").write_text(text, encoding="utf-8")
        (ROOT / "COMPATIBILITY.md").write_text(compatibility(games), encoding="utf-8")
    log(f"{len(ports)} games, {len(failed)} failed: {out / 'manifest.json'}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
