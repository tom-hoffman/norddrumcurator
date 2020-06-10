import zlib

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

import dialogs
from constants import *

def addChannelBranches(store, progRow, channels):
    for i in range(0, len(channels) - 1):
        try:
            ch = channels[i]
            store.append(progRow, [i+1, ch.name, ch.instrument, ""])
        except IndexError:
            pass

# THIS NEEDS TO BE FILES ON DISK!
def populateMemoryTreeStore(memory, programs):
    # (MemoryWindow, memory :: list<int>,
    #  programs :: dict<int : NDProg>) -> Gtk.TreeStore
    store = Gtk.TreeStore(int, str, str, str)
    for i in range(0, len(memory) - 1):
        prog = programs[memory[i]]  # get the right program
        progRow = store.append(None, [i+1, prog.name,
                                      prog.style, prog.category])
        addChannelBranches(store, progRow, prog.channels)     
    return store

def setUpColumns(tv):
    colHeaders = ["Number", "Name", "Style/Instrument", "Category"]
    for i in range(0, len(colHeaders)):
        tv.append_column(Gtk.TreeViewColumn(colHeaders[i], 
                                            Gtk.CellRendererText(),
                                            text = i))

class MemoryWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        # (app :: NordDrum1Manager) -> MemoryWindow
        # Note that app.root is the data root.
        self.app = app # not 100% sure this is necessary.
        Gtk.ApplicationWindow.__init__(self,
                                       title="Tom's Nord Drum 1 Program Manager",
                                       application=app)
        self.set_default_size(1200, 800)
        self.set_border_width(10)
        # Panes
        paned = Gtk.HPaned()
        self.add(paned)
        # Memory in left.
        swLeft = Gtk.ScrolledWindow()
        swLeft.set_shadow_type(Gtk.ShadowType.IN)
        swLeft.set_size_request(460, 800)
        self.lb = Gtk.ListBox()
        swLeft.add(self.lb)
        paned.add1(swLeft)
        self.populateMemoryRows()
        # Programs on right.
        swRight = Gtk.ScrolledWindow()
        swRight.set_shadow_type(Gtk.ShadowType.IN)
        self.store = populateMemoryTreeStore(self.app.root.memory,
                                             self.app.root.programs)
        tv = Gtk.TreeView()
        tv.set_model(self.store)
        setUpColumns(tv)
        swRight.add(tv)
        paned.add2(swRight)
        

    def rowButtonClicked(self, button, slot, action):
        # (button :: Gtk.Button, slot :: int, action :: str) ->
        print(f"Clicked {action} for {slot}.")
        if action == "Pull":
            self.importWindow = dialogs.ImportOneProgramWindow(self.app.root,
                                                               self.app.port)
            self.importWindow.set_transient_for(self)
            self.importWindow.connect("destroy", self.redraw)
            self.importWindow.show_all()
            callback_id = GLib.timeout_add(250, self.pull_one,
                                           self.app.port)

    def redraw(self, w):
        print("REDRAW!")

    def pull_one(self, midi_port):
        # this is the action after a program is pulled via MIDI.
        msg = midi_port.poll()
        if msg is None:
            return True
        elif (msg.type == "sysex") and (len(msg.data) == 108):
            iw = self.importWindow
            chk = zlib.crc32(msg.bin())
            # check to see if this is a dupe.
            # if not...
            self.importWindow.midiMessage = msg.data
            self.importWindow.checkSum = chk
            self.importWindow.subButt.set_sensitive(True)
            sw = Gtk.StackSwitcher()
            sw.set_stack(iw.stack)
            sw.show()
            iw.loadLabel.set_text("Enter program metadata.")
            iw.spinner.stop()
            iw.stack.set_visible_child_name("prog_page")
            iw.outerVBox.pack_start(sw, True, True, 0)
            iw.outerVBox.reorder_child(sw, 0)
            return False
        else:
            return True

    def getProgramFromMemory(self, m):
        # (memory :: int) -> NDProgram
        return self.app.root.programs[self.app.root.memory[m]]

    def memRowLabels(self, i):
        # (i :: int) -> Gtk.Hbox
        p = self.getProgramFromMemory(i)
        labels = [str(i + 1), p.name]
        hb = Gtk.HBox()
        for l in labels:
            hb.pack_start(Gtk.Label(l), expand = True, fill = True, padding = 10)
        return hb
    
    def memRowButtons(self, hb, slot):
        # (hb :: Gtk.HBox, slot :: int) -> 
        # Adds buttons to hb (HBox).
        # Change these for icons.
        actions = ["Pull", "Pick", "Copy", "Paste"]
        for b in actions:
            lab = Gtk.Label(b)
            lab.set_padding(2, 2)
            but = Gtk.Button()
            but.set_property("width-request", 20)
            but.add(lab)
            but.connect("clicked", self.rowButtonClicked, slot, b)
            hb.pack_end(but, expand = False, fill = False, padding = 2)

    def buildMemoryRow(self, i):
        # (i :: int) -> Gtk.ListBoxRow
        r = Gtk.ListBoxRow()
        hb = self.memRowLabels(i)
        self.memRowButtons(hb, i)
        r.add(hb)
        return r
        
    def populateMemoryRows(self):
        slots = self.app.root.memory
        for i in range(0, len(slots)):
            self.lb.add(self.buildMemoryRow(i))