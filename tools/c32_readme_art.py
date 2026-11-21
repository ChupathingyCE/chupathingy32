#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 The Chupathingy contributors
# SPDX-FileCopyrightText: 2026 Milenko x Horrible Dev
# SPDX-License-Identifier: GPL-3.0-or-later
"""Makes the pictures in README.md, in the look of Windows 9x, from
Chupathingy32's icon (art/icon):

    python3 tools/c32_readme_art.py

It writes art/readme/:

- banner.png: a window, its title bar with the 16-pixel icon and three
  buttons, and in it the 64-pixel icon, the name and the line under it
- windows.png, linux.png, steam-link.png: a raised button for each build
- taskbar.png: a taskbar with the Chupathingy32 button pressed in, for the
  foot of the page

The letters are a 5 by 7 pixel font drawn here, capitals and figures only.
Everything is drawn at one pixel to a pixel in the 16 colors of the Windows
palette (and the title bar's blue fade), then made twice as big, nothing
smoothed. Python's standard library only. Run it again when the icon
changes.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from c32_icon import ART, ROOT, read_png, write_png  # noqa: E402

OUT = ROOT / "art" / "readme"
TIMES = 2

# the Windows palette's colors used here
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
FACE = (192, 192, 192, 255)
SHADOW = (128, 128, 128, 255)
LIGHT = (223, 223, 223, 255)
NAVY = (0, 0, 128, 255)
TITLE_END = (16, 132, 208, 255)
MAROON = (128, 0, 0, 255)
CLEAR = (0, 0, 0, 0)

FONT = {
    "A": [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "B": ["#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "],
    "C": [" ### ", "#   #", "#    ", "#    ", "#    ", "#   #", " ### "],
    "D": ["#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "],
    "E": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"],
    "F": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
    "G": [" ### ", "#   #", "#    ", "# ###", "#   #", "#   #", " ####"],
    "H": ["#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "I": [" ### ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    "J": ["  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "],
    "K": ["#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"],
    "L": ["#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"],
    "M": ["#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"],
    "N": ["#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"],
    "O": [" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "P": ["#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "],
    "Q": [" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"],
    "R": ["#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"],
    "S": [" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    "U": ["#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "V": ["#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "],
    "W": ["#   #", "#   #", "#   #", "# # #", "# # #", "# # #", " # # "],
    "X": ["#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"],
    "Y": ["#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "],
    "Z": ["#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"],
    "0": [" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "],
    "1": ["  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    "2": [" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"],
    "3": ["#####", "   # ", "  #  ", "   # ", "    #", "#   #", " ### "],
    "4": ["   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "],
    "5": ["#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "],
    "6": ["  ## ", " #   ", "#    ", "#### ", "#   #", "#   #", " ### "],
    "7": ["#####", "    #", "   # ", "  #  ", " #   ", " #   ", " #   "],
    "8": [" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "],
    "9": [" ### ", "#   #", "#   #", " ####", "    #", "   # ", " ##  "],
    "-": ["     ", "     ", "     ", " ### ", "     ", "     ", "     "],
    ".": ["     ", "     ", "     ", "     ", "     ", " ##  ", " ##  "],
    " ": ["   ", "   ", "   ", "   ", "   ", "   ", "   "],
}
FONT_HEIGHT = 7


class Canvas:
    def __init__(self, width: int, height: int, fill=CLEAR):
        self.width, self.height = width, height
        self.pixels = [[fill] * width for _ in range(height)]

    def put(self, x: int, y: int, color) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = color

    def rect(self, x: int, y: int, width: int, height: int, color) -> None:
        for row in range(y, y + height):
            for column in range(x, x + width):
                self.put(column, row, color)

    def bevel(self, x: int, y: int, width: int, height: int, raised: bool = True, outer: bool = True) -> None:
        """Windows 9x's edge: a raised one (light above and to the left,
        dark below and to the right) or a sunken one, two pixels deep"""
        top_left = [LIGHT, WHITE] if raised else [SHADOW, BLACK]
        bottom_right = [BLACK, SHADOW] if raised else [WHITE, LIGHT]
        for depth in range(2 if outer else 1):
            left, top = x + depth, y + depth
            right, bottom = x + width - 1 - depth, y + height - 1 - depth
            for column in range(left, right + 1):
                self.put(column, top, top_left[depth])
                self.put(column, bottom, bottom_right[depth])
            for row in range(top, bottom + 1):
                self.put(left, row, top_left[depth])
                self.put(right, row, bottom_right[depth])
            self.put(right, top, bottom_right[depth])
            self.put(left, bottom, bottom_right[depth])

    def image(self, x: int, y: int, path: Path) -> None:
        width, height, rows = read_png(path)
        for row in range(height):
            for column in range(width):
                pixel = tuple(rows[row][column * 4:column * 4 + 4])
                if pixel[3]:
                    self.put(x + column, y + row, pixel)

    def text(self, x: int, y: int, words: str, color, scale: int = 1, bold: bool = False) -> int:
        """the words from (x, y); the width they took"""
        start = x
        for letter in words:
            glyph = FONT[letter]
            for row, line in enumerate(glyph):
                for column, mark in enumerate(line):
                    if mark == "#":
                        for extra in range(2 if bold else 1):
                            self.rect(x + (column + extra) * scale, y + row * scale, scale, scale, color)
            x += (len(glyph[0]) + 1 + (1 if bold else 0)) * scale
        return x - start

    def png(self, times: int = TIMES) -> bytes:
        rows = []
        for line in self.pixels:
            row = b"".join(bytes(pixel) * times for pixel in line)
            rows.extend([row] * times)
        return write_png(self.width * times, rows)


def text_width(words: str, scale: int = 1, bold: bool = False) -> int:
    return sum((len(FONT[letter][0]) + 1 + (1 if bold else 0)) * scale for letter in words) - scale


def title_button(canvas: Canvas, x: int, y: int, kind: str) -> None:
    """a title bar's button, 16 by 14: minimize, maximize or close"""
    canvas.rect(x, y, 16, 14, FACE)
    canvas.bevel(x, y, 16, 14)
    if kind == "minimize":
        canvas.rect(x + 4, y + 9, 6, 2, BLACK)
    elif kind == "maximize":
        canvas.rect(x + 3, y + 2, 9, 9, BLACK)
        canvas.rect(x + 4, y + 4, 7, 6, FACE)
    else:
        for step in range(7):
            for thick in range(2):
                canvas.put(x + 4 + step + thick, y + 3 + step, BLACK)
                canvas.put(x + 10 - step + thick, y + 3 + step, BLACK)


