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
                             f"Editing program {self.prog.ID + 1}: {self.prog.description}")
        self.set_modal(True)
        self.set_default_size(400, 400)
        # Layout grid with interactive elements.
        grid = Gtk.Grid()
        grid.set_margin_top(40)
        grid.set_margin_start(40)
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        self.add(grid)
        # description
        descriptionLabel = Gtk.Label(label = "Description: ")
        self.descriptionEntry = Gtk.Entry()
        self.descriptionEntry.set_text(self.prog.description)
        row = 0
        grid.attach(descriptionLabel, 0, row, 1, 1)
        grid.attach(self.descriptionEntry, 1, row, 2, 1)
        row += 1
        # channels
        self.instrumentCombos = []
        for i in range(CHANNEL_COUNT):
            iLabel = Gtk.Label(label = f"CH{i+1}: ")
            iCombo = Gtk.ComboBoxText()
            for j in range(len(INSTRUMENTS)):
                instrument = INSTRUMENTS[j]
                iCombo.append_text(instrument)
                if instrument == prog.instruments[i]:
                    iCombo.set_active(j)
            self.instrumentCombos.append(iCombo)
            grid.attach(iLabel, 0, row, 1, 1)
            grid.attach(iCombo, 1, row, 2, 1)
            row += 1
        # key
        keyLabel = Gtk.Label(label = "Key: ")
        self.keyCombo = Gtk.ComboBoxText()
        for i in range(len(KEYS)):
            key = KEYS[i] 
            self.keyCombo.append_text(key)
            if key == prog.key:
                self.keyCombo.set_active(i)
        grid.attach(keyLabel, 0, row, 1, 1)
        grid.attach(self.keyCombo, 1, row, 2, 1)
        row += 1
        # Cancel/Submit
        csBox = Gtk.HBox(spacing = 6)
        subButt = Gtk.Button.new_with_label("Submit")
        subButt.connect("clicked", self.processInput)
        csBox.pack_end(subButt, False, False, 0)
        cButt = Gtk.Button.new_with_label("Cancel")
        cButt.connect("clicked", self.cancel)
        csBox.pack_end(cButt, False, False, 0)
        grid.attach(csBox, 1, row, 2, 1)

    def cancel(self, button):
        self.destroy()

    def processInput(self, button):
        p = self.prog
        p.description = self.descriptionEntry.get_text()
        p.instruments = [i.get_active_text() for i in self.instrumentCombos]
        p.key = self.keyCombo.get_active_text()
        print(p.instruments)
        # probably change the cache_status here?
        self.destroy()
            


            
            
        
        