#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 The Chupathingy contributors
# SPDX-FileCopyrightText: 2026 Milenko x Horrible Dev
# SPDX-License-Identifier: GPL-3.0-or-later
"""Builds one Chupathingy32 target in one configuration, and collects what it
built into dist/:

    python3 tools/c32_build.py linux release      (on Linux)
    python tools/c32_build.py windows release     (on Windows)

The 32-bit Windows and Linux builds are the game's own (ninja windows,
ninja linux): this runs the game's tools/ci_build.py in the chupathingyce
submodule, so the build rules, the system root, SDL, the movies' FFmpeg and
the packaging are the game's, and none of it is copied here. What this adds:

- HALO_UPDATE_REPOSITORY=ChupathingyCE/chupathingy32 (unless the
  environment already names one), so a release's self-updater looks for
  updates on this repository's releases, not the game's. A game commit
  from before HALO_UPDATE_REPOSITORY (tools/version.py) would ignore it and
  update from the game's releases, so a build that looks for updates (a
  release, a test build, a nightly) is refused on such a commit; a -dev
  build never looks for updates and is still built.
- Chupathingy32's own icon (art/icon, tools/c32_icon.py): on Windows the
  game's port/windows/halo.ico is swapped for art/icon/chupathingy32.ico
  while the game builds, and put back after, so chupathingy.exe carries it;
  on Linux the icon's PNGs and desktop-entry.sh go beside the game.
- The game's dist/chupathingyce-<platform>-<config> folder, moved to this
  repository's dist/, and its symbols (Windows: the PDBs and the map) to
  symbols/, apart from what players download.

The version comes from the environment as for the game (its
tools/version.py): HALO_VERSION and HALO_RELEASE_BUILD=1 for a release,
<VERSION>-testing.<serial> or <VERSION>-nightly.<serial> for a test build or
a nightly. Without them, a build is the game's VERSION -dev and never looks
for updates. CI_COMPILER_LAUNCHER (ccache) is passed on, as the game's.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GAME = ROOT / "chupathingyce"
REPOSITORY = "ChupathingyCE/chupathingy32"
# what the game's tools/version.py has once it knows HALO_UPDATE_REPOSITORY
# (ChupathingyCE/chupathingyce#1461)
UPDATE_REPOSITORY_SUPPORT = "HALO_UPDATE_REPOSITORY"
# a test build's or a nightly's version (the game's PRERELEASE_VERSION, in
# short: the game's tools/version.py checks it in full)
PRERELEASE = re.compile(r"-(testing|nightly)\.\d{12}$")
# Chupathingy32's targets that are the game's own builds: the game's name
# for each (tools/ci_build.py)
GAME_BUILDS = {"windows": "windows", "linux": "linux"}
ICON = ROOT / "art" / "icon"
# the game's Windows icon, which its resource script (port/windows/halo.rc)
# builds into the executable
GAME_WINDOWS_ICON = GAME / "port" / "windows" / "halo.ico"
# what goes beside the Linux game: the icon at the sizes a desktop's menu
# uses, and the script that makes a menu entry for the folder it is in
LINUX_ICON_SIZES = (16, 24, 32, 48, 64, 128, 256)
LINUX_DESKTOP_SCRIPT = ROOT / "tools" / "linux" / "desktop-entry.sh"


def looks_for_updates(env: dict) -> bool:
    """whether this build's self-updater looks for updates: a release's
    (HALO_RELEASE_BUILD=1), a test build's or a nightly's"""
    return env.get("HALO_RELEASE_BUILD") == "1" or bool(PRERELEASE.search(env.get("HALO_VERSION", "")))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("target", choices=sorted(GAME_BUILDS))
    parser.add_argument("config", choices=["debug", "release"])
    args = parser.parse_args()

    if not (GAME / "tools/ci_build.py").is_file():
        print("error: the chupathingyce submodule is missing: git submodule update --init", file=sys.stderr)
        return 1
    platform = GAME_BUILDS[args.target]
    env = dict(os.environ)
    env.setdefault("HALO_UPDATE_REPOSITORY", REPOSITORY)
    version_py = (GAME / "tools/version.py").read_text(encoding="utf-8")
    if looks_for_updates(env) and UPDATE_REPOSITORY_SUPPORT not in version_py:
        print(f"error: {env.get('HALO_VERSION') or 'this build'} would look for updates, but the game's commit "
              "has no HALO_UPDATE_REPOSITORY (chupathingyce/tools/version.py), so it would update from the "
              "game's releases: move the submodule to a game commit with it (ChupathingyCE/chupathingyce#1461)",
              file=sys.stderr)
        return 1
    print(f"updates from {env['HALO_UPDATE_REPOSITORY']}'s releases", flush=True)
    command = [sys.executable, "tools/ci_build.py", platform, args.config]
    print("+", " ".join(command), f"(in {GAME.name})", flush=True)
    if platform == "windows":
        game_icon = GAME_WINDOWS_ICON.read_bytes()
        GAME_WINDOWS_ICON.write_bytes((ICON / "chupathingy32.ico").read_bytes())
        try:
            subprocess.run(command, cwd=GAME, env=env, check=True)
        finally:
            GAME_WINDOWS_ICON.write_bytes(game_icon)
    else:
        subprocess.run(command, cwd=GAME, env=env, check=True)

    name = f"chupathingyce-{platform}-{args.config}"
    built = GAME / "dist" / name
    if not built.is_dir():
        print(f"error: the game's build left no {built.relative_to(ROOT)}", file=sys.stderr)
        return 1
    for folder, source in (("dist", built), ("symbols", GAME / "dist" / f"{name}-symbols")):
        target = ROOT / folder / name
        if target.exists():
            shutil.rmtree(target)
        if source.is_dir():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(target))
            print(f"{source.relative_to(ROOT)} -> {target.relative_to(ROOT)}", flush=True)
    if platform == "linux":
        # (flat, at the folder's top: the self-updater takes only those)
        for size in LINUX_ICON_SIZES:
            shutil.copyfile(ICON / f"chupathingy32-{size}.png", ROOT / "dist" / name / f"chupathingy32-{size}.png")
        shutil.copyfile(LINUX_DESKTOP_SCRIPT, ROOT / "dist" / name / LINUX_DESKTOP_SCRIPT.name)
    for path in sorted((ROOT / "dist" / name).iterdir()):
        print(f"  {path.name} ({path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
