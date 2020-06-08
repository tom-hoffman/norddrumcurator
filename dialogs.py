import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from constants import *
from functions import *

def layoutProgramPage():
    progGrid = Gtk.Grid()
    nameLabel = Gtk.Label("Name: ")
    self.nameEntry = Gtk.Entry()
    progGrid.attach(nameLabel, 0, 0, 1, 1)
    progGrid.attach(self.nameEntry, 1, 0, 2, 1)
    styleLabel = Gtk.Label("Style: ")
    self.styleCombo = Gtk.ComboBoxText()
    for style in STYLES:
        styleCombo.append_text(style)
    progGrid.attach(styleLabel, 0, 1, 1, 1)
    progGrid.attach(self.styleCombo, 1, 1, 2, 1)
    catLabel = Gtk.Label("Category: ")
    self.catCombo = Gtk.ComboBoxText()
    for cat in CATEGORIES:
        self.catCombo.append_text(cat)
    progGrid.attach(catLabel, 0, 2, 1, 1)
    progGrid.attach(self.catCombo, 1, 2, 2, 1)
    favoriteLabel = Gtk.Label("Favorite: ")
    self.favoriteButton = Gtk.CheckButton()
    progGrid.attach(favoriteLabel, 0, 3, 1, 1)
    progGrid.attach(self.favoriteButton, 1, 3, 2, 1)
    presetLabel = Gtk.Label("Nord Preset: ")
    self.presetButton = Gtk.CheckButton()
    progGrid.attach(presetLabel, 0, 4, 1, 1)
    progGrid.attach(self.presetButton, 1, 4, 2, 1)
    return progGrid

def layoutChannelPage():
    chanGrid = Gtk.Grid()
    nameLabel = Gtk.Label("Name: ")
    nameEntry = Gtk.Entry()
    chanGrid.attach(nameLabel, 0, 0, 1, 1)
    chanGrid.attach(nameEntry, 1, 0, 2, 1)
    instLabel = Gtk.Label("Instrument: ")
    instCombo = Gtk.ComboBoxText()
    for instrument in INSTRUMENTS:
        instCombo.append_text(instrument)
    chanGrid.attach(instLabel, 0, 1, 1, 1)
    chanGrid.attach(instCombo, 1, 1, 2, 1)
    favoriteLabel = Gtk.Label("Favorite: ")
    favoriteButton = Gtk.CheckButton()
    chanGrid.attach(favoriteLabel, 0, 2, 1, 1)
    chanGrid.attach(favoriteButton, 1, 2, 2, 1)
    return chanGrid


class ImportOneProgramWindow(Gtk.Window):
    def __init__(self, root, midi_port):
        # self: DataRoot, midi_port: mido.IOPort
        Gtk.Window.__init__(self, title="Import ONE program...")
        self.root = root
        self.midi_port = midi_port
        # stack setup
        self.set_border_width(10)
        self.outerVBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                                 spacing=6)
        self.add(self.outerVBox)
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(500)
        # page 1 - load
        self.loadPage = self.layoutLoadPage()
        self.stack.add_titled(self.loadPage, "load_page", "Load")
        # page 2 - program metadata
        self.layoutProgramPage()
        self.stack.add_titled(self.progGrid, "prog_page", "Program")
        # page 3 - 6 - channel metadata
        for i in range(1, 5):
            self.stack.add_titled(layoutChannelPage(),
                                  f"chan_{i}_page", f"CH{i}")
        # putting it together
        self.outerVBox.pack_start(self.stack, True, True, 0)
        self.layoutCancelSubmit()
        self.outerVBox.pack_end(self.csBox, True, True, 0)

    def layoutProgramPage(self):
        self.progGrid = Gtk.Grid()
        nameLabel = Gtk.Label("Name: ")
        self.nameEntry = Gtk.Entry()
        self.progGrid.attach(nameLabel, 0, 0, 1, 1)
        self.progGrid.attach(self.nameEntry, 1, 0, 2, 1)
        styleLabel = Gtk.Label("Style: ")
        self.styleCombo = Gtk.ComboBoxText()
        for style in STYLES:
            self.styleCombo.append_text(style)
        self.progGrid.attach(styleLabel, 0, 1, 1, 1)
        self.progGrid.attach(self.styleCombo, 1, 1, 2, 1)
        catLabel = Gtk.Label("Category: ")
        self.catCombo = Gtk.ComboBoxText()
        for cat in CATEGORIES:
            self.catCombo.append_text(cat)
        self.progGrid.attach(catLabel, 0, 2, 1, 1)
        self.progGrid.attach(self.catCombo, 1, 2, 2, 1)
        favoriteLabel = Gtk.Label("Favorite: ")
        self.favoriteButton = Gtk.CheckButton()
        self.progGrid.attach(favoriteLabel, 0, 3, 1, 1)
        self.progGrid.attach(self.favoriteButton, 1, 3, 2, 1)
        presetLabel = Gtk.Label("Nord Preset: ")
        self.presetButton = Gtk.CheckButton()
        self.progGrid.attach(presetLabel, 0, 4, 1, 1)
        self.progGrid.attach(self.presetButton, 1, 4, 2, 1)
        

    def layoutLoadPage(self):
        loadVBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.loadLabel = Gtk.Label("Clearing MIDI message queue...")
        clearMidiMessages(self.midi_port)
        self.loadLabel.set_text("Waiting for PROG DUMP...")
        loadVBox.pack_start(self.loadLabel, False, False, 20)
        self.spinner = Gtk.Spinner()
        self.spinner.start()
        loadVBox.pack_start(self.spinner, False, False, 20)
        return loadVBox
    
    def cancel(self, msg):
        self.destroy()
    
    def layoutCancelSubmit(self):
        self.csBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        subButt = Gtk.Button.new_with_label("Submit")
        subButt.set_sensitive(False)
        self.csBox.pack_end(subButt, False, False, 0)
        cButt = Gtk.Button.new_with_label("Cancel")
        cButt.connect("clicked", self.cancel)
        self.csBox.pack_end(cButt, False, False, 0)
        
        