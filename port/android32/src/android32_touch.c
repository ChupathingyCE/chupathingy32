/*
ANDROID32_TOUCH.C

The on-screen touch controls' bridge between the overlay (TouchControls.java, shared with the 64-bit app)
and the game: the game's own port/android/host/host_touch.c, compiled here as it is (the 64-bit build links
the same file), so that the two cannot drift. Its Java_com_halo_decomp_* names are the shared overlay's.
host.h, which it includes for the 64-bit host's logging, is satisfied by android32_main.c's host_logf.
*/

#include "../../../chupathingyce/port/android/host/host_touch.c"
