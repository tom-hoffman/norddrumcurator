from typing import List, Dict

#
# Data model
#

class NDChannel:
    '''A Nord Drum 1 Channel.'''
    def __init__(self, name: str = "",
                 instrument: str = "",
                 favorite: bool = False):
        self.name = name
        self.instrument = instrument
        self.favorite = favorite
    def __repr__(self):
        return f"{self.name} {self.instrument}."

class NDProg:
    '''A Nord Drum 1 Program.'''
    # (file :: str, chk :: int, name :: str, style :: str, category :: str,
    #  channels :: list<NDChannel>, preset :: bool) -> NDProg
    def __init__(self, file, chk, name, style, category,
                 channels = [], preset = False, favorite = False):
        self.file = file
        self.chk = chk
        self.name = name
        self.style = style
        self.category = category
        self.channels = channels
        self.preset = preset
        self.favorite = favorite
    def __repr__(self):
        return f"NDProg: {self.name} with {len(self.channels)} channels."

class DataRoot:
    '''Top level container for the data objects.'''
    def __init__(self, programs: Dict[int, NDProg],
                 memory: List[int], program_counter: int = 0):
        self.programs = programs
        self.memory = memory
        self.program_counter = program_counter
    def __repr__(self):
        return f"DataRoot has {len(self.programs)} programs on disc and {len(self.memory)} in memory."
    def addProgram(self, program: NDProg):
        p = self.program_counter + 1
        self.programs[p] = program
        self.program_counter = p
