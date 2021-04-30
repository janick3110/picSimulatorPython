import memory as mem
import data
import time

def MOVLW(literal):
    """The contents of the W register are
added to the eight bit literal ’k’ and the
result is placed in the W register."""
    mem.w_register = literal

def COMF(registerVal, destination):
    registerVal = ~registerVal

def ADDLW(literal):
    mem.w_register += literal


def SUBLW(literal):
    mem.w_register -= literal


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


def DCFSZ(registerVal, destination):
    registerVal -= 1

    if registerVal == 0:
        return True
    else:
        return False


def INCFSZ(registerVal, destination):
    registerVal += 1

    if registerVal == 0:
        return True
    else:
        return False


def RLF(registerVal, destination):
    """Rotate right through carry"""
    c = 1 if data.c_flag else 0
    data.c_flag = False if registerVal < 0x80 else True
    output = c | ((registerVal << 1) & 0xFF)
    return output

def RRF(registerVal, destination):
    """Rotate right through carry"""
    c = 0x80 if data.c_flag else 0
    data.c_flag = False if (registerVal % 2) == 0 else True
    output = c | (registerVal >> 1)

    return output

def BSF(registerVal, bit):

    output = registerVal | pow(2, bit)
    return output

def BCF(registerVal, bit):

    output = registerVal & ~(pow(2, bit))
    return output


def BTFSC(register, bit):
    test = register & (pow(2,bit))
    if test == pow(2,bit):
        return False
    else:
        return True


def BTFSS(register, bit):
    test = register & (pow(2,bit))
    if test == pow(2,bit):
        return True
    else:
        return False

def SLEEP(duration):
    time.sleep(duration)

if __name__ == '__main__':
    print(time.time())
    SLEEP(10)
    print(time.time())



