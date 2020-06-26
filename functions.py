import pickle
import mido

import ndexceptions
from constants import *


def load():
    f = open(PICKLE_FILENAME, 'rb')
    d = pickle.load(f)
    f.close()
    return d

def save(root):
    with open(PICKLE_FILENAME, 'wb') as f:
        f.write(pickle.dumps(root))

def is_the_right_port(i):
    return MIDI_INTERFACE in i

def getMidiPort():
    # -> str
    f = filter(is_the_right_port, mido.get_input_names())
    try:
        return next(f)
    except StopIteration:
        raise ndexceptions.MidiInterfaceNotFound(MIDI_INTERFACE, mido.get_input_names())

def clearMidiMessages(port):
    # (port :: mido.IOPort ->
    for msg in port.iter_pending():
        print(msg)
    print("Queue clear.")

def programMatch(newCheck, progDict):
    # (newCheck :: int, dict<NDProg>) -> int
    # -1 is no match (ug)
    match = -1
    for k, v in progDict.items():
        if newCheck == v.chk:
            match = k
    return match