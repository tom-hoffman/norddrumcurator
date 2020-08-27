import time
from typing import List, Dict

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import GLib

import edit
import rows
import functions
import import_all
from model import *
from constants import *
from ndexceptions import *


class AppWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        # (app :: NordDrum1Manager) -> MemoryWindow
        # DATA
        # Note that app.root is the data root.
        
        self.app = app # not 100% sure this is necessary.
        self.all_instrument_buttons = []
        Gtk.ApplicationWindow.__init__(self,
                                       title="Nord Drum Curator",
                                       application=app)
        self.set_default_size(1000, 800)
        self.set_border_width(4)
        wholeGrid = Gtk.VBox()
        wholeGrid.set_size_request(1000, 800)
        self.add(wholeGrid)
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
                if i == "SEPARATOR":
                    container.append(Gtk.SeparatorMenuItem.new())
                else:
                    self.menuDict[i] = Gtk.MenuItem.new_with_label(i)
                    self.menuDict[i].set_sensitive(False)
                    container.append(self.menuDict[i])
        self.connectMenuItems()
        # Panes
        paned = Gtk.HPaned()
        wholeGrid.add(paned)
        # Programs on right.
        swRight = Gtk.ScrolledWindow()
        swRight.set_shadow_type(Gtk.ShadowType.IN)
        self.progListBox = Gtk.ListBox()
        self.progListBox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        # extend the all instr button list
        self.progListBox.connect("row-selected", self.programRowSelected)
        self.buildProgramRows()
        swRight.add(self.progListBox)
        paned.add2(swRight)
        # Memory in left.
        swLeft = Gtk.ScrolledWindow()
        swLeft.set_shadow_type(Gtk.ShadowType.IN)
        swLeft.set_size_request(400, 800)
        self.memListBox = rows.MemoryListBox()
        self.memListBox.set_selection_mode(Gtk.SelectionMode.SINGLE)
        swLeft.add(self.memListBox)
        paned.add1(swLeft)
        self.buildMemoryRows()

    def getSelectedProgram(self) -> NDProg:
        return self.progListBox.get_selected_row().program

# Menu actions

    def connectMenuItems(self):
        e = self.menuDict["Edit program..."]
        e.connect("activate", self.launchEditDialog)
        save = self.menuDict["Save"]
        save.set_sensitive(True)
        save.connect("activate", self.saveRoot)
        ex = self.menuDict["Exit"]
        ex.set_sensitive(True)
        ex.connect("activate", self.ex)
        pull = self.menuDict["Pull all..."]
        pull.set_sensitive(True)
        pull.connect("activate", self.pull_all)

    def launchEditDialog(self, menu):
        p = self.progListBox.get_selected_row()
        diag = edit.EditProgramDialog(p)
        diag.set_transient_for(self)
        diag.connect("destroy", self.redraw)
        diag.show_all()
    
    def saveRoot(self, menu):
        self.app.root.save()

    def ex(self, menu):
        self.destroy()
        
    def pull_all(self, menu):
        iw = import_all.ImportAllWindow(self.app.root,
                                   self.memListBox,
                                   self.app.port)
        iw.set_transient_for(self)
        iw.show_all()

    def programRowSelected(self, box, row):
        if row:
            self.menuDict["Edit program..."].set_sensitive(True)
        else:
            self.menuDict["Edit program..."].set_sensitive(False)

# Other window methods

    def redraw(self, w):
        # (w :: Gtk.Window)
        self.memListBox.updateAll()

    def connectProgramInstrumentButtons(self,
                                        pr: rows.ProgramRow):
        for i in range(len(pr.channel_buttons)):
            b = pr.channel_buttons[i]
            b.connect("clicked", self.previewProgramSound, 3 - i)
            pr.testButton.connect("clicked",
                                  self.activateProgramInstruments,
                                   pr)
            self.all_instrument_buttons.append(b)

    def connectMemoryInstrumentButtons(self,
                                       mr: rows.MemoryRow):
        for i in range(len(mr.channel_buttons)):
            b = mr.channel_buttons[i]
            b.connect("clicked", self.previewProgramSound, 3 - i)
            mr.testButton.connect("clicked",
                                  self.activateMemoryInstruments,
                                  mr)
            self.all_instrument_buttons.append(b)                                 

    def activateProgramInstruments(self,
                                   button: Gtk.Button,
                                   pr: rows.ProgramRow):
        syx = functions.read_sysex(pr.program.file)
        self.app.port.send(syx)
        self.deactivateAllInstruments()
        for b in pr.channel_buttons:
            b.set_sensitive(True)
    
    def activateMemoryInstruments(self,
                                  button: Gtk.Button,
                                  mr: rows.MemoryRow):
        value = self.app.root.memory[mr.slot]
        program = self.app.root.findProgram(value)
        syx = functions.read_sysex(program.file)
        self.app.port.send(syx)
        self.deactivateAllInstruments()
        for b in mr.channel_buttons:
            b.set_sensitive(True)
        

# Building program and memory rows.

    def buildProgramRows(self):
        progs = self.app.root.programs
        for p in progs:
            self.progListBox.add(rows.ProgramRow(p))
        self.progListBox.foreach(self.connectProgramInstrumentButtons)

    def buildMemoryRows(self):
        slots = self.app.root.memory
        for i in range(0, len(slots)):
            self.memListBox.add(rows.MemoryRow(i,self.app.root))
        self.memListBox.foreach(self.connectMemoryInstrumentButtons)


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

        hb.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        hb.drag_dest_add_text_targets()
        hb.connect("drag-data-received", self.on_drag_data_received)
        return hb
    

# Drag and drop handlers.

    def tree_drag_begin(self, treeview, context):
        print(f'Beginning drag from {treeview}.')



# Button handlers.
    
    def findProgram(self, prog_id: int) -> NDProg:
        return functions.findProgram(prog_id, self.app.root.programs)
    
    def previewProgramSound(self,
                            button: Gtk.Button,
                            channel_index: int):
        functions.playSound(self.app.port, channel_index)

    def deactivateAllInstruments(self):
        for b in self.all_instrument_buttons:
            b.set_sensitive(False)
