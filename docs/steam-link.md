# The Steam Link

Chupathingy runs natively on the original Steam Link, the small box Valve
sold from 2015. It isn't streamed: the game runs on the box. The port is
[JizzyRivers'](https://github.com/JizzyRivers/chupathingyce-steamlink) work,
and it lives here now with its history.

It's a test build. Campaign plays, the menus are all there, and you can
join online games. It's slow: about 23 frames a second at Blood Gulch's
spawn with performance mode on, less in heavier levels.

## Getting the build

Until a Chupathingy32 release carries it, the Steam Link build comes from
this repository's [Steam Link workflow](../.github/workflows/steamlink.yml)
on Actions. Each run keeps `c32-steamlink` for 7 days (you need to be
signed in to GitHub to download it), which holds:

- `chupathingyce.tgz`: the app, for the USB stick.
- `chupathingyce-steamlink-release.zip`: the same files for the updater.

## What you need

- An original Steam Link. Developer mode and SSH don't matter.
- A USB stick of 8 GB or more. FAT32 is fine. The disc image and what the
  game makes from it come to about 7.5 GB.
- Your Halo: Combat Evolved Xbox disc image, `.iso` or `.xiso`. FAT32 can't
  hold a file over 4 GB, so trim a bigger image to an `.xiso` first.
- A controller the box sees. A wired Xbox 360 controller is the one tested.

## Install

1. On the stick, make the folders `steamlink/apps/` and put
   `chupathingyce.tgz` in it.
2. Put your disc image on the root of the stick, not in a folder.
3. Optional, for Custom Edition maps: put Halo Custom Edition's installer
   (`.exe`) on the root of the stick too.
4. Plug the stick into the Steam Link and power cycle it. It installs the
   app when it starts.
5. Start **Chupathingy** from the box's apps.

The first start copies your maps to the stick (about 14 minutes), then
Custom Edition's if you added its installer (about 3 minutes), then builds
its cache (about 3 more). A ring fills while it works. It only happens
once.

Leave the stick in. Your maps, saves, settings and logs all live on it, in
`chupathingyce/`, because the box itself doesn't have the room. Don't pull
the stick while the game is running.

If you plug in a stick with a newer `chupathingyce.tgz` later, the game
installs it the next time it starts.

## Updates

When a new version is out, the game asks when it starts: **A** updates,
**B** is not now, and **Y** stops asking. The box updates from
Chupathingy32's releases once they carry the Steam Link file
(`chupathingyce-steamlink-release.zip`), signed with the game's keys.

Boxes on JizzyRivers' earlier builds (0.9.1a and before) update from his
server until his last release there moves them here.

## Button combos

Hold **Back** and press:

| Combo | Key | Does |
| --- | --- | --- |
| Back + d-pad down | F9 | Performance mode on or off |
| Back + d-pad up | F8 | The frame rate counter |
| Back + d-pad left | F7 | System info: free memory and uptime |
| Back + d-pad right | F6 | A screenshot, to `chupathingyce/screenshots/` on the stick |
| Back + left stick click | F5 | A line from the Xbox scene days |
| Back + Start + both triggers | | Back to the Steam Link's menu |

## Performance mode

Performance mode is on by default. It leaves out what the box can't afford:
decals, dynamic lights, reflections, specular and lens flares. It draws
fewer lines and scales them up, and switches models to less detail sooner.
In play it also leaves out the sky and the HUD's frames and fogs out the
distance. Cutscenes and the main menu keep those.

In network games it keeps everything that could be cover: see-through
parts and plants are drawn as usual, so you can't see through what other
players hide behind. `display.performance_online_cuts = true` drops them
online too.

The settings, in `chupathingyce/config.toml` on the stick:

| Setting | Default | What it does |
| --- | --- | --- |
| `display.performance_mode` | `true` | Performance mode when the game starts |
| `display.performance_lines` | `240` | The lines drawn, scaled up to the screen |
| `display.performance_view_distance` | `60.0` | How far you see before the fog |
| `display.performance_model_detail` | `0.5` | How soon models switch to less detail |
| `display.performance_online_cuts` | `false` | Leave out see-through parts and plants online too |

## Known limits

- About 23 frames a second on open maps, less on heavy ones.
- No Delta Guide, no screenshots or clips of the desktop kind (use Back +
  d-pad right), and no medal icons.
- 256 MB of memory: the box uses the Xbox's texture cache size.

## When something breaks

Take `chupathingyce/run.log` off the stick and attach it to your report.
See [troubleshooting.md](troubleshooting.md#reporting-a-bug).
