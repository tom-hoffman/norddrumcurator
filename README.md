Nord Drum Curator
=================

This is a personal project to write a GTK3 app in Python to manage the Nord Drum 1 memory and a library of drum programs.  It is a personal project in the sense that I don't really plan on packaging for Linux, let alone Windows or OS X, but who knows what the future might bring.

![Early development screenshot.](https://raw.githubusercontent.com/tom-hoffman/norddrumcurator/master/nd-curator.png)

The original, somewhat short lived, Nord Drum 1 has no utilities for managing drum programs, unlike the subsequent Nord Drum 2 and 3p.

Currently I'm only worring about the Nord Drum 1, because that's the one I got.  Adding support for the 2 or 3p should not be hard.

The basic model for the interface is a double paned window, where the left pane has a list of the 99 memory positions of my ND1, and the right pane has a tree view of all the programs I have saved to the computer.

My intention is to be able to rearrange the programs in memory on the left pane and then upload the changes to the ND1 in as automatic a process as possible.

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


