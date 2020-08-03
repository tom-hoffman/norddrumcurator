import pickle
from typing import List, Dict

import mido

import ndexceptions
import model
from constants import *

# Load/save data root

def load():
    f = open(PICKLE_FILENAME, 'rb')
    d = pickle.load(f)
    f.close()
    return d

def save(root: model.DataRoot):
    with open(PICKLE_FILENAME, 'wb') as f:
        f.write(pickle.dumps(root))

# MIDI functions

def is_the_right_port(i: List):
    return MIDI_INTERFACE in i

def getMidiPort():
    # -> str
    f = filter(is_the_right_port, mido.get_input_names())
    try:
        return next(f)
    except StopIteration:
        raise ndexceptions.MidiInterfaceNotFound(MIDI_INTERFACE, mido.get_input_names())

def clearMidiMessages(port):
    for msg in port.iter_pending():
        print(msg)
    print("Queue clear.")

def save_sysex(name: str, sysex: mido.Message):
    with open(FILE_PREFIX + name, 'xb') as f:
        f.write(sysex.bin())

def read_sysex(file_name: str) -> mido.Message:
    with open(FILE_PREFIX + file_name, 'rb') as f:
        return f.read()

def sendMidiProgramChange(port: mido.ports.IOPort,
                    program: int):
    # You need to subtract one from the program because computers.
    port.send(mido.Message('program_change',
                           channel = ND_CHANNEL,
                           program = (program - 1)))

def pushProgram(port: mido.ports.IOPort,
                file: str):
    print(file)

def midiConfirm(port: mido.ports.IOPort):
    for n in CHANNEL_NUMBERS:
        port.send(mido.Message('note_on',
                               note = n,
                               velocity = VELOCITY,
                               channel = ND_CHANNEL))

# Misc utility functions.

def programMatch(newCheck: int, progDict: Dict):
    # -1 is no match (ug)
    match = -1
    for k, v in progDict.items():
        if newCheck == v.chk:
            match = k
    return match
