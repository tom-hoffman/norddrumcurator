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
    # (file :: str, chk :: int, name :: str, style :: str, 
    #  category :: str, key :: str, channels :: list<NDChannel>,
    #  favorite :: bool, preset :: bool) -> NDProg
    def __init__(self, file, chk, name, style, category, key,
                 channels = [], favorite = False, preset = False):
        self.file = file
        self.chk = chk
        self.name = name
        self.style = style
        self.category = category
        self.key = key
        self.channels = channels
        self.favorite = favorite
        self.preset = preset
    def __repr__(self):
        return f"NDProg: {self.name} with {len(self.channels)} channels."

class DataRoot:
    '''Top level container for the data objects.'''
    # NOTE: The memory list starts with a dummy value at index 0.
    def __init__(self, programs: Dict[int, NDProg],
                 memory: List[int], program_counter: int):
        self.programs = programs
        self.memory = memory
        self.program_counter = program_counter
    def __repr__(self):
        return f"Programs -> {self.programs}; Memory -> {self.memory}"
    def __str__(self):
        return f"DataRoot has {len(self.programs)} programs on disc and {len(self.memory)} in memory."
    def addProgram(self, program: NDProg):
        p = self.program_counter + 1
        self.programs[p] = program
        self.program_counter = p
