<h1 align="center">Chupathingy32</h1>

<p align="center"><b>Chupathingy for 32-bit and older hardware.</b></p>

<p align="center">
<a href="https://github.com/ChupathingyCE/chupathingy32/releases">Releases</a> ·
<a href="https://github.com/ChupathingyCE/chupathingyce">The game</a> ·
<a href="https://stats.chupathingy.org">Games online now</a> ·
<a href="https://chupathingy.org">chupathingy.org</a>
</p>

Chupathingy32 is the home of the Chupathingy builds for older machines:
32-bit Windows, 32-bit Linux, and soon the Steam Link. They play online with
every other Chupathingy build, on PCs, Macs, phones and consoles.

It's the same game as Chupathingy, from the same code. This repository holds
the game as the `chupathingyce` submodule and builds it for these machines.
Each release ships the same game commit as the matching Chupathingy release.

You need your own copy of Halo. No game files are included.

**Status: in testing.** The first release is planned with Chupathingy 0.9.2.

## Which build?

| Machine | Download | Notes |
| --- | --- | --- |
| Windows, 32-bit (x86) | `chupathingyce-windows-release.zip` | Windows 10 or later. |
| Linux, 32-bit (x86) | `chupathingyce-linux-release.zip` | glibc 2.31 or later (32-bit). Brings its own SDL3. |
| Steam Link | Not yet | Planned. See [The Steam Link](#the-steam-link). |

On a 64-bit PC or a Mac, get the game's own builds instead: they run better.
They're on [Chupathingy's releases](https://github.com/ChupathingyCE/chupathingyce/releases/latest).
The 32-bit Windows build offers the 64-bit one when it starts on 64-bit
Windows.

## Install

1. Download the zip for your machine from
   [Releases](https://github.com/ChupathingyCE/chupathingy32/releases) and
   unzip it into a folder of its own.
2. Start `chupathingy.exe` on Windows, or `chupathingy` on Linux.
3. The first time, it asks for your Halo disc image and copies the maps out
   of it.

Everything else works as in the game's own builds. Its
[install guide](https://github.com/ChupathingyCE/chupathingyce/blob/main/docs/install.md)
has the details: where your saves go, the maps folders, and the first start
on Windows.

The 32-bit and 64-bit builds use the same folders for saves and settings,
so you can switch between them.

## Updates

The game checks for a new version when it starts and asks before updating.
Chupathingy32's builds update from this repository's releases, signed with
the same key as the game's.

Test builds and nightlies are on their own channels, as in the game: set
the channel in Settings > Network Setup > Updates, or get one from Releases
(marked Pre-release). A test build starts on the testing channel.
[docs/releases.md](docs/releases.md) has how the releases are made.

## The Steam Link

The Steam Link port is JizzyRivers' work
([JizzyRivers/chupathingyce-steamlink](https://github.com/JizzyRivers/chupathingyce-steamlink)).
The game's side of it is already in Chupathingy. It moves here next, with
its history, and builds in this repository's CI with Valve's
[Steam Link SDK](https://github.com/ValveSoftware/steamlink-sdk), which CI
downloads. Until then, get it from JizzyRivers' repository.

Later: 32-bit Android, older ARM boards, and JackT's Legacy PC port.

## Building it yourself

Clone with the game:

```sh
git clone --recursive https://github.com/ChupathingyCE/chupathingy32.git
cd chupathingy32
```

(In a clone you already have: `git submodule update --init`.)

The 32-bit builds are the game's own `ninja windows` and `ninja linux`. You
need what the game needs for them: see its
[docs/building.md](https://github.com/ChupathingyCE/chupathingyce/blob/main/docs/building.md)
and [port/windows/README.md](https://github.com/ChupathingyCE/chupathingyce/blob/main/port/windows/README.md).
Then:

```sh
python3 tools/c32_build.py linux release      # on Linux: dist/chupathingyce-linux-release
python tools/c32_build.py windows release     # on Windows: dist/chupathingyce-windows-release
```

`tools/c32_build.py` runs the game's `tools/ci_build.py` in the submodule
and points the updater at this repository's releases. A build of your own
is a `-dev` build and never looks for updates.

Changes to the game itself go to
[ChupathingyCE/chupathingyce](https://github.com/ChupathingyCE/chupathingyce)
([CONTRIBUTING.md](CONTRIBUTING.md)).

## Generative AI

The decompilation this project is built on, and the port it began as a fork of, were made with heavy use of generative AI. Chupathingy has its own code and releases now, but a lot of that earlier work is still in it.

We use AI tools the way developers use any other tool. A person decides what to build, reviews every change, tests it, and is responsible for it. Nothing is handed to an AI to build from start to finish without a person involved. We're also working through the code we inherited to clean up what reads as machine-written: comments that only repeat the code, unclear names, and changes nobody can explain.

If you contribute, the same applies to you: see the game's [CONTRIBUTING](https://github.com/ChupathingyCE/chupathingyce/blob/main/CONTRIBUTING.md#using-ai-tools).

## License

Chupathingy32 is free software under the GNU General Public License,
version 3 or later ([LICENSE](LICENSE)). It comes with no warranty. The game
(the `chupathingyce` submodule) is under its own repository's license, with
its third-party code under theirs.

The license covers Chupathingy's code only. It gives no rights in Halo or
anything else Microsoft owns.

## Credits

- The game: [Chupathingy](https://github.com/ChupathingyCE/chupathingyce)
  and its contributors.
- [JizzyRivers](https://github.com/JizzyRivers): the Steam Link port, and
  the game's ARM, OpenGL ES 2 and older-hardware hooks it builds on.

## Support

Chupathingy is free and always will be. Support through
[Ko-fi](https://ko-fi.com/milenko) or [Patreon](https://www.patreon.com/c/chupathingy)
goes to running the site and the servers.

## Links

- The game: [ChupathingyCE/chupathingyce](https://github.com/ChupathingyCE/chupathingyce)
- Games online now: [stats.chupathingy.org](https://stats.chupathingy.org)
- Discord: [discord.gg/chupathingy](https://discord.gg/chupathingy)

Chupathingy32 is an unofficial fan project. It isn't affiliated with or
endorsed by Microsoft, Xbox Game Studios, Bungie or Halo Studios. Halo is a
trademark of Microsoft. No game files are included: you bring your own copy.
