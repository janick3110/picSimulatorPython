


stackpointer = 0
stack = [int] * 8


def incrementSP():

    stack.stackpointer = (stack.stackpointer + 1) % 8

def decrementSP(self):
    self.stackpointer = (self.stackpointer - 1) % 8

def doCall(self, i):
    self.stack[self.stackpointer] = i
    incrementSP()

def ret(self):
    decrementSP()

