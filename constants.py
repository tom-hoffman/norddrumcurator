import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

PICKLE_FILENAME = "drums.pickle"
FILE_PREFIX = "programs/"

STYLES = ("real", "retro", "ethno", "fx")
CATEGORIES = ("drums", "percussion", "kit")
INSTRUMENTS = ("kick", "snare", "rack tom", "floor tom",
               "closed hat", "open hat", "other hat",
               "crash", "ride", "cowbell", "woodblock",
               "steel-drum", "ping", "sci fi", "unknown")
PERFORMANCE_GROUPS = ["Live 1", "Live 2", "My Kit"] + list(STYLES)
KEYS = ("None", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
CACHE_STATUSES = ("checked", "dirty", "unknown")
COLUMN_HEADERS = ("Name", "Style/Instrument", "Category")
ACTIONS = ("Pull", "Push")
CHANNEL_NAMES = ("CH1", "CH2", "CH3", "CH4")


MIDI_INTERFACE = "UM-ONE:UM-ONE MIDI 1"
ND_CHANNEL = 1

CSS_PATH = 'gtkstyle.css'
CSS = Gtk.CssProvider()
CSS.load_from_path(CSS_PATH)
SCREEN = Gdk.Screen.get_default()
PRIORITY = Gtk.STYLE_PROVIDER_PRIORITY_USER
CONTEXT = Gtk.StyleContext()
CONTEXT.add_provider_for_screen(SCREEN, CSS, PRIORITY)
