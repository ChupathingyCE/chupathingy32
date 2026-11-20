# Contributing to Chupathingy32

Chupathingy32 builds Chupathingy for 32-bit and older hardware. The game,
with everything the platforms share, is
[ChupathingyCE/chupathingyce](https://github.com/ChupathingyCE/chupathingyce),
pinned here as the `chupathingyce` submodule.

## Where a change goes

- **Here:** the build and release workflows, `tools/`, the icon
  (`art/icon/`), and the code a target needs that no other build does:
  the Steam Link's, under `port/steamlink/`.
- **The game:** everything else, including the hooks older hardware uses
  (the `HALO_CONSOLE_*` capabilities, the OpenGL ES path, the updater). A
  change there must leave the other builds as they are. Once it's merged, a
  pull request here moves the submodule to it. The Game bump workflow opens
  that pull request every night.

Never commit, attach or link game data (maps, sounds, movies, disc images)
or keys.

## Pull requests

- Open them against `ChupathingyCE/chupathingy32`'s `main`.
- One change per pull request, with how you tested it: which machine and
  which build.
- The Build check passes for both targets, and the Steam Link check for
  changes under `port/steamlink/`.
- Contributions are under the GNU GPL, version 3 or later, like the rest
  of the repository.

[docs/building.md](docs/building.md) has how to build each target.

Contributors are credited in the release notes. The game's
[CONTRIBUTING.md](https://github.com/ChupathingyCE/chupathingyce/blob/main/CONTRIBUTING.md)
has the rest, including how we use AI tools.
