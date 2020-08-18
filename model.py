from typing import List, Dict, Tuple

import mido

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
                 instruments: List[str] = 4 *["?"],
                 key: str = "", 
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

class DataRoot:
    '''Top level container for the data objects.'''
    def __init__(self,
                 programs: Tuple[NDProg] = (),
                 memory: List[int] = [-1] * 99,
                 cache_status: List[str] = ["dirty"] * 99,
                 program_counter: int = 0):
        self.programs = programs
        self.memory = memory
        self.cache_status = cache_status
        self.program_counter = program_counter
        
    def __repr__(self):
        return f"DataRoot has {len(self.programs)} programs on disc."

    def addProgram(self, p: NDProg) -> Tuple[NDProg]:
        new = self.programs + (p,)
        self.program_counter += 1
        return new

    def load_factory_soundbank(self):
        bank = mido.read_syx_file(FACTORY_SOUNDBANK)
        for i in range(81):
            mess = functions.resetSysExIndex(bank[i])
            ID = self.program_counter
            description = FACTORY_SOUNDBANK_METADATA[i][1]
            name = functions.program_file_name(ID, description)
            check = functions.messageChecksum(mess)
            style = FACTORY_SOUNDBANK_METADATA[i][0]
            cat = FACTORY_SOUNDBANK_METADATA[i][2]
            prog = NDProg(ID,
                          name,
                          check,
                          description,
                          tags = [style, cat, "nord"])
                                                      
            self.programs = self.addProgram(prog)
            functions.save_sysex(name, mess)

    def save(self, location: str = PICKLE_FILENAME):
        with open(location, 'wb') as f:
            f.write(pickle.dumps(self))