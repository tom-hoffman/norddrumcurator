import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import ndexceptions
from model import *


class ProgramRow(Gtk.ListBoxRow):
    def __init__(self,
                 program: NDProg):
        Gtk.ListBoxRow.__init__(self)
        self.program = program
        hb = Gtk.HBox()
        # setting up drag and drop
        hb.drag_source_set(Gdk.ModifierType.BUTTON1_MASK,
                           [],
                           Gdk.DragAction.COPY)
        hb.drag_source_add_text_targets()
        #hb.connect('drag-begin', self.drag_begin)
        #hb.connect('drag-data-get', self.drag_data_get)
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
    
    def updateRow(self,
                  new: NDProg):
        self.descriptionLabel.set_text(new.description)
        instruments = list(reversed(new.instruments))
        for i in range(len(self.channel_buttons)):
            self.channel_buttons[i].set_label(instruments[i])
        
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
        # self.hb.connect("drag-data-received", self.on_drag_data_received)
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
        css.add_class(self.root.cache_status[self.slot])
        value = self.root.memory[self.slot]
        program = self.root.findProgram(value)
        self.descriptionLabel.set_text(program.description)
        instruments = list(reversed(program.instruments))
        for i in range(len(self.channel_buttons)):
            self.channel_buttons[i].set_label(instruments[i])

#     def on_drag_data_received(self, widget, drag_context, x, y,
#                               data, info, time):
#         text = data.get_text()
#         if text != "-1":
#             slot = self.getMemSlotFromHBox(widget)
#             print(f"Received program {text} for memory slot {slot}.")
#             prog = int(text)
#             self.app.root.memory[slot] = prog
#             self.app.root.cache_status[slot] = "dirty"
#             self.redraw(None, widget)
#         else:
#             warn = Gtk.MessageDialog(
#                 transient_for = self,
#                 flags = 0,
#                 message_type = Gtk.MessageType.ERROR,
#                 buttons=Gtk.ButtonsType.OK,
#                 text="You cannot drag a channel")
#             warn.run()
#             warn.destroy()

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
        
        