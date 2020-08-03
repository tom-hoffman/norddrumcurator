import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import mido

import window
from model import *
import functions
import constants


class NordDrum1Manager(Gtk.Application):
    '''I don't entirely understand this.'''
    def __init__(self):
        try:
            self.root = functions.load()
            self.root.cache_status = list(map(self.resetStatus,
                                         self.root.cache_status))
        except FileNotFoundError:
            # Note that the memory list has an extra value at index 0.
            self.root = DataRoot({0 : UNKNOWN_PLEASURES},
                                 [0] * 100,
                                 ["unknown"] * 100,
                                 0)
        self.port = mido.open_ioport(functions.getMidiPort())
        Gtk.Application.__init__(self)

    def resetStatus(self, s):
        if s == "checked":
            return "unknown"
        else:
            return s

    def do_activate(self):
        mWin = window.MemoryWindow(self)
        mWin.show_all()
        
    def do_startup(self):
        Gtk.Application.do_startup(self)
            
app = NordDrum1Manager()
exit_status = app.run(sys.argv)
sys.exit(exit_status)