from nd1manager import *
from programbrowser import *

# Test Data Functions
#

def testChannel(i):
    # (i :: int) -> NDChannel
    return NDChannel(f"Test Channel {i + 1}", INSTRUMENTS[i % 4], False)

def generateTestChannels(n):
    # (n :: int) -> list<NDChannel>
    o = n * 4
    return [testChannel(i) for i in range(o, o + 4)]

def testProgram(i):
    # (n = int) -> NDProgram
    return NDProg(f"{FILE_PREFIX}/prog{i + 1}",
                     f"Test Program {i + 1}",
                     STYLE[i % 4],
                     CATEGORY[i // 10],
                     generateTestChannels(i),
                     False, False)

def generateTestPrograms(n):
    # (n :: int) -> dict<NDProg>
    return {i + 1 : testProgram(i) for i in range(0, n)}
        
def generateTestData(n):
    # (ch_count :: int) -> DataRoot
    pDict = generateTestPrograms(n)
    mem = list(range(1, n+1))
    return DataRoot(pDict, mem, n)


