import utility as u
import memory as mem
import data

def MOVLW(literal):
    """The contents of the W register are
added to the eight bit literal ’k’ and the
result is placed in the W register."""
    mem.w_register = literal


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


def DCFSZ(register, destination):
    return NotImplemented


def INCFSZ(register, destination):
    return NotImplemented


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



    binary = u.integer_to_binary(register)
    if binary[14-bit] == "0":
        print("Bit cleared")
    else:
        print("Bit not cleared")


def BTFSS(register, bit):
    binary = u.integer_to_binary(register)
    if binary[14-bit] == "1":
        print("Bit set")
    else:
        print("Bit not set")


if __name__ == '__main__':
    data.c_flag = False

    print(data.c_flag)
    print(hex(RLF(128, 0)))
    print(data.c_flag)
    print(u.integer_to_binary(RLF(1, 0)))
    print(data.c_flag)


    #print(u.integer_to_binary(BSF(0, 7)))

    #print(u.integer_to_binary(BCF(0xFF, 0)))



