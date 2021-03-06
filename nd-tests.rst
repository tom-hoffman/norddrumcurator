``nd-man`` Nord Drum Manager DocTest file
=========================================

Test setup
----------

GENERATE TEST DATA NEEDS UNKNOWN PLEASURES AT BEGINNING.

    >>> from model import *
    >>> from ndTestSetup import *
    
Generating test data
--------------------

    >>> tp = generateTestPrograms(30)
    >>> print(len(tp))
    31
    >>> fp = tp[1]
    >>> print(fp)
    NDProg: Test Program 1 with 4 channels.
    >>> print(fp.channels)
    [Test Channel 1: kick., Test Channel 2: snare., Test Channel 3: rack tom., Test Channel 4: floor tom.]

    >>> lp = tp[30]
    >>> print(lp)
    NDProg: Test Program 30 with 4 channels.
    >>> print(lp.channels)
    [Test Channel 117: kick., Test Channel 118: snare., Test Channel 119: rack tom., Test Channel 120: floor tom.]
    
    >>> tdr = generateTestData(30)
    >>> print(tdr)
    DataRoot has 31 programs on disc and 30 in memory.

Saving & loading
----------------

A reference for implementing this in the main code later.

    >>> import tempfile
    >>> import pickle
    >>> t = tempfile.TemporaryFile()
    >>> t.write(pickle.dumps(tdr)) # output not significant
    7534
    >>> t.seek(0) 
    0
    >>> loaded = pickle.load(t) 
    >>> print(loaded)
    DataRoot has 31 programs on disc and 30 in memory.
    >>> t.close()

Populating the memory tree store
--------------------------------

    >>> from window import *
    >>> populateFilesTreeStore(tdr.memory, tdr.programs) #doctest: +ELLIPSIS
    <Gtk.TreeStore object at ... (GtkTreeStore at ...)>

Midi tests
----------

These are interactive and may need to be checked on the ND.

    >>> import mido
    >>> import functions
    >>> port = mido.open_ioport(functions.getMidiPort())
    
    >>> print(port) #doctest: +ELLIPSIS
    <open I/O port ...>

Check to see if the ND switches to channel 25.

    >>> functions.sendMidiProgramChange(port, 25)

Listen/watch for confirmation from ND.

    >>> functions.midiConfirm(port)
    

