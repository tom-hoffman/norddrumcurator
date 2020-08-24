import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

# model constants

# tags <= 5 characters.
TAGS = ["real", "retro", "ethno", "fx", "drums", "perc.", "kit"]
CHANNEL_COUNT = 4
# Instrument name length <= 5 characters.
INSTRUMENTS = ("?", "kick", "snare", "r-tom", "f-tom",
               "c-hat", "o-hat", "ride", "crash", "edrum",
               "clap", "cbell", "block", "bell",
               "metal", "drone", "scifi")
KEYS = ("?", "None", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
CACHE_STATUSES = ("checked", "dirty", "unknown")

# file constants
PICKLE_FILENAME = "drums.pickle"
FILE_PREFIX = "programs/"
FACTORY_SOUNDBANK = "nord_drum_factory_bank_v1.04.syx"

# MIDI constants
MIDI_INTERFACE = "UM-ONE:UM-ONE MIDI 1"
NOMINAL_MIDI_CHANNEL = 1
MIDI_CHANNEL = NOMINAL_MIDI_CHANNEL - 1
CHANNEL_NUMBERS = (36, 38, 46, 42)
VELOCITY = 100

# UI constants
CSS_PATH = 'gtkstyle.css'
CSS = Gtk.CssProvider()
CSS.load_from_path(CSS_PATH)
SCREEN = Gdk.Screen.get_default()
PRIORITY = Gtk.STYLE_PROVIDER_PRIORITY_USER
CONTEXT = Gtk.StyleContext()
CONTEXT.add_provider_for_screen(SCREEN, CSS, PRIORITY)

# these all have to be unique.
MENU_DICT = {"File" : ("New", "Open...", "Save", "Save as...", "Save copy...",
                       "Print...", "Exit"),
             "Edit" : ("Copy", "Paste", "SEPARATOR", "Edit program..."),
             "Sync" : ("Check sync", "Pull all...", "Push changes")}

FACTORY_SOUNDBANK_METADATA = (("retro", "Monologue", "drums"),
("real", "Classic Vistalite", "drums"),
("retro", "Blue House", "kit"),
("real", "Brushford", "kit"),
("real", "Bebox Delux", "drums"),
("retro", "Always Hip Hop", "kit"),
("real", "Gran Casa Timp", "kit"),
("retro", "Thanx to Burgees", "drums"),
("fx", "Reso Sweep", "perc"),
("retro", "Vince Gate", "drums"),
("retro", "UnoDosKickHat", "kit"),
("real", "spectrum", "drums"),
("real", "Ateiste", "drums"),
("retro", "Noisy Barrel Orchestra", "drums"),
("retro", "Higgins Particle Hat", "kit"),
("retro", "Clothed Funk Kit", "kit"),
("ethno", "Komal Melodic", "perc"),
("ethno", "Lalalatin", "perc"),
("retro", "Bend Down Disco", "perc"),
("retro", "Flying Dront Circus", "kit"),
("ethno", "Tribunal", "perc"),
("real", "King Kong Karma", "kit"),
("fx", "Training with Kolal", "perc"),
("retro", "Tiny Tiny Pic", "kit"),
("ethno", "Red Beat", "perc"),
("retro", "peatPerlife", "kit"),
("retro", "Piccolosim", "perc"),
("real", "Acoustic Flower King", "kit"),
("fx", "Apostasy Steam Noise", "perc"),
("fx", "DoReMinor Melodic", "perc"),
("fx", "Must Bend Tolotto", "drums"),
("ethno", "Sambalasala", "perc"),
("fx", "Kiss the Click", "perc"),
("retro", "Sweep Type 4tonight", "drums"),
("fx", "Noise Click Trap", "kit"),
("real", "Bend Timpanic", "drums"),
("retro", "dododrum", "kit"),
("fx", "Fast Sweep Melodic", "drums"),
("ethno", "Bella Balinese", "perc"),
("fx", "Noisy Royalty", "drums"),
("ethno", "Steely Melodic", "drums"),
("real", "Soft Acoustic", "drums"),
("real", "Tubular Bells and Triangle", "perc"),
("ethno", "Ultra Tribal Dance", "perc"),
("retro", "HeaHihat", "kit"),
("fx", "Click Gate and Vinyl", "kit"),
("real", "Double Snare", "kit"),
("real", "Hells Bells", "perc"),
("real", "Rototsthile", "drums"),
("retro", "Melodic Technocrat", "kit"),
("real", "Dull Dusty", "drums"),
("fx", "Retrophile Gated Noise", "drums"),
("ethno", "Real Cuba Conga Cola", "perc"),
("retro", "Retrograd", "drums"),
("fx", "GasaGate", "perc"),
("real", "Clap Trap", "drums"),
("real", "Krimsonite", "drums"),
("real", "Serious Decay", "kit"),
("ethno", "Dry Tribe", "drums"),
("fx", "Cinematikino", "perc"),
("fx", "Toy Ambulance", "kit"),
("retro", "Neophile", "drums"),
("retro", "Stabby Hip Hop", "kit"),
("real", "Retro Noise Reverb", "drums"),
("retro", "Ulam Spiral", "drums"),
("retro", "Sawkas Jungle Heat", "kit"),
("retro", "Knick Knock Knack", "drums"),
("real", "Bright Click Brush", "drums"),
("retro", "New Romantic Tight", "kit"),
("fx", "Intergalactic Battle", "perc"),
("retro", "Nosampled Drum", "drums"),
("retro", "Poor Tone", "kit"),
("fx", "Clicks&Pops", "drums"),
("fx", "Fat Gated Chattanoga", "drums"),
("real", "Retro Real Snap Snare", "drums"),
("ethno", "Slitz Box", "perc"),
("ethno", "Real Tommy Steel", "perc"),
("fx", "Macro Sweeper", "kit"),
("fx", "Darwin's Sex Machine", "kit"),
("real", "Apparatorium", "drums"),
("", "Default", ""))                              