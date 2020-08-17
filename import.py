import mido

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import functions
from constants import *
from model import *

class ImportDialog(Gtk.Window):
    def __init__(self,
                 root: DataRoot,
                 port: mido.IOPort):
        Gtk.Window.__init__(self, title = "Import from Nord Drum...")
        self.set_modal(True)
        
        
        
                 