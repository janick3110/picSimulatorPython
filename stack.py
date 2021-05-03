stackpointer = 7
stack = []


def incrementSP():
    global stackpointer
    stackpointer = (stackpointer + 1) % 8


def decrementSP():
    global stackpointer
    stackpointer = (stackpointer - 1) % 8


def pushAddress(i):
    incrementSP()
    stack[stackpointer] = i



def popAddress():
    out = stack[stackpointer]
    decrementSP()
    return out
