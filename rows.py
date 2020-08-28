import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkX11

import ndexceptions
from model import *


class ProgramRow(Gtk.ListBoxRow):
    def __init__(self,
                 program: NDProg):
        Gtk.ListBoxRow.__init__(self)
        self.program = program
        hb = Gtk.HBox()
        copyButton = Gtk.Button.new_from_icon_name("edit-copy", 2)
        hb.pack_start(copyButton, expand = False, fill = False, padding = 2)
        self.descriptionLabel = Gtk.Label(label = self.program.description)

        hb.pack_start(self.descriptionLabel,
                      expand = False, fill = False, padding = 2)
        self.add(hb)
        buttonBox = Gtk.HBox()
        self.channel_buttons = []
        instruments = list(reversed(self.program.instruments))
        for i in instruments:
            b = Gtk.Button.new_with_label(i)
            b.get_style_context().add_class("instrument")
            b.set_sensitive(False)
            buttonBox.pack_end(b, expand = False, fill = False, padding = 2)
            self.channel_buttons.append(b)      
        hb.pack_end(buttonBox,
                      expand = False, fill = False, padding = 2)
        self.testButton = Gtk.Button.new_with_label("test")
        self.testButton.get_style_context().add_class("control")
        buttonBox.pack_end(self.testButton, expand = False,
                           fill = False, padding = 2)
        copyButton.drag_source_set(Gdk.ModifierType.BUTTON1_MASK,
                           [],
                           Gdk.DragAction.COPY)
        copyButton.drag_source_add_text_targets()
        copyButton.connect('drag-begin', self.drag_begin)
        copyButton.connect('drag-data-get', self.drag_data_get)
    
    def updateRow(self,
                  new: NDProg):
        self.descriptionLabel.set_text(new.description)
        instruments = list(reversed(new.instruments))
        for i in range(len(self.channel_buttons)):
            self.channel_buttons[i].set_label(instruments[i])
            
    def drag_begin(self,
                   widget: Gtk.Widget,
                   context: GdkX11.X11DragContext):
        print(f'Beginning drag from {widget}.')

    def drag_data_get(self,
                      sending_widget: Gtk.Widget,
                      context: GdkX11.X11DragContext,
                      data: Gtk.SelectionData,
                      info: int,
                      time: int):
        data.set_text(str(self.program.ID), -1)
        
class MemoryRow(Gtk.ListBoxRow):
    def __init__(self,
                 slot_index: int,
                 root: DataRoot):
        Gtk.ListBoxRow.__init__(self)
        self.slot = slot_index
        self.root = root
        value = root.memory[self.slot]
        self.hb = Gtk.HBox()
        # Drag and drop setup
        self.hb.drag_dest_set(Gtk.DestDefaults.ALL, [], Gdk.DragAction.COPY)
        self.hb.drag_dest_add_text_targets()
        self.hb.connect("drag-data-received", self.on_drag_data_received)
        self.numberLabel = Gtk.Label(label = f"{str(self.slot + 1)}.  ")
        self.hb.pack_start(self.numberLabel, expand = False,
                      fill = False, padding = 0)
        program = root.findProgram(value)
        self.descriptionLabel = Gtk.Label(label = program.description)
        self.hb.pack_start(self.descriptionLabel,
                      expand = False, fill = False, padding = 0)
        self.add(self.hb)
        buttonBox = Gtk.HBox()
        self.hb.get_style_context().add_class(self.root.cache_status[self.slot])
        self.channel_buttons = []
        instruments = list(reversed(program.instruments))
        for i in instruments:
            b = Gtk.Button.new_with_label(i)
            b.get_style_context().add_class("mem-instrument")
            b.set_sensitive(False)
            buttonBox.pack_end(b, expand = False, fill = False, padding = 0)
            self.channel_buttons.append(b)      
        self.hb.pack_end(buttonBox,
                      expand = False, fill = False, padding = 2)
        self.testButton = Gtk.Button.new_with_label("test")
        self.testButton.get_style_context().add_class("mem-control")
        buttonBox.pack_end(self.testButton, expand = False,
                           fill = False, padding = 0)
    def updateRow(self):
        css = self.hb.get_style_context()
        css.remove_class("dirty")
        css.remove_class("unknown")
        css.remove_class("checked")
        css.add_class(self.root.cache_status[self.slot])
        value = self.root.memory[self.slot]
        program = self.root.findProgram(value)
        self.descriptionLabel.set_text(program.description)
        instruments = list(reversed(program.instruments))
        for i in range(len(self.channel_buttons)):
            self.channel_buttons[i].set_label(instruments[i])

    def on_drag_data_received(self,
                              widget,
                              drag_context: GdkX11.X11DragContext,
                              x: int,
                              y: int,
                              data: Gtk.SelectionData,
                              info: int,
                              time: int):
        self.root.memory[self.slot] = int(data.get_text())
        self.root.cache_status[self.slot] = "dirty"
        self.updateRow()
        
                              

class MemoryListBox(Gtk.ListBox):
    def __init__(self):
        Gtk.ListBox.__init__(self)
    def getMemoryRow(self,
                     slot: int) -> MemoryRow:
        for r in self.get_children():
            if r.slot == slot:
                return r
        return None
    def updateAll(self):
        for r in self.get_children():
            r.updateRow()
        
        