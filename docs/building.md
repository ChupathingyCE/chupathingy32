# Building Chupathingy32

Chupathingy32 builds the game with the game's own build. This repository
adds the release settings, the icon and the packaging, so most of what you
need is what the game needs.

Get the code with the game:

```sh
git clone --recursive https://github.com/ChupathingyCE/chupathingy32.git
cd chupathingy32
```

In a clone you already have: `git submodule update --init`.

A build of your own is a `-dev` build and never looks for updates.

## Windows (x86)

Build on Windows. You need what the game's
[Windows notes](https://github.com/ChupathingyCE/chupathingyce/blob/main/port/windows/README.md)
list: Visual Studio or its Build Tools with the C++ workload (for the 32-bit
x86 libraries and the Windows SDK), LLVM (clang, lld and llvm-rc), Python 3
and ninja. MSYS2 with `make` builds the movies' FFmpeg.

```sh
python tools/c32_build.py windows release
```

The result is `dist/chupathingyce-windows-release`. While the game builds,
`tools/c32_build.py` swaps the game's icon for Chupathingy32's and puts the
game's back after.

## Linux (x86)

Build on Linux. CI uses Ubuntu 24.04 with clang 22 from
[apt.llvm.org](https://apt.llvm.org) (`clang-22`, `lld-22`, `llvm-22`,
`libclang-rt-22-dev`, with `/usr/lib/llvm-22/bin` first on `PATH`), plus
`gcc-multilib`, `libc6-dev-i386`, `cmake`, `pkg-config`, `libwayland-bin`,
`ninja-build` and `zstd`. The game's
[Linux notes](https://github.com/ChupathingyCE/chupathingyce/blob/main/port/linux/README.md)
have the details.

```sh
python3 tools/c32_build.py linux release
```

The result is `dist/chupathingyce-linux-release`, with the icon's PNGs and
`desktop-entry.sh` beside the game. The build links against Debian 11's
32-bit glibc, which the game's build downloads, so it starts on older
systems too.

`debug` instead of `release` makes a debug build.

## The Steam Link

The Steam Link build is a cross build for the box's 32-bit ARM, made on
Linux with clang and Valve's
[Steam Link SDK](https://github.com/ValveSoftware/steamlink-sdk). The
[Steam Link workflow](../.github/workflows/steamlink.yml) is the reference
for every step and its pinned versions.

1. Get the SDK's toolchain and root filesystem beside this repository, or
   anywhere with `MARVELL_SDK_PATH` set. The whole SDK is about 3 GB, so a
   sparse checkout is enough:

   ```sh
   git init steamlink-sdk && cd steamlink-sdk
   git remote add origin https://github.com/ValveSoftware/steamlink-sdk.git
   git sparse-checkout set toolchain rootfs
   git fetch --depth 1 --filter=blob:none origin master
   git checkout FETCH_HEAD
   cd ..
   ```

2. Build SDL3 for the box (the game's SDL version) with
   `port/steamlink/toolchain.cmake`, installed to `build/sdl3`. The
   workflow's "Build SDL3" step has the exact options.
3. Build the game:

   ```sh
   cd chupathingyce
   python3 configure.py --release --console-port ../port/steamlink
   ninja steamlink
   cd ..
   ```

4. Package it: `python3 port/steamlink/package.py` makes
   `build/chupathingyce.tgz` for the USB stick and
   `build/chupathingyce-steamlink-release.zip` for the updater.

[steam-link.md](steam-link.md) has how to install it.

## The icon

The icon's pixel art is in `art/icon/`, at each size it's drawn at.
`python3 tools/c32_icon.py` makes the Windows `.ico`, the Linux PNGs and
the Steam Link's icon from it. Run it after changing the art, and commit
what it writes.

`python3 tools/c32_readme_art.py` makes the README's pictures in
`art/readme/` from the icon. Run it after changing the icon too.

## Releases

Releases, test builds and nightlies are made by the Release workflow and
signed by ChupathingyCE's release workflows. No key is ever in this
repository. [releases.md](releases.md) has the whole flow.