def title_bar(canvas: Canvas, x: int, y: int, width: int, title: str) -> None:
    """a window's active title bar, 18 high: the blue fade, the icon, the
    title in bold, and its three buttons"""
    for column in range(width):
        share = column / max(1, width - 1)
        color = tuple(round(NAVY[index] + (TITLE_END[index] - NAVY[index]) * share) for index in range(3)) + (255,)
        canvas.rect(x + column, y, 1, 18, color)
    canvas.image(x + 1, y + 1, ART / "chupathingy32-16.png")
    canvas.text(x + 21, y + 6, title, WHITE, bold=True)
    right = x + width - 2
    title_button(canvas, right - 16, y + 2, "close")
    title_button(canvas, right - 16 - 2 - 16, y + 2, "maximize")
    title_button(canvas, right - 16 - 2 - 32, y + 2, "minimize")


def banner() -> Canvas:
    width, height = 410, 104
    canvas = Canvas(width, height, FACE)
    canvas.bevel(0, 0, width, height)
    title_bar(canvas, 3, 3, width - 6, "CHUPATHINGY32")
    # the window's inside: a sunken white panel, the icon and the words
    canvas.rect(6, 24, width - 12, height - 30, WHITE)
    canvas.bevel(6, 24, width - 12, height - 30, raised=False)
    canvas.image(18, 31, ART / "chupathingy32-64.png")
    name = "CHUPATHINGY32"
    canvas.text(96, 38, name, MAROON, scale=3)
    canvas.text(97, 72, "CHUPATHINGY FOR 32-BIT AND OLDER HARDWARE", BLACK)
    return canvas


def button(words: str) -> Canvas:
    width, height = text_width(words) + 14, 15
    canvas = Canvas(width, height, FACE)
    canvas.bevel(0, 0, width, height)
    canvas.text(7, 4, words, BLACK)
    return canvas


def taskbar() -> Canvas:
    width, height = 410, 22
    canvas = Canvas(width, height, FACE)
    for column in range(width):
        canvas.put(column, 0, LIGHT)
        canvas.put(column, 1, WHITE)
    # the window's button, pressed in, as the window in front's is
    label = "CHUPATHINGY32"
    button_width = 22 + text_width(label, bold=True) + 8
    canvas.bevel(3, 3, button_width, 17, raised=False)
    canvas.rect(5, 5, button_width - 4, 13, LIGHT)
    canvas.image(7, 4, ART / "chupathingy32-16.png")
    canvas.text(27, 8, label, BLACK, bold=True)
    # the tray, sunken, one pixel deep
    tray = "32-BIT"
    tray_width = text_width(tray) + 12
    left = width - 3 - tray_width
    canvas.bevel(left, 3, tray_width, 17, raised=False, outer=False)
    canvas.text(left + 6, 8, tray, BLACK)
    return canvas


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    pictures = {
        "banner.png": banner(),
        "windows.png": button("WINDOWS X86"),
        "linux.png": button("LINUX X86"),
        "steam-link.png": button("STEAM LINK"),
        "taskbar.png": taskbar(),
    }
    for name, canvas in pictures.items():
        (OUT / name).write_bytes(canvas.png())
        print(f"art/readme/{name} ({canvas.width * TIMES}x{canvas.height * TIMES})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
