#!/usr/bin/env python3
"""Check the catalog's games on love-mini without a Mini: each game that may be shared runs
for a few hundred frames under qemu-user, with its profile and a few presses of Start, A
and the d-pad, in love-mini's kit for PCs (love-mini-<version>-qemu.tar.gz of its releases).
The game is run as the catalog packs it (tools/build.py), unpacked as on the card. A game
passes when it runs all its frames without an error.

    tools/check.py --kit KIT [--out check] [--frames 360] [id ...]

KIT: the kit's love-mini folder (its run.sh). Writes check/<id>/ (frames, report.json,
log.txt), check/sheet.png (each game's last frame) and check/summary.md, also to the
GitHub job's summary. Needs qemu-arm and an armhf glibc (SYSROOT, see the kit's run.sh).
Standard library only; git for the sources."""
import argparse
import json
import os
import shutil
import subprocess
import sys
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build  # noqa: E402  (the games and their sources, as the catalog builds them)

# Start twice, A, right held, A held, up: past most title screens and into play
INPUT = "60 28 1\n64 28 0\n120 28 1\n124 28 0\n150 57 1\n154 57 0\n180 106 1\n240 106 0\n250 57 1\n280 57 0\n290 103 1\n300 103 0\n"


def run(g, kit, out, frames, cache, inp):
    # the game as the catalog packs it, unpacked as on the card
    dest = out / g["id"]
    card = out / ".card" / g["id"]
    shutil.rmtree(card, ignore_errors=True)
    card.mkdir(parents=True)
    try:
        zpath, _ = build.build_game(g, cache, card)
    except Exception as e:  # noqa: BLE001  (reported as the game's failure)
        return g, False, f"not built: {e}"
    with zipfile.ZipFile(zpath) as z:
        z.extractall(card)
    games = card / "Roms/PORTS/Games" / build.RUNTIME
    game = games / "games" / g["id"]
    env = dict(os.environ, LOVEMINI_EXIT_ON_ERROR="1", EVERY="60")
    if (game / "game.love").is_file():
        target, profile = game / "game.love", game / "profile.lua"
    else:
        target, profile = game, games / "profiles" / f"{g['id']}.lua"
    if profile.is_file():
        env["PROFILE"] = str(profile)
    try:
        code = subprocess.run([str(kit / "run.sh"), str(target), str(frames), str(dest), str(inp)], env=env,
                              timeout=1800, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
    except subprocess.TimeoutExpired:
        return g, False, "did not finish in 30 minutes"
    try:
        r = json.loads((dest / "report.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return g, False, f"no report (crashed? exit {code}), see its log.txt"
    if r["errors"]:
        return g, False, "error: " + r["errors"][0].splitlines()[0][:160]
    if r["frames"] < frames:
        return g, False, f"stopped after {r['frames']} of {frames} frames (exit {code})"
    notes = [f"missing {k}" for k in r["missing"]] + list(r["unsupported"])
    left = [s for s in r["shaders"] if s.get("effect", "none") == "none" and not s.get("post")]
    if left:
        notes.append(f"{len(left)} shaders left out")
    return g, True, "; ".join(notes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--kit", required=True)
    ap.add_argument("--out", default=str(build.ROOT / "check"))
    ap.add_argument("--frames", type=int, default=360)
    ap.add_argument("--cache", default=str(build.ROOT / ".cache"))
    args = ap.parse_args()
    kit, out, cache = Path(args.kit).resolve(), Path(args.out).resolve(), Path(args.cache).resolve()
    out.mkdir(parents=True, exist_ok=True)
    inp = out / "input.txt"
    inp.write_text(INPUT)
    games = [g for g in build.load_games(set(args.ids)) if g["redistribute"] and "owned" not in g]
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 2) as pool:
        results = list(pool.map(lambda g: run(g, kit, out, args.frames, cache, inp), games))
    version = (kit / "VERSION").read_text().strip() if (kit / "VERSION").is_file() else "?"
    lines = [f"# Games on love-mini {version} under qemu", "", f"{args.frames} frames each.", "",
             "| Game | Result | Notes |", "|---|---|---|"]
    for g, ok, note in results:
        lines.append(f"| {g['name']} | {'runs' if ok else 'FAILS'} | {note} |")
        build.log(f"{'ok  ' if ok else 'FAIL'}  {g['id']:14} {note}")
    text = "\n".join(lines) + "\n"
    (out / "summary.md").write_text(text, encoding="utf-8")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(text)
    subprocess.run([sys.executable, "-I", str(kit / "sheet.py"), str(out / "sheet.png")]
                   + [str(out / g["id"]) for g, _, _ in results], stdout=subprocess.DEVNULL)
    failed = [g["id"] for g, ok, _ in results if not ok]
    build.log(f"{len(results) - len(failed)} of {len(results)} games run" + (f"; failed: {', '.join(failed)}" if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
