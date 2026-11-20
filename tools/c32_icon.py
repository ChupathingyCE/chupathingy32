#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 The Chupathingy contributors
# SPDX-FileCopyrightText: 2026 Milenko x Horrible Dev
# SPDX-License-Identifier: GPL-3.0-or-later
"""Makes Chupathingy32's icons from the pixel art in art/icon/:

    python3 tools/c32_icon.py

The art is pixel art made at each size, as Windows 9x icons were: 16, 24,
32, 48, 58 and 64 pixels (art/icon/icon-<size>.png), in the 16 colors of
the Windows palette. It is the game's own icon (port/art/icon.svg in the
game: the helmet with tusks, on red) traced at each size, with a black
outline, shading and a raised edge; the 16-pixel one is drawn by hand.
Nothing is smoothed: bigger sizes are a smaller one's pixels made 2 or 4
times as big. This writes

- art/icon/chupathingy32.ico: the Windows executable's icon (16, 24, 32, 48
  and 256 pixels, the 256 one the 64 made 4 times as big)
- art/icon/chupathingy32-<size>.png: 16, 24, 32, 48, 64, 128 and 256 pixels,
  for the Linux download and its menu entry (tools/c32_build.py)
- port/steamlink/app/icon.png: the Steam Link's menu icon, 116 pixels (the
  58 made twice as big)

Python's standard library only. Run it again when the art changes.
"""

import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "art" / "icon"
STEAMLINK_ICON = ROOT / "port" / "steamlink" / "app" / "icon.png"
# (size made, from the art at size, times)
LINUX_SIZES = {16: (16, 1), 24: (24, 1), 32: (32, 1), 48: (48, 1), 64: (64, 1), 128: (64, 2), 256: (64, 4)}
ICO_SIZES = {16: (16, 1), 24: (24, 1), 32: (32, 1), 48: (48, 1), 256: (64, 4)}


def read_png(path: Path):
    """an 8-bit RGBA or RGB PNG's (width, height, rows of RGBA bytes)"""
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path}: not a PNG")
    offset, idat, header = 8, b"", None
    while offset < len(data):
        length, kind = struct.unpack(">I4s", data[offset:offset + 8])
        body = data[offset + 8:offset + 8 + length]
        if kind == b"IHDR":
            header = struct.unpack(">IIBBBBB", body)
        elif kind == b"IDAT":
            idat += body
        offset += 12 + length
    width, height, depth, color, _, _, interlace = header
    if depth != 8 or color not in (2, 6) or interlace:
        raise ValueError(f"{path}: needs 8-bit RGB or RGBA, not interlaced")
    channels = 4 if color == 6 else 3
    raw = zlib.decompress(idat)
    stride = width * channels
    rows, previous, at = [], bytearray(stride), 0
    for _ in range(height):
        kind, line = raw[at], bytearray(raw[at + 1:at + 1 + stride])
        at += 1 + stride
        for i in range(stride):
            left = line[i - channels] if i >= channels else 0
            up = previous[i]
            corner = previous[i - channels] if i >= channels else 0
            if kind == 1:
                line[i] = (line[i] + left) & 255
            elif kind == 2:
                line[i] = (line[i] + up) & 255
            elif kind == 3:
                line[i] = (line[i] + (left + up) // 2) & 255
            elif kind == 4:
                guess = left + up - corner
                a, b, c = abs(guess - left), abs(guess - up), abs(guess - corner)
                line[i] = (line[i] + (left if a <= b and a <= c else up if b <= c else corner)) & 255
        previous = line
        if channels == 3:
            line = bytearray(b"".join(bytes(line[i:i + 3]) + b"\xff" for i in range(0, stride, 3)))
        rows.append(bytes(line))
    return width, height, rows


def write_png(width: int, rows) -> bytes:
    def chunk(kind: bytes, body: bytes) -> bytes:
        return struct.pack(">I", len(body)) + kind + body + struct.pack(">I", zlib.crc32(kind + body))
    raw = b"".join(b"\x00" + row for row in rows)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, len(rows), 8, 6, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b""))


def scaled(size: int, times: int) -> bytes:
    """the art at size, each pixel made times by times"""
    width, height, rows = read_png(ART / f"icon-{size}.png")
    if (width, height) != (size, size):
        raise ValueError(f"icon-{size}.png is {width}x{height}")
    out = []
    for row in rows:
        line = b"".join(row[x * 4:x * 4 + 4] * times for x in range(width))
        out += [line] * times
    return write_png(width * times, out)


def write_ico(path: Path) -> None:
    images = [(size, scaled(*ICO_SIZES[size])) for size in sorted(ICO_SIZES)]
    data = struct.pack("<HHH", 0, 1, len(images))
    offset = 6 + 16 * len(images)
    for size, image in images:
        data += struct.pack("<BBBBHHII", size % 256, size % 256, 0, 0, 1, 32, len(image), offset)
        offset += len(image)
    path.write_bytes(data + b"".join(image for _, image in images))


def main() -> int:
    write_ico(ART / "chupathingy32.ico")
    for size, (art, times) in LINUX_SIZES.items():
        (ART / f"chupathingy32-{size}.png").write_bytes(scaled(art, times))
    STEAMLINK_ICON.write_bytes(scaled(58, 2))
    for path in [ART / "chupathingy32.ico", *(ART / f"chupathingy32-{s}.png" for s in LINUX_SIZES), STEAMLINK_ICON]:
        print(f"{path.relative_to(ROOT)} ({path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
