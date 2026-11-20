<h1 align="center">Chupathingy32</h1>

<p align="center"><b>Chupathingy for 32-bit and older hardware.</b></p>

<p align="center">
<a href="https://github.com/ChupathingyCE/chupathingy32/releases">Releases</a> ·
<a href="docs/install.md">Install</a> ·
<a href="docs/troubleshooting.md">Help</a> ·
<a href="https://github.com/ChupathingyCE/chupathingyce">The game</a> ·
<a href="https://chupathingy.org">chupathingy.org</a>
</p>

Chupathingy is a 64-bit game now. Chupathingy32 is where it keeps running
on everything older: 32-bit Windows, 32-bit Linux and the 2015 Steam Link.

It's the same game, from the same code. This repository holds the game as
the `chupathingyce` submodule and builds it for these machines. Each
release ships the same game commit as the matching Chupathingy release, and
plays online with every other Chupathingy build: PCs, Macs, phones and
consoles.

You need your own copy of Halo: Combat Evolved. No game files are included.

**Status: in testing.** The first release is planned alongside Chupathingy 0.9.2.

## Which build?

| Machine | Download | Notes |
| --- | --- | --- |
| Windows, 32-bit (x86) | `chupathingyce-windows-release.zip` | Windows 10 or later. |
| Linux, 32-bit (x86) | `chupathingyce-linux-release.zip` | glibc 2.31 or later (32-bit). Brings its own SDL3. |
| Steam Link (2015) | `chupathingyce.tgz` | Test builds only for now. See [docs/steam-link.md](docs/steam-link.md). |

On a 64-bit PC or a Mac, get
[Chupathingy's own builds](https://github.com/ChupathingyCE/chupathingyce/releases/latest)
instead. They run better. The 32-bit Windows build offers the 64-bit one
when it starts on 64-bit Windows.

Every build needs graphics with OpenGL 3.3 or later. The Steam Link has
its own OpenGL ES 2 path.

## Install

1. Download the zip for your machine from
   [Releases](https://github.com/ChupathingyCE/chupathingy32/releases) and
   unzip it into a folder of its own, one you can write to.
2. Start `chupathingy.exe` on Windows, or `chupathingy` on Linux.
3. The first time, pick your Halo disc image. The game copies the maps out
   of it.

[docs/install.md](docs/install.md) has each platform step by step, where
your files go, updates and settings.

## Updates

The game checks for a new version when it starts and asks before it
updates. Chupathingy32's builds update from this repository's releases,
signed with the same keys as the game's. Test builds and nightlies have
their own channels, as in the game.

## Documentation

- [Install and play](docs/install.md): each platform, your maps, updates, `config.toml`
- [The Steam Link](docs/steam-link.md): the USB stick, button combos, performance mode
- [Help](docs/troubleshooting.md): known limits, common problems, reporting a bug
- [Building it yourself](docs/building.md): Windows, Linux and the Steam Link
- [How releases are made](docs/releases.md): versions, files, signing

The game's own [docs](https://github.com/ChupathingyCE/chupathingyce/tree/main/docs)
cover everything else: online play, maps, modes and settings.

## Contributing

Most changes belong in the game itself. [CONTRIBUTING.md](CONTRIBUTING.md)
says what goes where.

## Generative AI

The decompilation this project is built on, and the port it began as a fork of, were made with heavy use of generative AI. Chupathingy has its own code and releases now, but a lot of that earlier work is still in it.

We use AI tools the way developers use any other tool. A person decides what to build, reviews every change, tests it, and is responsible for it. Nothing is handed to an AI to build from start to finish without a person involved. We're also working through the code we inherited to clean up what reads as machine-written: comments that only repeat the code, unclear names, and changes nobody can explain.

If you contribute, the same applies to you: see the game's [CONTRIBUTING](https://github.com/ChupathingyCE/chupathingyce/blob/main/CONTRIBUTING.md#using-ai-tools).

## Credits

- [JizzyRivers](https://github.com/JizzyRivers): the Steam Link port
  (`port/steamlink`, with its history), and the game's ARM, OpenGL ES 2 and
  older-hardware hooks it builds on. Thank you.
- The game: [Chupathingy](https://github.com/ChupathingyCE/chupathingyce)
  and its contributors.
- Valve's [Steam Link SDK](https://github.com/ValveSoftware/steamlink-sdk),
  which the Steam Link build downloads. It isn't part of this repository.
- The Khronos Group's OpenGL ES headers (`port/steamlink/include`, MIT and
  Apache-2.0).
- Mozilla's certificate list, as packaged by curl
  (`port/steamlink/app/ca-certificates.crt`).

## License

Chupathingy32 is free software under the GNU General Public License,
version 3 or later ([LICENSE](LICENSE)). It comes with no warranty. The game
(the `chupathingyce` submodule) is under its own repository's license, and
its third-party code under theirs. Every download carries the licenses it
needs.

The license covers Chupathingy's code only. It gives no rights in Halo or
anything else Microsoft owns.

## Support

Chupathingy is free and always will be. Support through
[Ko-fi](https://ko-fi.com/milenko) or [Patreon](https://www.patreon.com/c/chupathingy)
goes to running the site and the servers. To support a specific developer
or port, ask them directly.

## Links

- The game: [ChupathingyCE/chupathingyce](https://github.com/ChupathingyCE/chupathingyce)
- Games online now: [stats.chupathingy.org](https://stats.chupathingy.org)
- Discord: [discord.gg/chupathingy](https://discord.gg/chupathingy)

Chupathingy32 is an unofficial fan project. It isn't affiliated with or
endorsed by Microsoft, Xbox Game Studios, Bungie, Halo Studios or Valve.
Halo is a trademark of Microsoft. Steam Link is a trademark of Valve. No
game files are included: you bring your own copy.
