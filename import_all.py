import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

import mido
import time

import rows
import functions

from model import *

class ImportAllWindow(Gtk.Window):
    def __init__(self,
                 root: DataRoot,
                 memListBox: rows.MemoryListBox,
                 progListBox: Gtk.ListBox,
                 midi_port: mido.ports.IOPort):
        Gtk.Window.__init__(self, title = "PROG DUMP ALL")
        self.root = root
        self.memListBox = memListBox
        self.progListBox = progListBox
        self.midi_port = midi_port
        self.cleared = False
        self.showingReadingMessage = False
        self.message_counter = 0
        self.set_modal(True)
        self.set_default_size(300, 200)
        self.set_border_width(10)
        vbox = Gtk.VBox(spacing = 6)
        self.add(vbox)
        self.textBox = Gtk.VBox(spacing = 0)
        self.textBox.set_size_request(300, 100)
        vbox.pack_start(self.textBox, False, False, 0)
        self.lab = Gtk.Label()
        self.lab.set_text('Clearing message queue...')
        self.lab1 = Gtk.Label()
        self.lab2 = Gtk.Label()
        self.lab3 = Gtk.Label()
        self.textBox.pack_start(self.lab, True, True, 0)
        self.textBox.pack_start(self.lab1, True, True, 0)
        self.textBox.pack_start(self.lab2, True, True, 0)
        self.textBox.pack_start(self.lab3, True, True, 0)
        self.progressBar = Gtk.ProgressBar()
        self.progressBar.set_pulse_step(0.05)
        vbox.pack_start(self.progressBar, True, True, 40)
        cancelButton = Gtk.Button.new_with_label("Cancel")
        cancelButton.connect("clicked", self.cancel)
        cancelButton.set_property("width-request", 40)
        vbox.pack_end(cancelButton, False, False, 0)
        self.timeout_id = GLib.timeout_add(80, self.on_timeout)

    def setupImportInstructions(self):
        self.lab.set_text('On the Nord Drum,')
        self.lab1.set_text('press SHIFT/PROG DUMP, then')
        self.lab2.set_text('press PROG DUMP until it says "ALL,"')
        self.lab3.set_text('and then press PROGRAM.')

    def showReadingMessage(self):
        self.lab.set_text('')
        self.lab1.set_text('Reading programs from')
        self.lab2.set_text('Nord Drum...')
        self.lab3.set_text('')

    def clear(self):
        m = self.midi_port.poll()
        if type(m) != mido.Message:
            self.cleared = True
            self.progressBar.set_fraction(0.0)
            self.setupImportInstructions()
        else:
            self.progressBar.pulse()

    def on_timeout(self):
        # Called every 80 ms (from above).
        if not(self.cleared):
            self.clear()
        else:
            m = self.midi_port.poll()
            if isinstance(m, mido.Message):
                if m.type == 'sysex':
                    if not(self.showingReadingMessage):
                        self.showReadingMessage()
                        self.showingReadingMessage = True
                    # This should set each memory slot to the ID of
                    # the correct program.
                    # clean the message.
                    cleaned_message = functions.allMessageToOne(m)
                    # get the checksum.
                    check = functions.messageChecksum(cleaned_message)
                    # check if it is a dupe.
                    match = self.root.findDuplicateProgram(check)
                    if match == None:
                        ID = self.root.program_counter
                        file_path = functions.program_file_name(ID)
                        prog = NDProg(ID,
                                      file_path,
                                      check,
                                      f"new import-{ID}")
                        self.root.addProgram(prog, cleaned_message)
                        self.root.memory[self.message_counter] = ID
                        parentWin = self.props.transient_for
                        pRow = rows.ProgramRow(prog)
                        self.progListBox.add(pRow)
                        self.progListBox.show_all()
                        # parentWin.connectProgramInstrumentButtons(pRow)
                    else:
                        self.root.memory[self.message_counter] = match
                    # either way...
                    self.root.cache_status[self.message_counter] = "checked"
                    self.message_counter += 1
                    self.progressBar.set_fraction(self.message_counter * 0.01)        
                    if self.message_counter == 99:
                        self.memListBox.updateAll()
                        self.destroy()
                else:
                    pass
            else:
                pass
        return True






#                     
#                     
        
    
    def cancel(self,
               button: Gtk.Button):
        self.destroy()



