/*
ANDROID32_SETUP.C

The start-up screens a console port supplies (HALO_CONSOLE_SETUP_SCREENS,
halo_console_features.h), which turns the desktop launcher off: Android has
no install screens yet. The game data is put in the app's external files
folder by hand (adb, or a file manager); without it src/android32_main.c
shows a message and quits. The updater asks nothing: this port has no
release of its own to update from yet.
*/

#include "platform.h"
#include "sdl_platform.h"
#include "ce_installer.h"

#include <SDL3/SDL.h>
#include <dirent.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

void console_setup_start(void)
{
}

/* ---------- Custom Edition's maps, optional

Halo PC's Custom Edition installer (halocesetup_en_1.00.exe) in the app's files folder is read by the game's own
importer (ce_installer.c, as the desktop ports and the Steam Link's setup do) and its maps written to maps_ce
there: the resource maps (bitmaps.map, sounds.map, loc.map) that Custom Edition's maps and the community's are read
with. The game itself runs on the Xbox's maps alone. A toast says what is happening, as there is no window yet. */

static void toast(const char *text)
{
	SDL_ShowAndroidToast(text, 1, -1, 0, 0);
}

/* a file in folder that is Custom Edition's installer: a big .exe the importer recognises */
static BOOL find_installer(const char *folder, char *found, int size)
{
	DIR *directory = opendir(folder);
	struct dirent *entry;
	BOOL result = FALSE;

	if (!directory)
		return FALSE;
	while (!result && (entry = readdir(directory)) != NULL)
	{
		const char *dot = strrchr(entry->d_name, '.');
		SDL_PathInfo information;
		char path[1100];

		if (!dot || SDL_strcasecmp(dot, ".exe"))
			continue;
		snprintf(path, sizeof(path), "%s/%s", folder, entry->d_name);
		if (SDL_GetPathInfo(path, &information) && information.size > (50u << 20) && ce_installer_is_installer(path))
		{
			snprintf(found, (size_t)size, "%s", path);
			result = TRUE;
		}
	}
	closedir(directory);
	return result;
}

static void offer_custom_edition(const char *data_root)
{
	char path[1100], installer[1100], error[256] = "", file[256], text[320];
	BOOL succeeded = FALSE;
	unsigned long long done = 0, total = 0;
	Uint64 last_toast = 0;

	snprintf(path, sizeof(path), "%s/maps_ce/bitmaps.map", data_root);
	if (!access(path, F_OK) || !find_installer(data_root, installer, sizeof(installer)))
		return;
	platform_log("importing Custom Edition's maps from %s to %s", installer, data_root);
	toast("Importing Custom Edition's maps: about a minute...");
	if (!platform_import_start(PLATFORM_IMPORT_CE_INSTALLER, installer, data_root, error, sizeof(error)))
	{
		platform_log("Custom Edition's maps could not be copied from its installer: %s", error);
		toast("Custom Edition's installer could not be read.");
		return;
	}
	for (;;)
	{
		BOOL finished;

		file[0] = '\0';
		finished = platform_import_poll(file, sizeof(file), &done, &total, &succeeded, error, sizeof(error));
		if (SDL_GetTicks() - last_toast > 8000)
		{
			snprintf(text, sizeof(text), "Custom Edition: %s (%llu of %llu MB)", file, done >> 20, total >> 20);
			toast(text);
			last_toast = SDL_GetTicks();
		}
		if (finished)
			break;
		SDL_Delay(50);
	}
	if (succeeded)
	{
		platform_log("imported %llu MB of maps into %s/maps_ce", done >> 20, data_root);
		toast("Custom Edition's maps are in.");
	}
	else
	{
		platform_log("Custom Edition's maps could not be copied from its installer: %s", error);
		toast("Custom Edition's maps could not be copied.");
	}
}

void console_setup_after_data(const char *data_root)
{
	offer_custom_edition(data_root);
}

BOOL platform_offer_game_data(char *destination, unsigned long size)
{
	(void)destination;
	(void)size;
	return FALSE;
}

void *console_setup_screen_open(void)
{
	return NULL;
}

void console_setup_screen_progress(void *screen, float fraction, const char *title, const char *line)
{
	(void)screen;
	(void)fraction;
	(void)title;
	(void)line;
}

void console_setup_screen_close(void *screen)
{
	(void)screen;
}

void console_setup_notice(const char *first, const char *second)
{
	platform_log("%s %s", first ? first : "", second ? second : "");
}

int console_setup_update_question(const char *latest, const char *current)
{
	(void)latest;
	(void)current;
	return 0;
}

/* the test script's pointer events (xinput_sdl.c) act on the desktop's mouse pointer, which the touch
build's menus do not have (sdl_platform.c's touch section): nothing to do */
void platform_test_pointer_event(float x, float y, int button, int wheel)
{
	(void)x;
	(void)y;
	(void)button;
	(void)wheel;
}
