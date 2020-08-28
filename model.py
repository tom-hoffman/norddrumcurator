from typing import List, Dict, Tuple

import mido
import pickle

import functions
from constants import *

#
# Data model
#

class NDProg:
    '''A Nord Drum 1 Program.'''
    def __init__(self,
                 ID: int,
                 file: str,
                 chk: int,
                 description: str,
                 replaces: int = -1,
                 instruments: List[str] = 4 * ["?"], 
                 key: str = "?", 
                 tags: List[str] = []):
        self.ID = ID
        self.file = file
        self.chk = chk
        self.description = description
        self.replaces = replaces
        self.instruments = instruments
        self.key = key
        self.tags = tags
    def __repr__(self):
        return f"NDProg: {self.description}."

UNKNOWN_PLEASURES = NDProg(0,
                           '../unknown_pleasures.syx',
                           2175622434,
                           "Unknown Pleasures",
                           key = "C#")

class DataRoot:
    '''Top level container for the data objects.'''
    def __init__(self,
                 programs: List[NDProg] = [UNKNOWN_PLEASURES],
                 memory: List[int] = [0] * 99, # clean this up.
                 cache_status: List[str] = ["dirty"] * 99,
                 program_counter: int = 1):
        self.programs = programs
        self.memory = memory
        self.cache_status = cache_status
        self.program_counter = program_counter
        
    def __repr__(self):
        return f"DataRoot has {len(self.programs)} programs on disc."

    def addProgram(self,
                   p: NDProg,
                   m: mido.Message):
        self.programs.append(p)
        self.program_counter += 1
        functions.save_sysex(p.file, m)

    def save(self, location: str = PICKLE_FILENAME):
    # Saves data root.
        with open(location, 'wb') as f:
            f.write(pickle.dumps(self))

    def findDuplicateProgram(self, chk: int) -> int:
        # returns the ID of the matching program.
        for p in self.programs:
            if p.chk == chk:
                return p.ID
        return None

    def findProgram(self, prog_id: int) -> NDProg:
        it = None
        for p in self.programs:
            if prog_id == p.ID:
                it = p
        return it
    
    def programFromSlot(self,
                        slot: int) -> NDProg:
        return self.findProgram(self.memory[slot])

    def load_factory_soundbank(self):
        bank = mido.read_syx_file(FACTORY_SOUNDBANK)
        for i in range(81):
            mess = functions.allMessageToOne(bank[i])
            ID = self.program_counter
            description = FACTORY_SOUNDBANK_METADATA[i][1]
            name = functions.program_file_name(ID)
            check = functions.messageChecksum(mess)
            style = FACTORY_SOUNDBANK_METADATA[i][0]
            cat = FACTORY_SOUNDBANK_METADATA[i][2]
            prog = NDProg(ID,
                          name,
                          check,
                          description,
                          tags = [style, cat, "nord"])                    
            self.addProgram(prog, mess)
