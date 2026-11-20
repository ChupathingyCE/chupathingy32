# Help

Most problems are the game's, not the 32-bit build's, so the game's own
[help page](https://github.com/ChupathingyCE/chupathingyce/blob/main/docs/help.md)
is worth a look too. This page covers what's different here.

## Known limits

- **OpenGL only.** The 32-bit builds have no Vulkan renderer. Your graphics
  need OpenGL 3.3 or later.
- **No AppImage** for 32-bit Linux. Use the zip.
- **Not code signed.** Windows asks before the first start: choose
  **More info**, then **Run anyway**.
- **Older PCs are slow in big levels.** Set **PERFORMANCE** to **POTATO** in
  the display settings ([install.md](install.md#settings) has more).
- **The Steam Link** is a test build with limits of its own:
  [steam-link.md](steam-link.md#known-limits).

## Reporting a bug

Send your logs with every report. They tell us what happened.

On Windows and Linux, while the game is running:

1. Open the Delta Guide (**F3**, or a controller's Guide button) and go to
   **SETTINGS**.
2. Pick **SEND MY LOGS**. It asks first. Pick **SEND**.
3. You get a short code. Pick **COPY** and paste it with your report.

If the game won't start, use the setup screen: hold **Shift** (or **Back**
on a controller) while the game starts, go to **LOGS & HELP** and pick
**SEND MY LOGS**.

The logs go to dump.chupathingy.org. Your computer's account name and
network addresses are taken out before they're sent.

On the Steam Link, take `chupathingyce/run.log` off the USB stick and
attach it instead.

Then post your report in #bug-reports on the
[Discord](https://discord.gg/chupathingy), or open an
[issue here](https://github.com/ChupathingyCE/chupathingy32/issues). Say
that you play Chupathingy32, which build (the version is at the bottom of
the main menu), your system and graphics card, and what you did just before
it went wrong.

A bug that happens on the game's 64-bit builds too belongs to the game:
[its issues](https://github.com/ChupathingyCE/chupathingyce/issues).

## The game won't start on Linux

On a 64-bit system, the 32-bit game needs 32-bit libraries: OpenGL, sound
and X11. The game's
[Linux notes](https://github.com/ChupathingyCE/chupathingyce/blob/main/port/linux/README.md)
list the packages. Start `./chupathingy` from a terminal to see what's
missing. Or use the game's 64-bit build.

## No update is offered

The 32-bit builds look for updates on Chupathingy32's releases, from your
update channel, and only offer builds newer than yours. A build you made
yourself never looks.

Installs from the game's own releases (0.9.1a and older) still look there.
The game's 0.9.2 release is planned to carry the 32-bit builds made here,
and from then on they update from here.

## Windows offers the 64-bit build

On 64-bit Windows, the 32-bit build offers the 64-bit one once. It runs
better there. To keep the 32-bit build, say no, or set
`offer_64bit = false` in the `[update]` section of `config.toml`.
