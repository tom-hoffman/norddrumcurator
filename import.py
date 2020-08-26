import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

import mido
import time

import functions
from model import *

class ImportAllWindow(Gtk.Window):
    def __init__(self,
                 root: DataRoot,
                 midi_port: mido.ports.IOPort):
        Gtk.Window.__init__(self, title = "PROG DUMP ALL")
        self.root = root
        self.midi_port = midi_port
        self.cleared = False
        self.messages = []
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

    def clear(self):
        m = self.midi_port.poll()
        if type(m) != mido.Message:
            self.cleared = True
            self.progressBar.set_fraction(0.0)
            self.setupImportInstructions()
        else:
            self.progressBar.pulse()

    def on_timeout(self):
        # Called every 50 ms.
        if not(self.cleared):
            self.clear()
        else:
            m = self.midi_port.poll()
            if isinstance(m, mido.Message):
                if m.type == 'sysex':
                    c = functions.allMessageToOne(m)
                    self.messages.append(c)
                    l = len(self.messages)
                    self.progressBar.set_fraction(l * 0.01)
                    if l >= 99:
                        print(self.messages)
                        return False
            else:
                print("Slow the rate" + str(len(self.messages)))
            

        
        return True

            
        
    
    def cancel(self,
               button: Gtk.Button):
        self.destroy()

win = ImportAllWindow(DataRoot(), mido.open_ioport(functions.getMidiPort()))
time.sleep(0)
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

