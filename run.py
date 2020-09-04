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
    def __init__(self):
        try:
            self.root = functions.load()
            self.root.cache_status = list(map(self.resetStatus,
                                         self.root.cache_status))
        except FileNotFoundError:
            self.root = DataRoot()
            self.root.load_factory_soundbank()
        self.port = mido.open_ioport(functions.getMidiPort())
        Gtk.Application.__init__(self)
            
    def resetStatus(self, s):
        if s == "checked":
            return "unknown"
        else:
            return s

    def do_activate(self):
        self.win = window.AppWindow(self)
        self.win.connect("destroy", self.cleanup)
        self.win.show_all()
        
    def cleanup(self, menu = None):
        self.port.close()
        
    def do_startup(self):
        Gtk.Application.do_startup(self)
            
app = NordDrum1Manager()
exit_status = app.run(sys.argv)
sys.exit(exit_status)