import zlib

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

import dialogs
import functions
from constants import *
from ndexceptions import *

# Screen layout helper functions.

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
    for i in range(0, len(COLUMN_HEADERS)):
        tv.append_column(Gtk.TreeViewColumn(COLUMN_HEADERS[i], 
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
        self.progTree.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK,
                                               [('text/plain', 0, 0)], Gdk.DragAction.COPY)
        self.progTree.connect('drag-begin', self.tree_drag_begin)
        self.progTree.connect('drag-data-get', self.tree_drag_data_get)
        self.updateProgTree()
        setUpColumns(self.progTree)
        swRight.add(self.progTree)
        paned.add2(swRight)

    def redraw(self, w, memRow=None):
        # (w :: Gtk.Window, memRow :: Gtk.Hbox)
        # memRow is an unselected row you need to redraw.
        # also saving...
        functions.save(self.app.root)
        self.updateProgTree()
        self.updateMemoryList(memRow)

    def getProgramIndexFromName(self, name: str) -> int:
        # Returns -1 if the program name does not match.
        i = -1
        for key, value in self.app.root.programs.items():
            if name == value.name:
                i = key
        else:
            return i

    def getProgramNameFromTreeSelection(self) -> str:
        (store, treeIter) = self.progTree.get_selection().get_selected()
        return str(list(store[treeIter])[0])     
    
    def getProgramIndexFromTreeSelection(self):
        return(self.getProgramIndexFromName(
            self.getProgramNameFromTreeSelection()))
 
    def tree_drag_data_get(self, treeview, context, data, info, timestamp):
        # Getting the key of the selected branch.
        # XXX need to get the parent if this is a channel.
        i = str(self.getProgramIndexFromTreeSelection())
        if i == -1:
            # get the parent of the channel.
            raise NDError
        else:
            data.set_text(i, -1)
    
    def updateProgTree(self):
        self.store = populateFilesTreeStore(self.app.root.memory,
                                             self.app.root.programs)
        self.progTree.set_model(self.store)

    def getActiveRowBox(self):
        return self.memList.get_selected_row().get_child()

    def getActiveMemoryIndex(self, rBox):
        return int(rBox.get_children()[0].get_text())

    def getProgramFromMemory(self, m):
        # (memory :: int) -> NDProgram
        return self.app.root.programs[self.app.root.memory[m]]

    def updateMemoryList(self, rBox = None):
        # this is a bit insane, context-wise.
        m = self.app.root.memory
        p = self.app.root.programs
        if not(rBox):
            rBox = self.getActiveRowBox()
        else:
            rBox
        oldLabel = rBox.get_children()[1]
        progIndex = self.getActiveMemoryIndex(rBox)
        oldLabel.set_label(p[m[progIndex]].name)
        css = rBox.get_style_context()
        css.add_class(self.app.root.cache_status[progIndex])

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

    def memRowLabels(self, i):
        # (i :: int) -> Gtk.Hbox
        p = self.getProgramFromMemory(i)
        labels = [str(i), p.name]
        hb = Gtk.HBox()
        css = hb.get_style_context()
        css.add_class(self.app.root.cache_status[i])
        for l in labels:
            hb.pack_start(Gtk.Label(l),
                          expand = True, fill = True, padding = 10)
        hb.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        hb.drag_dest_add_text_targets()
        hb.connect("drag-data-received", self.on_drag_data_received)
        return hb

    def getMemSlotFromHBox(self, widget):
        return int(widget.get_children()[0].get_text())

# Drag and drop handlers.

    def tree_drag_begin(self, treeview, context):
        print(f'Beginning drag from {treeview}.')

    def on_drag_data_received(self, widget, drag_context, x, y,
                              data, info, time):
        text = data.get_text()
        slot = self.getMemSlotFromHBox(widget)
        print(f"Received program {text} for memory slot {slot}.")
        prog = int(text)
        self.app.root.memory[slot] = prog
        self.app.root.cache_status[slot] = "dirty"
        self.redraw(None, widget)
        
    def memRowButtons(self, hb, slot):
        # (hb :: Gtk.HBox, slot :: int) -> 
        # Adds buttons to hb (HBox).
        for b in ACTIONS:
            lab = Gtk.Label(b)
            lab.set_padding(2, 2)
            but = Gtk.Button()
            but.set_property("width-request", 20)
            but.add(lab)
            but.connect("clicked", self.rowButtonClicked, slot, b)
            hb.pack_end(but, expand = False, fill = False, padding = 2)

# Button handlers.

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

# Midi pull action.

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
                # if not a dupe.
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
                # if it is a dupe.
                rBox = self.getActiveRowBox()
                i = self.getActiveMemoryIndex(rBox)
                self.app.root.memory[i] = match
                self.app.root.cache_status[i] = "checked"
                iw.destroy()
            return False
        else:
            return True



