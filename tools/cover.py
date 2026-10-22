#!/usr/bin/env python3
"""A game's cover from a frame of a run with love-mini (its tools/run.sh: <out>/frames,
PNGs of RGB rows without filters, as love-mini's tools/ppm2png.py writes them): fitted
into 320x240 on black, written as games/<id>/cover.png. Standard library only.

    tools/cover.py ID FRAME.png"""
import struct
import sys
import zlib
from pathlib import Path

W, H = 320, 240


def read_png(path):
    data = Path(path).read_bytes()
    pos, idat, w, h = 8, b"", 0, 0
    while pos < len(data):
        n, t = struct.unpack(">I4s", data[pos:pos + 8])
        body = data[pos + 8:pos + 8 + n]
        if t == b"IHDR":
            w, h, depth, color = struct.unpack(">IIBB", body[:10])
            if (depth, color) != (8, 2):
                raise SystemExit(f"{path}: not 8-bit RGB")
        elif t == b"IDAT":
            idat += body
        pos += 12 + n
    raw = zlib.decompress(idat)
    stride = w * 3 + 1
    rows = []
    for y in range(h):
        if raw[y * stride] != 0:
            raise SystemExit(f"{path}: filtered rows: not one of love-mini's frames")
        rows.append(raw[y * stride + 1:(y + 1) * stride])
    return w, h, rows


def write_png(path, w, h, rgb):
    raw = b"".join(b"\x00" + rgb[y * w * 3:(y + 1) * w * 3] for y in range(h))
    chunk = lambda t, d: struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xffffffff)
    Path(path).write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
                           + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def main():
    gid, frame = sys.argv[1], sys.argv[2]
    w, h, rows = read_png(frame)
    s = min(W / w, H / h)
    cw, ch = max(1, int(w * s)), max(1, int(h * s))
    ox, oy = (W - cw) // 2, (H - ch) // 2
    out = bytearray(W * H * 3)
    for y in range(ch):
        # a box of source pixels per cover pixel: a smaller picture without moiré
        y0, y1 = int(y / s), max(int(y / s) + 1, int((y + 1) / s))
        for x in range(cw):
            x0, x1 = int(x / s), max(int(x / s) + 1, int((x + 1) / s))
            acc = [0, 0, 0]
            n = 0
            for yy in range(y0, min(y1, h)):
                row = rows[yy]
                for xx in range(x0, min(x1, w)):
                    acc[0] += row[xx * 3]; acc[1] += row[xx * 3 + 1]; acc[2] += row[xx * 3 + 2]
                    n += 1
            d = ((oy + y) * W + ox + x) * 3
            out[d:d + 3] = bytes(v // max(1, n) for v in acc)
    dest = Path(__file__).resolve().parent.parent / "games" / gid / "cover.png"
    write_png(dest, W, H, bytes(out))
    print(dest)


if __name__ == "__main__":
    main()
