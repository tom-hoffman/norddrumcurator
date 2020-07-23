class NDError(Exception):
    pass

class MidiInterfaceNotFound(NDError):
    def __init__(self, correct, l):
        NDError.__init__()
        self.correct = correct
        self.l = l
    def __str__(self):
        return f"{self.correct} not listed in active midi inputs: {self.l}"