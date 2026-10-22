# Compatibility

The games of this catalog on love-mini: under qemu (the Mini's build of love-mini, a test run
of a few hundred frames) and on a Mini Plus (frame times from love-mini's log). Made by `tools/build.py`
from `games/*/game.json`: change those, not this file.

Shared: whether its license (code, pictures, sounds, fonts) lets this catalog share it; a
game that is not is listed for its results only.

| Game | Shared | qemu | Mini Plus | Controls | License | Notes |
|---|---|---|---|---|---|---|
| [Balatro](https://store.steampowered.com/app/2379780/Balatro/) | wrapper only (your copy) | — | — | gamepad: d-pad and A to pick cards, as the game's own controller support | Commercial (LocalThunk, Playstack): the game is not included. This wrapper: MIT; PortMaster's Balatro patches: MIT; Nunito: SIL OFL 1.1 | Not yet tried on love-mini: its shaders (card editions, the swirling background, CRT) are left out, so it looks flatter than on a PC. |
| [Curse of the Arrow](https://github.com/egordorichev/CurseOfTheArrow) | no | runs | 60 fps (0.2.2) | B jump, A shoot, d-pad | GPL-3.0 (code), CC BY-NC-SA 4.0 (assets) | Not shared from here: its pictures and sounds are for non-commercial use only (CC BY-NC-SA), so the game is not open source. |
| [Flash Blip](https://github.com/plinkr/flash-blip) | yes | runs | 52 ms a frame (0.2.0, 8 shaders left out) | gamepad | MIT | Its glow, blur and CRT shaders are left out on the Mini. |
| [Gravity Wars](https://github.com/whyboris/Gravity-Wars) | yes | runs | 20 ms a frame (0.2.0) | d-pad aim, A fire | MIT |  |
| [KleleAtoms](https://github.com/Nightwolf-47/KleleAtoms) | yes | runs | 60 fps (0.3.0) | cursor: d-pad, A click | MIT | Played with love-mini's cursor: the d-pad moves it, A clicks. |
| [LOVEchess](https://github.com/badduck32/LOVEchess) | yes | runs | 60 fps (0.3.0) | cursor: d-pad, A click | MIT (code); chess pieces apparently Wikimedia Commons' Chess Pieces Sprite (CC BY-SA 3.0) | Played with love-mini's cursor: the d-pad moves it, A clicks. |
| [Lovetris](https://github.com/sharkwouter/lovetris) | yes | runs | 60 fps (0.2.0) | gamepad | MIT-style (code, Classic by rxi), Bitstream Vera / DejaVu (fonts) |  |
| [Max Downforce](https://github.com/Foppygames/max-downforce) | no | runs | 18 ms a frame (0.2.1) | A accelerate, d-pad steer, Start | GPL-3.0 (code), CC BY 4.0 (music by Kevin MacLeod, LICENSE-MUSIC) | Not shared from here: its font (RetroVille NC by Jayvee D. Enaguas) says all rights reserved; the rest is GPL-3.0 and CC BY 4.0 music. |
| [Monkune](https://github.com/JadedCtrl/Monkune) | yes | runs | 60 fps (0.2.1) | d-pad, A, Start | GPL-3.0 (code), free culture licenses per asset (art/*.txt: CC BY, CC0, public domain) |  |
| [Moon Pong](https://github.com/omrawaley/Moon-Pong) | yes | runs | runs (0.2.0) | d-pad up and down | Apache-2.0 |  |
| [Tux Swimmer](https://github.com/nicolas-sabbatini/tux-swimmer) | no | runs | 20 ms a frame (0.2.0) | A swim, Start | MIT | Not shared from here: its font (FFF Forward by Fonts For Flash) may not be redistributed; the code is MIT. |
