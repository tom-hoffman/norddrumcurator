Nord Drum Curator
=================

To be clear, this project does not yet work.

The original, somewhat short lived, Nord Drum 1 has no utilities for managing drum programs, unlike the subsequent Nord Drum 2 and 3p.

The Nord Drum 1 memory holds 99 programs in a single bank.

This is a personal project to write a GTK3 app in Python to manage the Nord Drum 1 memory and a library of drum programs.  It is a personal project in the sense that I don't really plan on packaging for Linux, let alone Windows or OS X, but who knows what the future might bring.

Currently I'm only worring about the Nord Drum 1, because that's the one I got.  Adding support for the 2 or 3p should not be hard.

The basic model for the interface is a double paned window, where the left pane has a list of the 99 memory positions of my ND1, and the right pane has a tree view of all the programs I have saved to the computer.

My intention is to be able to rearrange the programs in memory on the left pane and then upload the changes to the ND1 in as automatic a process as possible.

This will all be managed via SYSEX messages to and from the ND1.  Unfortunately the actual binary format used by the ND1 does some kind of tricky checksumming that hasn't been reverse engineered completely, so this all isn't as clever or powerful as it could be.

To start with the interactive GTK debugger:

``GTK_DEBUG=interactive python3 run.py``


