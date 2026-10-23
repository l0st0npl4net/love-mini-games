# Compatibility

The games of this catalog on love-mini: under qemu (the Mini's build of love-mini, a test run
of a few hundred frames) and on a Mini Plus (frame times from love-mini's log). Made by `tools/build.py`
from `games/*/game.json`: change those, not this file.

Shared: whether its license (code, pictures, sounds, fonts) lets this catalog share it; a
game that is not is listed for its results only.

| Game | Shared | qemu | Mini Plus | Controls | License | Notes |
|---|---|---|---|---|---|---|
| [Balatro](https://store.steampowered.com/app/2379780/Balatro/) | wrapper only (your copy) | — | runs, about 23 fps (love-mini 0.3.1, before its profile) | gamepad: d-pad and A to pick cards, as the game's own controller support | Commercial (LocalThunk, Playstack): the game is not included. This wrapper: MIT; PortMaster's Balatro patches: MIT; Nunito: SIL OFL 1.1 | Its shaders (card editions, CRT) are left out, so it looks flatter than on a PC; its swirling background is a flat colour. |
| [Bomb Klotski](https://codeberg.org/MossyGreySlope/Bomb-Klotski) | yes | runs | — | cursor: d-pad, hold A to drag a block | AGPL-3.0-or-later | LÖVE Jam 2025, by MossyGreySlope. |
| [Box Smasher](https://github.com/rollerozxa/boxsmasher) | yes | runs | — | cursor: d-pad, hold A and let go to throw | GPL-3.0-or-later (code, pictures), CC0 (sounds), OFL 1.1 (font) |  |
| [Curse of the Arrow](https://github.com/egordorichev/CurseOfTheArrow) | no | runs | 60 fps (0.2.2) | B jump, A shoot, d-pad | GPL-3.0 (code), CC BY-NC-SA 4.0 (assets) | Not shared from here: its pictures and sounds are for non-commercial use only (CC BY-NC-SA), so the game is not open source. |
| [Down Sheep](https://gitlab.com/alexjgriffith/downsheep) | yes | runs | — | d-pad, A jump, X switch sheep, Menu | GPL-3.0 (code), CC BY 4.0 (pictures by Alexander Griffith; music Thunder Hoodie Beats), CC BY 3.0 (sounds: NenadSimic, Lamoot), OFL 1.1 (fonts Avara, Inconsolata) | Lisp Game Jam 2020, by Alexander Griffith (in Fennel). |
| [Flash Blip](https://github.com/plinkr/flash-blip) | yes | runs | 52 ms a frame (0.2.0, 8 shaders left out) | gamepad | MIT | Its glow, blur and CRT shaders are left out on the Mini. |
| [GMSweeper](https://github.com/GreffMASTER/GMSweeper) | yes | runs | — | cursor: d-pad, A open, B flag; Start new game | MIT |  |
| [Granite Crash](https://github.com/Varkalandar/granite_crash) | yes | runs | — | d-pad | GPL-3.0-or-later | Alpha: 7 maps. |
| [Gravity Wars](https://github.com/whyboris/Gravity-Wars) | yes | runs | 20 ms a frame (0.2.0) | d-pad aim, A fire | MIT |  |
| [HELO](https://github.com/paulpls/helo) | yes | runs | — | A fly, Start again | GPL-3.0 (code and pictures, by paulpls) | By paulpls. |
| [In Your Face City Trains](https://github.com/SimonLarsen/iyfct) | yes | runs | — | A jump, Start, Y restart, Select pause | GPL-3.0 (code), CC BY 3.0 (pictures, sounds; music "The rb Sequence" by Fighter X) | By Simon Larsen. |
| [KleleAtoms](https://github.com/Nightwolf-47/KleleAtoms) | yes | runs | 60 fps (0.3.0) | cursor: d-pad, A click | MIT | Played with love-mini's cursor: the d-pad moves it, A clicks. |
| [LOVEchess](https://github.com/badduck32/LOVEchess) | yes | runs | 60 fps (0.3.0) | cursor: d-pad, A click | MIT (code); chess pieces apparently Wikimedia Commons' Chess Pieces Sprite (CC BY-SA 3.0) | Played with love-mini's cursor: the d-pad moves it, A clicks. |
| [Lovetris](https://github.com/sharkwouter/lovetris) | yes | runs | 60 fps (0.2.0) | gamepad | MIT-style (code, Classic by rxi), Bitstream Vera / DejaVu (fonts) |  |
| [Max Downforce](https://github.com/Foppygames/max-downforce) | no | runs | 18 ms a frame (0.2.1) | A accelerate, d-pad steer, Start | GPL-3.0 (code), CC BY 4.0 (music by Kevin MacLeod, LICENSE-MUSIC) | Not shared from here: its font (RetroVille NC by Jayvee D. Enaguas) says all rights reserved; the rest is GPL-3.0 and CC BY 4.0 music. |
| [Monkune](https://github.com/JadedCtrl/Monkune) | yes | runs | 60 fps (0.2.1) | d-pad, A, Start | GPL-3.0 (code), free culture licenses per asset (art/*.txt: CC BY, CC0, public domain) |  |
| [Moon Pong](https://github.com/omrawaley/Moon-Pong) | yes | runs | runs (0.2.0) | d-pad up and down | Apache-2.0 |  |
| [Mr. Rescue](https://github.com/SimonLarsen/mrrescue) | yes | runs | — | A jump, B shoot, X action, d-pad; Start and Menu in menus | zlib (code), CC BY-SA 3.0 (pictures, music, sounds: Tangram Games), MIT (slam, AnAL; TSerial stand-in: this catalog's) | By Simon Larsen and Tangram Games. |
| [NEON PHASE](https://github.com/eevee/neon-phase) | yes | runs | 32 ms a frame (0.3.0) | gamepad | ISC (code), CC BY-SA 4.0 (pictures, music, sounds, maps), CC0 (font m5x7 by Daniel Linssen) | By Eevee and GlitchedPuppet, set in GlitchedPuppet's Floraverse. |
| [Phibonacci](https://github.com/AlexanDDOS/Phibonacci) | yes | runs | — | d-pad; Select: the cursor for Restart and Undo | MIT (code), OFL 1.1 (font Lato) | 2048 with Fibonacci numbers. |
| [Seismic Afterburner](https://github.com/rominou66/Love-Jam-2022-Seismic-Afterburner) | yes | runs | — | d-pad, A shoot, B afterburner, Start | AGPL-3.0 (code, pictures), CC0 (music by SketchyLogic), CC BY 3.0 / 4.0 (sounds: dklon, KuraiWolf, Michel Baradari), OFL 1.1 (font Press Start 2P) | LÖVE Jam 2022, by rominou66. Upright screen: small on the Mini. |
| [Six Card Golf](https://github.com/CGagnier/six-card-golf) | yes | runs | — | d-pad, A take or flip, B close | MIT | Against the Mini. |
| [SNAK'](https://github.com/Keyslam/SNAK) | yes | runs | — | d-pad, A restart the level | MIT (code, tiles), OFL 1.1 (font Press Start 2P) | Its blur, grain and vignette shaders are left out on the Mini. |
| [StayClose](https://github.com/ThunderNL/StayClose) | yes | runs | — | gamepad: d-pad the red ship, A/B/X/Y the blue one, Start | MIT (code, pictures, music), CC BY 3.0 (font Boxy Bold by william.thompsonj) | LÖVE Jam 2023, by ThunderNL. |
| [Super Jump And Dash Man](https://github.com/neguse/SuperJumpAndDashMan) | yes | runs | — | d-pad, A jump, B dash | zlib (code, sounds) | LÖVE Jam 2019, by neguse. |
| [The Return of the Rogue](https://github.com/bastienleonard/7drl2022) | yes | runs | — | d-pad, A act, X rest | GPL-3.0 (code), OFL 1.1 (font Source Code Pro) | A 7DRL 2022 roguelike in letters, by Bastien Léonard. |
| [Tower of the Cryptolich](https://github.com/dbisdorf/cryptolich) | yes | runs | — | d-pad, A shoot, B aim, Start | MIT (code, pictures, sounds), CC BY-SA 4.0 (font Mx437 IBM BIOS by VileR) | By Dan Bisdorf. |
| [Tux Swimmer](https://github.com/nicolas-sabbatini/tux-swimmer) | no | runs | 20 ms a frame (0.2.0) | A swim, Start | MIT | Not shared from here: its font (FFF Forward by Fonts For Flash) may not be redistributed; the code is MIT. |
| [Zero Velocity](https://github.com/theoratkin/zero-velocity) | yes | runs | — | d-pad turn, A fire | GPL-3.0-or-later (code), CC BY-SA 4.0 (pictures), CC BY 4.0 (music by Eric Skiff), CC0 (laser sound), OFL 1.1 (font Press Start 2P), MIT (moonshine, classic) | Its glow, CRT and scanline shaders are left out on the Mini. |
