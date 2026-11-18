# How Chupathingy32 is released

Chupathingy32 ships the game's own 32-bit Windows and Linux builds, from the
same game commit as the matching Chupathingy release. It has the same three
kinds of builds as the game: releases, test builds and nightlies. All of
them are made by `.github/workflows/release.yml`.

## Versions and tags

A build's version is the game's. Chupathingy32 has no version numbers of
its own.

| Kind | Version | Tag | Shown as |
| --- | --- | --- | --- |
| Release | `0.9.2` | `v0.9.2` | Latest release |
| Test build | `0.9.2-testing.202612201530` | `v0.9.2-testing` (replaced each time) | Pre-release |
| Nightly | `0.9.2-nightly.202612210400` | `nightly` (replaced each time) | Pre-release |

The number after `testing.` or `nightly.` is the time the build was made
(UTC, year to minute). It's the same version grammar the game uses.

- **A release** is a pushed tag `v<VERSION>`, where VERSION is the game's
  `VERSION` file at the submodule's commit. The workflow refuses any other
  tag. On release day the submodule is moved to the commit the game
  released, then the tag is pushed.
- **A test build** is started by hand (Actions, Release, Run workflow,
  kind `testing`). It builds this repository's main as it is.
- **A nightly** builds main with the game moved to the game's main, in the
  run only. It runs every night once the repository variable
  `NIGHTLY_PUBLISH` is `true`, and skips a night when neither main changed.

Test builds and nightlies are never marked latest, so players on the
release channel never see them.

## Files

Each build has the game's own 32-bit names:

| File | What |
| --- | --- |
| `chupathingyce-windows-release.zip` | 32-bit Windows (x86) |
| `chupathingyce-linux-release.zip` | 32-bit Linux (x86) |
| `updates.json`, `updates.json.sig` | The list of update files the game reads, and its signature |
| `*.zip.sig` | Each zip's own signature (releases only, for older builds) |
| `SHA256SUMS` | The zips' SHA-256 |

The names don't say "x86" or "32" on purpose. A 32-bit install's updater
asks for `windows` or `linux`, the game's names for its 32-bit builds, and
the game's signing tool only lists files named
`chupathingyce-<platform>-<release|debug>.zip`. Renaming them would leave
installs in the field without an update. The release notes and this
repository's name say what they are. The Steam Link's will be
`chupathingyce-steamlink-release.zip`.

## Signing

Releases are signed with the game's update key, in the same format, with
the game's own `tools/update_sign.py`. The sign job runs only when the
repository variable `SIGNING` is `true`, in the environment `signing`, with
the secret `UPDATE_SIGNING_KEY`. Those are the same environment and secret
names as the game's release workflow. Until signing is on, a release is
published as a draft, and test builds and nightlies are published unsigned:
they can be downloaded by hand, but no updater installs them.

The game has no prerelease key yet, so test builds and nightlies are signed
with the update key, as the game's are. When the prerelease key is made, the
sign job for them moves to the environment `signing-prerelease` and the
secret `UPDATE_PRERELEASE_KEY`.

## How 32-bit installs get updates

The game's builds look for updates on the game's releases. Chupathingy32's
builds are made with `HALO_UPDATE_REPOSITORY=ChupathingyCE/chupathingy32`,
so their updater looks here instead: the latest release, then its
`updates.json`, then the zip. The testing channel reads the fixed `testing`
pre-release here, and the nightly channel the `nightly` pre-release. The
32-bit Windows build on 64-bit Windows still offers the 64-bit build, from
the game's releases.

`HALO_UPDATE_REPOSITORY` needs the game change in ChupathingyCE/chupathingyce
#1461. A game commit from before it ignores the setting, and its builds look
on the game's releases.

Installs that came from the game's releases (0.9.1a and older) still look
there. The plan for the move: the game's next release carries the 32-bit
zips made here, under the same names. Those builds then look here for every
update after. The game keeps carrying them for a few releases, so nobody
who skips a release is left behind.

## Testers

Test builds go out the same way as the game's: a pre-release, then a post
asking testers to play it and report bugs in #bug-reports first.
