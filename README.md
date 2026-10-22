# love-mini games

Games made with [LÖVE](https://love2d.org) 11, ready for the Miyoo Mini and Mini Plus on
[love-mini](https://github.com/l0st0npl4net/love-mini) (LÖVE for the Mini, under OnionOS).
Each one is installed with [Port Store](https://github.com/l0st0npl4net/PortStore-Catalog-MiyooMini)
like any other port: Port Store puts love-mini on the card with the first of them.

The games are their authors': this catalog only takes them from their repositories at a
known commit, adds what love-mini needs (a profile for the Mini's buttons, an entry in
OnionOS's Ports list, a picture) and packs them. Only open-source games are packed: their
code **and** everything they bring — pictures, sounds, music, fonts — under licenses that let
anyone share them (no "non-commercial only", no "may not be redistributed"). Games tried that
are not are listed with their results only. Which games play how well on a Mini:
[COMPATIBILITY.md](COMPATIBILITY.md).

## A game

`games/<id>/`:

- `game.json`:

  ```json
  {
    "id": "moonpong",
    "name": "Moon Pong",
    "love": "11",
    "source": { "github": "omrawaley/Moon-Pong", "commit": "<40 hex digits>", "dir": "MoonPong" },
    "license": "Apache-2.0",
    "redistribute": true,
    "status": "playable",
    "categories": ["sports"],
    "controls": "d-pad up and down",
    "tested": { "qemu": "runs", "mini-plus": "60 fps (0.3.0)" },
    "notes": ""
  }
  ```

  `source.dir`: the folder with `main.lua`. `redistribute`: whether everything in the game is
  under an open license (see above); a game that is not is left out of the release.
  `attribution`: credit the game's source does not give (another's pictures it uses), packed
  as `ATTRIBUTION.txt`. `skip`: paths of the source not packed (screenshots, other builds). `pack: "folder"`:
  the game goes onto the card as a folder, not a `.love` (a game that opens its own files by
  path). `porter`: who brought it (default `love-mini-games`).
- A game the player owns (a commercial one) has no `source` but `owned`:

  ```json
  "owned": {
    "files": ["Balatro.exe", "Balatro.love"],
    "what": "Balatro.exe (or Balatro.love) from your copy of Balatro",
    "hint": "where to find it and where it goes",
    "store": "https://store.steampowered.com/app/2379780/Balatro/",
    "search": ["Roms/PORTS/Games/Balatro"]
  },
  "wrapper": "wrapper"
  ```

  Nothing of the game is packed: only `wrapper/` (the profile and what it uses: Lua patches,
  a font, their licenses), an entry for Ports that checks the player's file, and a README.
  The catalog entry says `"assets": "owned"` and `needs` the file: Port Store shows where it
  goes and moves it from `App/PortStore/import/`, or from a folder of `search` (where another
  port of the game kept it). The profile adjusts the game as it loads
  (love-mini 0.4.0: `env`, `lua`, `edits`, `files`); the player's file is never changed.
- `profile.lua` (optional): love-mini's profile for the game, see love-mini's README (keys,
  the cursor for mouse games, the screen, shaders).
- `cover.png` (optional): its picture, 320×240. `tools/cover.py <id> <frame.png>` makes one
  from a frame of a run of the game with love-mini under qemu (love-mini's `tools/run.sh`).

## Building

```sh
tools/build.py            # every game: dist/<id>.zip, dist/<id>.png, dist/manifest.json, COMPATIBILITY.md
tools/build.py moonpong   # some games only (their manifest entries printed)
```

Python 3 and git; the sources are fetched at their commits into `.cache/`. A game's zip is laid
out from the SD card's root:

```
Roms/PORTS/Games/love-mini/games/<id>/game.love    (or the game's folder)
Roms/PORTS/Games/love-mini/games/<id>/profile.lua
Roms/PORTS/Games/love-mini/games/<id>/LICENSE.txt
Roms/PORTS/Shortcuts/LOVE games/<Name>.port        starts love-mini's run.sh <id>
Roms/PORTS/Imgs/<Name>.png
```

`manifest.json` is in the format of [Mixtape](https://github.com/snyderman3000/mixtape)'s
catalogs, each game with `"requires": ["love-mini"]` and `"folder": "LÖVE"` (in MiyooPorts,
Port Store 1.3.1 puts love-mini's games in that folder). Zips are made the same way every time,
so a game's version (`<commit>-<zip checksum>`) changes only when the game or what is added to
it does.

## Publishing

`.github/workflows/catalog.yml` builds the games on every change to `games/` or `tools/` and
publishes them as a release (`games-<date>-<run>`, marked latest). Port Store's catalog reads
`releases/latest/download/manifest.json` (its `recipes/sources/love-mini-games.json`).

## License

The tools and this catalog's own files (profiles, `game.json`, pictures made from the games):
MIT, see [LICENSE](LICENSE). Each game keeps its own license; it is packed with it.
