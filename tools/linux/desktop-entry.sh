#!/bin/sh
# SPDX-FileCopyrightText: 2026 The Chupathingy contributors
# SPDX-FileCopyrightText: 2026 Milenko x Horrible Dev
# SPDX-License-Identifier: GPL-3.0-or-later
#
# Adds Chupathingy32 to your desktop's application menu, for the folder this
# script is in. Run it again if you move the folder.
#
#   sh desktop-entry.sh           add the menu entry
#   sh desktop-entry.sh remove    take it out again
set -e
here=$(cd "$(dirname "$0")" && pwd)
data=${XDG_DATA_HOME:-$HOME/.local/share}
entry=$data/applications/chupathingy32.desktop

if [ "$1" = remove ]; then
	rm -f "$entry"
	for size in 16 24 32 48 64 128 256; do
		rm -f "$data/icons/hicolor/${size}x${size}/apps/chupathingy32.png"
	done
	echo "Removed the Chupathingy32 menu entry."
	exit 0
fi

if [ ! -x "$here/chupathingy" ]; then
	echo "chupathingy isn't next to this script. Run it from the unzipped folder." >&2
	exit 1
fi
for size in 16 24 32 48 64 128 256; do
	if [ -f "$here/chupathingy32-$size.png" ]; then
		mkdir -p "$data/icons/hicolor/${size}x${size}/apps"
		cp "$here/chupathingy32-$size.png" "$data/icons/hicolor/${size}x${size}/apps/chupathingy32.png"
	fi
done
mkdir -p "$data/applications"
# (Exec and Path quoted as the desktop entry spec asks, for a folder with
# spaces in its name)
cat > "$entry" <<ENTRY
[Desktop Entry]
Type=Application
Name=Chupathingy32
Comment=Chupathingy for 32-bit and older PCs
Exec="$here/chupathingy"
Path=$here
Icon=chupathingy32
Categories=Game;ActionGame;
Terminal=false
StartupWMClass=chupathingy
ENTRY
command -v update-desktop-database > /dev/null 2>&1 && update-desktop-database "$data/applications" 2> /dev/null || true
echo "Added Chupathingy32 to your application menu."
