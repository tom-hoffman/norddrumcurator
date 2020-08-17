from typing import List, Dict

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

import dialogs
import functions
import model
from constants import *
from ndexceptions import *

# Screen layout helper functions.

class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        # (app :: NordDrum1Manager) -> MemoryWindow
        # Note that app.root is the data root.
        self.app = app # not 100% sure this is necessary.
        Gtk.ApplicationWindow.__init__(self,
                                       title="Nord Drum Curator",
                                       application=app)
        self.set_default_size(1200, 800)
        self.set_border_width(4)
        wholeGrid = Gtk.VBox()
        wholeGrid.set_size_request(1200, 800)
        self.add(wholeGrid)
        file_menu_container = Gtk.Menu.new()
        # Menubar
        # This creates "insensitive" and unconnected menu items.
        menubar = Gtk.MenuBar.new()
        wholeGrid.add(menubar)
        self.menuDict = {}
        for key, value in MENU_DICT.items():
            container = Gtk.Menu.new()
            self.menuDict[key] = Gtk.MenuItem.new_with_label(key)
            menubar.append(self.menuDict[key])
            self.menuDict[key].set_submenu(container)
            for i in value:
                self.menuDict[i] = Gtk.MenuItem.new_with_label(i)
                self.menuDict[i].set_sensitive(False)
                container.append(self.menuDict[i])
        # Panes
        paned = Gtk.HPaned()
        wholeGrid.add(paned)
        # Memory in left.
        swLeft = Gtk.ScrolledWindow()
        swLeft.set_shadow_type(Gtk.ShadowType.IN)
        swLeft.set_size_request(360, 800)
        self.memList = Gtk.ListBox()
        self.memList.set_selection_mode(Gtk.SelectionMode.SINGLE)
        swLeft.add(self.memList)
        paned.add1(swLeft)
        self.populateMemoryRows()
        # Programs on right.
        swRight = Gtk.ScrolledWindow()
        swRight.set_shadow_type(Gtk.ShadowType.IN)
        self.progListBox = Gtk.ListBox()
        self.populateProgramRows()
        swRight.add(self.progListBox)
        paned.add2(swRight)

    def redraw(self, w, memRow=None):
        # (w :: Gtk.Window, memRow :: Gtk.Hbox)
        # memRow is an unselected row you need to redraw.
        pass
        # self.updateProgTree()
        # self.updateMemoryList(memRow)

    def populateProgramRows(self):
        progs = self.app.root.programs
        for p in progs:
            self.progListBox.add(self.buildProgramRow(p))

    def populateMemoryRows(self):
        slots = self.app.root.memory
        for i in range(0, len(slots)):
            self.memList.add(self.buildMemoryRow(i))

    def buildProgramRow(self, p: model.NDProg) -> Gtk.ListBoxRow:
        r = Gtk.ListBoxRow()
        hb = self.progRowLabels(p)
        # buttons
        r.add(hb)
        return r

    def buildMemoryRow(self, i):
        # (i :: int) -> Gtk.ListBoxRow
        r = Gtk.ListBoxRow()
        hb = self.memRowLabels(i)
        r.add(hb)
        return r

    def progRowLabels(self, p: model.NDProg) -> Gtk.HBox:
        hb = Gtk.HBox()
        css = hb.get_style_context()
        hb.pack_start(Gtk.Label(p.description),
                      expand = False, fill = False, padding = 10)
        return hb

    def memRowLabels(self, i):
        # (i :: int) -> Gtk.Hbox
        hb = Gtk.HBox()
        css = hb.get_style_context()
        css.add_class(self.app.root.cache_status[i])
        if self.app.root.memory[i] == -1:
            hb.pack_start(Gtk.Label("No data."),
                          expand = False, fill = True, padding = 10)
        else:
            p = self.getProgramFromMemory(i)
            labels = [str(i), p.description]
            for l in labels:
                hb.pack_start(Gtk.Label(l),
                              expand = False, fill = True, padding = 10)
            self.memRowButtons(hb, i)

        hb.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        hb.drag_dest_add_text_targets()
        hb.connect("drag-data-received", self.on_drag_data_received)
        return hb

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

    def getActiveRowBox(self):
        return self.memList.get_selected_row().get_child()

    def getActiveMemoryIndex(self, rBox):
        return int(rBox.get_children()[0].get_text())

    def getProgramFromMemory(self, m):
        # (memory :: int) -> NDProgram
        return self.app.root.programs[self.app.root.memory[m]]

    def updateMemoryListBox(self, rBox = None):
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

    def getMemSlotFromHBox(self, widget):
        return int(widget.get_children()[0].get_text())

# Drag and drop handlers.

    def tree_drag_begin(self, treeview, context):
        print(f'Beginning drag from {treeview}.')

    def on_drag_data_received(self, widget, drag_context, x, y,
                              data, info, time):
        text = data.get_text()
        if text != "-1":
            slot = self.getMemSlotFromHBox(widget)
            print(f"Received program {text} for memory slot {slot}.")
            prog = int(text)
            self.app.root.memory[slot] = prog
            self.app.root.cache_status[slot] = "dirty"
            self.redraw(None, widget)
        else:
            warn = Gtk.MessageDialog(
                transient_for = self,
                flags = 0,
                message_type = Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="You cannot drag a channel")
            warn.run()
            warn.destroy()

# Button handlers.

    def rowButtonClicked(self, button, slot, action):
        # (button :: Gtk.Button, slot :: int, action :: str) ->
        print(f"Clicked {action} for {slot}.")
        functions.sendMidiProgramChange(self.app.port, slot)
        r = button.get_parent().get_parent()
        self.memList.select_row(r)
        # if action...





