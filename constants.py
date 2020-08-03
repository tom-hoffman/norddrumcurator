import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


# model constants
STYLES = ("real", "retro", "ethno", "fx")
CATEGORIES = ("drums", "percussion", "kit")
INSTRUMENTS = ("kick", "snare", "rack tom", "floor tom",
               "closed hat", "open hat", "other hat",
               "crash", "ride", "cowbell", "woodblock",
               "steel-drum", "ping", "sci fi", "unknown")
PERFORMANCE_GROUPS = ["Live 1", "Live 2", "My Kit"] + list(STYLES)
KEYS = ("None", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
CACHE_STATUSES = ("checked", "dirty", "unknown")
CHANNEL_NAMES = ("CH1", "CH2", "CH3", "CH4")

# file constants
PICKLE_FILENAME = "drums.pickle"
FILE_PREFIX = "programs/"

# MIDI constants
MIDI_INTERFACE = "UM-ONE:UM-ONE MIDI 1"
ACTUAL_CHANNEL = 1 # the one on the ND display.
ND_CHANNEL = ACTUAL_CHANNEL - 1
CHANNEL_NUMBERS = (36, 38, 46, 42)
VELOCITY = 20

# UI Cconstants
COLUMN_HEADERS = ("Name", "Style/Instrument", "Category")
ACTIONS = ("Pull", "Push")
CSS_PATH = 'gtkstyle.css'
CSS = Gtk.CssProvider()
CSS.load_from_path(CSS_PATH)
SCREEN = Gdk.Screen.get_default()
PRIORITY = Gtk.STYLE_PROVIDER_PRIORITY_USER
CONTEXT = Gtk.StyleContext()
CONTEXT.add_provider_for_screen(SCREEN, CSS, PRIORITY)
