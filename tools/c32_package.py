#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 The Chupathingy contributors
# SPDX-FileCopyrightText: 2026 Milenko x Horrible Dev
# SPDX-License-Identifier: GPL-3.0-or-later
"""Zips the builds in a folder for a release, as the game's releases are:

    python3 tools/c32_package.py artifacts release

Each build folder chupathingyce-<platform>-<config> under the first folder
(at any depth: downloaded artifacts are one folder deeper) becomes
release/chupathingyce-<platform>-<config>.zip, its files at the zip's root,
stored rather than deflated (the self-updaters read stored entries most
simply), with the Linux game's programs marked executable (artifacts lose
the bit). The names are the game's 32-bit ones, windows and linux, which the
self-updater of a 32-bit install asks for (its update platform): they are
not renamed here, or installs in the field would not find their update.
Then SHA256SUMS, as sha256sum writes it.
"""

import argparse
import hashlib
import re
import sys
import zipfile
from pathlib import Path

BUILD = re.compile(r"^chupathingyce-(windows|linux)-(release|debug)$")
# the Linux game, its old name's stub, and the libraries beside them
EXECUTABLE = {"chupathingy", "halo"}


def package(build: Path, out: Path) -> Path:
    zip_path = out / f"{build.name}.zip"
    linux = "-linux-" in build.name
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_STORED) as archive:
        for path in sorted(build.rglob("*")):
            if not path.is_file():
                continue
            name = path.relative_to(build).as_posix()
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_STORED
            mode = 0o755 if linux and (name in EXECUTABLE or name.endswith(".so.0")) else 0o644
            info.external_attr = (0o100000 | mode) << 16
            info.create_system = 3
            archive.writestr(info, path.read_bytes())
    return zip_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("builds", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    builds = sorted(path for path in args.builds.rglob("*") if path.is_dir() and BUILD.match(path.name))
    if not builds:
        print(f"error: no chupathingyce-<windows|linux>-<config> folder in {args.builds}", file=sys.stderr)
        return 1
    names = [build.name for build in builds]
    if len(names) != len(set(names)):
        print(f"error: a build is there twice: {names}", file=sys.stderr)
        return 1
    sums = []
    for build in builds:
        if any(part == "maps" for path in build.rglob("*") for part in path.relative_to(build).parts):
            print(f"error: {build} has a maps folder; game files are never released", file=sys.stderr)
            return 1
        zip_path = package(build, args.out)
        sums.append(f"{hashlib.sha256(zip_path.read_bytes()).hexdigest()}  {zip_path.name}\n")
        print(f"{build} -> {zip_path} ({zip_path.stat().st_size} bytes)")
    (args.out / "SHA256SUMS").write_text("".join(sums))
    print((args.out / "SHA256SUMS").read_text(), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
