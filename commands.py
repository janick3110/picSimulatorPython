import utility as u
import memory as mem

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


def RLF(register, destination):
    return NotImplemented


def RRF(register, destination):
    return NotImplemented


def BSF(register, bit):
    binaryList = list(u.integer_to_binary(register))
    binaryList[14-bit] = "1"
    binary = "".join(binaryList)
    print(u.binary_to_integer(binary))


def BCF(register, bit):
    binaryList = list(u.integer_to_binary(register))
    binaryList[14 - bit] = "0"
    binary = "".join(binaryList)
    print(u.binary_to_integer(binary))


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
    print(u.integer_to_binary(2))



