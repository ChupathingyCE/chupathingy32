# ChupathingyCE for 32-bit Android

For Android devices whose system is 32-bit only (armeabi-v7a), which the upstream app's native
64-bit build (arm64-v8a) cannot run on: cheap Android TV boxes (an Amlogic S905W2 has 64-bit cores
and a 32-bit Android), many Fire TV sticks and boxes with Fire OS, old tablets, and smart displays
such as an Echo Show 5 with LineageOS. Android 9 (API 28) or later, OpenGL ES 3.0 or later (the
renderer uses 3.2 where the driver has it).

Tested: Amlogic S905W2 (Mali-G31, ES 3.2): Blood Gulch at about 40 fps; Echo Show 5 on LineageOS
18.1 (Mali-T720, ES 3.1, 1 GB): about 30 fps. The Fire TV Stick 4K Select is not Android (Vega OS).

## Install

1. `adb install chupathingyce-android32-<version>.apk` (a build from `package.py`, below).
2. Start "Chupathingy 32". With no game data it shows a setup screen (large buttons, a remote's d-pad
   reaches them): **Choose a disc image** (an Xbox disc image of Halo, .iso or .xiso, copied out by
   `XisoExtractor`, upstream's reader) or **Choose a folder with the maps** (the Xbox's maps, with
   `ui.map`, from a computer or a USB drive; copied `ui.map` first and then the smallest maps first as far
   as the free space goes, so a device with 1.5 GB left still gets the multiplayer maps). Both use the
   system's file picker, which opens in Downloads. A box with no file picker (the S905W2 has none) lists any
   disc image (.iso, .xiso) it finds in the app's own folder (`.../files/`, and the same on a USB drive), as
   a button: copy one there (adb, a file manager) and press "check again". The whole set with the movies is
   2.4 GB. Or copy the maps by hand, which the screen also says:
   `adb push maps /sdcard/Android/data/dev.horrible.chupathingyce32/files/`, then "check again".
   Custom Edition's maps are optional: put Halo PC's installer (`halocesetup_en_1.00.exe`) in the same
   folder and the next start reads it with the game's own importer into `maps_ce` (about a minute, a toast
   says so; 418 MB).
3. A gamepad works as on the desktop. A device with a touchscreen gets the on-screen controls (the
   64-bit app's overlay, shared). The first start makes the game's caches, which takes a while.

An app is updated only by a build signed with the key it was installed with: a release build is signed
with ChupathingyCE's key from `app/keystore.properties` (storeFile, storePassword, keyAlias, keyPassword;
never committed), and is unsigned without it. A debug build (signed with the computer's debug key) has to
be uninstalled before a release one goes on, which deletes the app's files folder: keep the maps.

## Build

Needs the Android SDK with an NDK (r27), JDK 17, LLVM, ninja and cmake, with `ANDROID_HOME` and
`JAVA_HOME` set, SDL3 built for armeabi-v7a in `build/android32/sdl3-build` (cmake with the NDK's
toolchain file; the source in `build/android32/SDL3`, release-3.4.16), and the game's submodule at a
commit that has the game's `HALO_ANDROID32` hooks.

    cd chupathingyce
    python configure.py --release --console-port ../port/android32
    ninja android32                         # libmain.so
    python ../port/android32/stage.py       # the libraries the app packs
    cd ../port/android32/app && ./gradlew assembleDebug

    python port/android32/package.py        # the release APK, in build/android32/release/

## How it is put together

The Java is the 64-bit app's (`chupathingyce/port/android/app/src/main/java`, `HaloActivity` with its `:game`
process, the touch overlay, the gyro aim, the map importer, `XisoExtractor`): `app/app/build.gradle` copies
it without that app's `LauncherActivity`, which `app/app/src/main/java/com/halo/decomp/LauncherActivity.java`
replaces with this build's setup screen. The touch bridge is the game's own `host_touch.c`. A build of your
own is a `-dev` build and never looks for updates.

### How it differs from the Steam Link port

The game is the same 32-bit Linux platform layer, with the NDK's clang and bionic and the renderer's
ES path calling the driver directly (no GLES 2 layer). `src/android32_align.c` emulates the
instructions a 64-bit kernel will not run unaligned for a 32-bit program (the Steam Link's 3.8
kernel did it for the game); `src/android32_setup.c` and `android32_steam.c` stand in for the
desktop's start-up and Steam calls; `src/android32_touch.c` compiles the game's `host_touch.c`. The game's
side is the `HALO_ANDROID32` hooks in the game repository.
