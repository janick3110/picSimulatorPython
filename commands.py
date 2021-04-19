def MOVLW(literal):
    return NotImplemented


def ADDLW(literal):
    return NotImplemented


def SUBLW(literal):
    return NotImplemented


def CALL(subroutine):
    return NotImplemented


def GOTO(label):
    return NotImplemented


def MOVWF(destination):
    return NotImplemented


def MOVF(origin, destination):
    return NotImplemented


def SUBWF(register, destination):
    return NotImplemented


def DCFSZ(register, destination):
    return NotImplemented


def INCFSZ(register, destination):
    return NotImplemented


def RLF(register, destination):
    return NotImplemented


def RRF(register, destination):
    return NotImplemented


def BSF(register, bit):
    register[bit] = 1


def BCF(register, bit):
    register[bit] = 1


def BTFSC(register, bit):
    return NotImplemented


def BTFSS(register, bit):
    return NotImplemented
