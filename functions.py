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
    print(f"Writing: {sysex}")
    mido.write_syx_file(FILE_PREFIX + name, [sysex])

def read_sysex(file_name: str) -> mido.Message:
    return mido.read_syx_file(FILE_PREFIX + file_name)[0]

def sendMidiProgramChange(port: mido.ports.IOPort,
                    program: int):
    # You need to subtract one from the program because computers.
    port.send(mido.Message('program_change',
                           channel = ND_CHANNEL,
                           program = (program - 1)))

def pushProgram(port: mido.ports.IOPort,
                file: str):
    syx = read_sysex(file)
    print(syx)
    #port.send(mido.Message('sysex', data = [syx.data]))
    port.send(syx)

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
