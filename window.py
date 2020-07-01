import zlib

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

import dialogs
import functions
from constants import *

def addChannelBranches(store, progRow, channels):
    for i in range(0, len(channels)):
        try:
            ch = channels[i]
            store.append(progRow, [ch.name, ch.instrument, ""])
        except IndexError:
            pass

def populateFilesTreeStore(memory, programs):
    # (MemoryWindow, memory :: list<int>,
    #  programs :: dict<int : NDProg>) -> Gtk.TreeStore
    store = Gtk.TreeStore(str, str, str)
    for i in range(0, len(programs)):
        prog = programs[i]  # get the right program
        progRow = store.append(None, [prog.name,
                                      prog.style, prog.category])
        addChannelBranches(store, progRow, prog.channels)     
    return store

def setUpColumns(tv):
    colHeaders = ["Name", "Style/Instrument", "Category"]
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
        self.memList = Gtk.ListBox()
        self.memList.set_selection_mode(Gtk.SelectionMode.SINGLE)
        swLeft.add(self.memList)
        paned.add1(swLeft)
        self.populateMemoryRows()
        # Programs on right.
        swRight = Gtk.ScrolledWindow()
        swRight.set_shadow_type(Gtk.ShadowType.IN)
        self.progTree = Gtk.TreeView()
        self.updateProgTree()
        setUpColumns(self.progTree)
        swRight.add(self.progTree)
        paned.add2(swRight)

    def updateProgTree(self):
        self.store = populateFilesTreeStore(self.app.root.memory,
                                             self.app.root.programs)
        self.progTree.set_model(self.store)

    def getActiveRowBox(self):
        return self.memList.get_selected_row().get_child().get_children()

    def getActiveMemoryIndex(self, rBox):
        return int(rBox[0].get_text())

    def updateMemoryList(self):
        # this is a bit insane, context-wise.
        m = self.app.root.memory
        p = self.app.root.programs
        rBox = self.getActiveRowBox()
        oldLabel = rBox[1]
        progIndex = self.getActiveMemoryIndex(rBox)
        oldLabel.set_label(p[m[progIndex]].name)

    def redraw(self, w):
        # also saving...
        functions.save(self.app.root)
        self.updateProgTree()
        self.updateMemoryList()

    def memRowLabels(self, i):
        # (i :: int) -> Gtk.Hbox
        p = self.getProgramFromMemory(i)
        labels = [str(i), p.name]
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
        for i in range(1, len(slots)):
            self.memList.add(self.buildMemoryRow(i))

    def rowButtonClicked(self, button, slot, action):
        # (button :: Gtk.Button, slot :: int, action :: str) ->
        print(f"Clicked {action} for {slot}.")
        r = button.get_parent().get_parent()
        self.memList.select_row(r)
        if action == "Pull":
            self.importWindow = dialogs.ImportOneProgramWindow(slot,
                                                               self.app.root,
                                                               self.app.port)
            self.importWindow.set_transient_for(self)
            self.importWindow.connect("destroy", self.redraw)
            self.importWindow.show_all()
            callback_id = GLib.timeout_add(250, self.pull_one,
                                           self.app.port)



    def pull_one(self, midi_port):
        # this is the action after a program is pulled via MIDI.
        msg = midi_port.poll()
        if msg is None:
            return True
        elif (msg.type == "sysex") and (len(msg.data) == 108):
            iw = self.importWindow
            chk = zlib.crc32(msg.bin())
            # check to see if this is a dupe.
            match = functions.programMatch(chk, self.app.root.programs)
            if match == -1:
                iw.midiMessage = msg
                iw.checkSum = chk
                iw.subButt.set_sensitive(True)
                sw = Gtk.StackSwitcher()
                sw.set_stack(iw.stack)
                sw.show()
                iw.loadLabel.set_text("Enter program metadata.")
                iw.spinner.stop()
                iw.stack.set_visible_child_name("prog_page")
                iw.outerVBox.pack_start(sw, True, True, 0)
                iw.outerVBox.reorder_child(sw, 0)
            else:
                rBox = self.getActiveRowBox()
                self.app.root.memory[self.getActiveMemoryIndex(rBox)] = match 
                print(f"Setting row {self.getActiveMemoryIndex(rBox)} to {match}.")
                iw.destroy()
            return False
        else:
            return True

    def getProgramFromMemory(self, m):
        # (memory :: int) -> NDProgram
        return self.app.root.programs[self.app.root.memory[m]]

