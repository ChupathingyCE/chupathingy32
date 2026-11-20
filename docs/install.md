# Install and play

Chupathingy32 is the game's own 32-bit Windows and Linux builds, and the
Steam Link build. Once it's running, it's the same game as every other
Chupathingy build, so the game's
[docs](https://github.com/ChupathingyCE/chupathingyce/tree/main/docs) apply
to it too.

## Before you start

- **Your own copy of Halo: Combat Evolved.** An Xbox disc image (`.iso` or
  `.xiso`), any region. The game copies the maps out of it the first time
  it starts. It also takes the Halo PC disc and the Custom Edition
  installer: see the game's
  [maps guide](https://github.com/ChupathingyCE/chupathingyce/blob/main/docs/maps.md#importing-at-first-start).
- **Graphics with OpenGL 3.3 or later** on Windows and Linux.
- **A 64-bit PC?** Use the game's own
  [64-bit builds](https://github.com/ChupathingyCE/chupathingyce/releases/latest)
  instead. They run better, and they have the Vulkan renderer.

## Windows (32-bit)

You need Windows 10 or later.

1. Download `chupathingyce-windows-release.zip` from
   [Releases](https://github.com/ChupathingyCE/chupathingy32/releases).
2. Unzip it into a folder you can write to, such as
   `Documents\Chupathingy32`. Not `Program Files`.
3. Start `chupathingy.exe`. The builds aren't code signed yet, so if
   Windows warns about an unknown publisher, choose **More info**, then
   **Run anyway**.
4. Pick your Xbox disc image.

On 64-bit Windows, the game offers the 64-bit build once. Turn that off
with `offer_64bit = false` in the `[update]` section of `config.toml`.

## Linux (32-bit)

You need glibc 2.31 or later, 32-bit (Debian 11, Ubuntu 20.04 or newer).
The zip brings its own SDL3.

1. Download `chupathingyce-linux-release.zip` from
   [Releases](https://github.com/ChupathingyCE/chupathingy32/releases).
2. Unzip it into a folder of its own.
3. Start `chupathingy` in that folder.
4. Pick your Xbox disc image.

To put it in your application menu, run `sh desktop-entry.sh` in the same
folder. It adds a Chupathingy32 entry with its icon for that folder. Run it
again if you move the folder, or run `sh desktop-entry.sh remove` to take
the entry out.

On a 64-bit system that can run 32-bit programs, the game needs the 32-bit
OpenGL, sound and X11 libraries. The game's
[Linux notes](https://github.com/ChupathingyCE/chupathingyce/blob/main/port/linux/README.md)
list them for Debian, Ubuntu and Arch Linux. On such a system the 64-bit
build is the better choice anyway.

## The Steam Link

The 2015 Steam Link installs the game from a USB stick, and the stick holds
your maps and saves. See [steam-link.md](steam-link.md).

## Where your files go

The 32-bit builds use the same places as the game's 64-bit builds, so you
can switch between them and keep your saves and settings.

| Platform | Maps, settings and logs | Saves |
| --- | --- | --- |
| Windows | next to `chupathingy.exe` | `%APPDATA%\ChupathingyCE` |
| Linux | next to the `chupathingy` program | `~/.local/share/chupathingyce` |
| Steam Link | `chupathingyce/` on the USB stick | `chupathingyce/save/` on the stick |

On Windows and Linux, the setup screen shows each folder: hold **Shift**
(or **Back** on a controller) while the game starts, go to **SETTINGS** and
open the **PATHS** tab.

## Updates

The game checks for a new version when it starts and asks before it
updates. The 32-bit builds update from
[Chupathingy32's releases](https://github.com/ChupathingyCE/chupathingy32/releases).
The one thing they take from the game's releases is the 64-bit build that
32-bit Windows offers on a 64-bit PC. Each update is signed, and the game
checks it before it installs anything.

The update channel picks which builds you get:

| Channel | Gets |
| --- | --- |
| `release` (the default) | releases |
| `testing` | test builds and releases |
| `nightly` | nightlies, test builds and releases |

Set it on the setup screen's **UPDATES** tab, or as `channel` in the
`[update]` section of `config.toml`. A test build or a nightly starts on its
own channel. The game never offers a build older than yours.

Builds you make yourself never look for updates.

## Settings

Most settings are in the game's menus. Everything else is in `config.toml`,
which the game writes the first time it starts, every setting commented out
at its default. It's next to the game on Windows and Linux, and in
`chupathingyce/` on the Steam Link's stick. The game's
[settings guide](https://github.com/ChupathingyCE/chupathingyce/blob/main/docs/settings.md)
explains how to edit it and what the settings do.

On an older PC, these help the most:

- **PERFORMANCE** at **POTATO** in the display settings (`tuning.preset =
  "potato"` in `config.toml`) turns the heaviest drawing down.
- **LIGHT EFFECTS** at **LOW** or **OFF**.
- A smaller window: `display.window_scale` in `config.toml`.
