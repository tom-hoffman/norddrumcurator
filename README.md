Nord Drum Curator
=================

This is a personal project to write a GTK3 app in Python to manage the Nord Drum 1 memory and a library of drum programs.  It is a personal project in the sense that I don't really plan on packaging for Linux, let alone Windows or OS X, but who knows what the future might bring.

![Early development screenshot.](https://raw.githubusercontent.com/tom-hoffman/norddrumcurator/master/nd-curator.png)

As of Sept 4, 2020, the code in the "sets" branch is considered alpha quality. That is, there are bugs and quirks, but it is usable to me. You can pull the whole set of programs from a ND1.  You can set the name and other metadata for the programs.  The programs appear where they currently are in the ND memory and are also saved to a library of all programs. You can drag programs from the library into specific slots.  You can push all programs back to the ND.

For example, here's what I'm doing now:

	* Design a base kit I like. I'm a rock drummer, so in this case is is a very ringy and resonant kit sound.
	* Pull that to the app, give it a name and other metadata.
	* Drag copies of the kit to five consecutive memory locations (say 95 - 99).
	* Push the changes to the ND1.
	* Now I can edit 96 - 99 to be different variations on the original kit (shorter decay, different base tones, less noise, etc).
	* Pull those versions back in to the ND, and update the metadata.
	* Now I can switch between those kit variations for different parts of a song, in my case using a footswitch on the Midi Baby 3.
	* If I ever get to the point of doing this in a live set, I can also use the app to sequence the programs for a specific set of songs.

Please note that "Nord" and "Nord Drum" are trademarks of Clavia DMI AB, with whom I have no connection.

The original, somewhat short lived, Nord Drum 1 has no utilities for managing drum programs, unlike the subsequent Nord Drum 2 and 3p. Currently I'm only worring about the Nord Drum 1, because that's the one I got.  Adding support for the 2 or 3p should not be (very) hard, mostly supporting multiple banks and more inputs.

In particular, what I want to do is arrange related sets of programs in adjacent memory locations, so I can use a foot switch to change from, say, one drum program for the verse of a song, to a different one for the chorus, and then back again. I'd also like to be able to easily rearange programs to match a different sequence of songs for live performance.

The basic model for the interface is a double paned window, where the left pane has a list of the 99 memory positions of my ND1, and the right pane has a list of all the programs I have saved to the computer.  My intention is to be able to rearrange the programs in memory on the left pane and then upload the changes to the ND1.

This will all be managed via SYSEX messages to and from the ND1.  Unfortunately the actual binary format used by the ND1 does some kind of tricky checksumming that hasn't been reverse engineered completely.  Without that, we can't actually edit the programs themselves outside the ND1.

Current Status
--------------

As of 8/14/2020, I'm doing a major refactoring now that I have a better 
understanding of how to dump and push all files at once. 

What works:

 * Pulling and saving a program from your Nord Drum.
 * Entering metadata when you pull the program.
 * Dragging and dropping an imported program into a different memory location.
 * Pushing the program to its new location on the Nord Drum.

In short, it is now useful. I'm going to use it like this for a little while and next priorities will come 

TODO:

 * Editing the metadata on existing programs.
 * Prettying up programs pane (Gtk.CellRendererToggle).

Python dependencies
-------------------

 * Python 3
 * mido (Python MIDI library)
 * PyGTK 3.0 
 * crcmod

Non-Python dependencies
-----------------------

 * amidi - Apparently needed to push a complete SysEx file to the ND.


To start with the interactive GTK debugger:

``GTK_DEBUG=interactive python3 run.py``


