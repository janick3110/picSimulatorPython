stackpointer = 0
stack = [int] * 8


def incrementSP():
    global stackpointer
    stackpointer = (stackpointer + 1) % 8


def decrementSP():
    global stackpointer
    stackpointer = (stackpointer - 1) % 8


def pushAddress(i):
    stack[stackpointer] = i
    incrementSP()


def popAddress():
    out = stack[stackpointer]
    decrementSP()
    return out
