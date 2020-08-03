from model import *
from constants import *

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
                  0,
                  f"Test Program {i + 1}",
                  STYLES[i % 4],
                  CATEGORIES[i % 3],
                  None,
                  generateTestChannels(i),
                  False, False)

def generateTestPrograms(n):
    # (n :: int) -> dict<NDProg>
    d = {i + 1 : testProgram(i) for i in range(0, n)}
    d[0] = UNKNOWN_PLEASURES
    return d
        
def generateTestData(n):
    # (ch_count :: int) -> DataRoot
    pDict = generateTestPrograms(n)
    mem = list(range(1, n+1))
    caches = ['dirty'] * n
    return DataRoot(pDict, mem, caches, n)



