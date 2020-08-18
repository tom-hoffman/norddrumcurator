import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import functions
from constants import *
from model import * 

class EditProgramDialog(Gtk.Window):
    def __init__(self, prog: NDProg):
        self.prog = prog
        Gtk.Window.__init__(self, title =
                             f"{self.prog.ID}: {self.prog.description}")
        self.set_modal(True)
        # Layout grid with interactive elements.
        grid = Gtk.Grid()
        self.add(grid)
        descriptionLabel = Gtk.Label("Description: ")
        descriptionEntry = Gtk.Entry()
        descriptionEntry.set_text(self.prog.description)
        grid.attach(descriptionLabel, 0, 0, 1, 1)
        grid.attach(descriptionEntry, 1, 0, 2, 1)
        combos = []
        for i in range(CHANNEL_COUNT):
            iLabel = Gtk.Label(f"CH{i+1}: ")
            instrumentCombos = []
            iCombo = Gtk.ComboBoxText()
            for instrument in INSTRUMENTS:
                # GET THE CURRENT INSTRUMENT IF THERE IS ONE.
                iCombo.append_text(instrument)
            instrumentCombos.append(iCombo)
            grid.attach(iLabel, 0, 1+i, 1, 1)
            grid.attach(iCombo, 1, 1+i, 2, 1)



# for testing...
p = NDProg(0, "nofile", 0, "No program.")
win = EditProgramDialog(p)
win.show_all()
Gtk.main()

            
            
        
        