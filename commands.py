import memory as mem
import data
import time
import actualSimulator as simu


def MOVLW(literal):
    """The contents of the W register are
added to the eight bit literal ’k’ and the
result is placed in the W register."""
    data.w_register = literal


def COMF(register, destination):
    val = ~data.data_memory[register]
    WriteInDestination(register, val, destination)


def ADDWF(register, destination):
    val = data.data_memory[register] + data.w_register
    WriteInDestination(register, val, destination)


def ANDWF(register, destination):
    val = data.data_memory[register] & data.w_register
    WriteInDestination(register, val, destination)


def CLRX(register, destination):
    if(destination == 0):
        data.w_register = 0x0
    elif(destination == 1):
        data.data_memory[register] = 0x0


def DECF(register, destination):
    val = data.data_memory[register] - 1
    WriteInDestination(register, val, destination)


def INCF(register, destination):
    val = data.data_memory[register] + 1
    WriteInDestination(register, val, destination)


def IORWF(register, destination):
    val = data.data_memory[register] | data.w_register
    WriteInDestination(register, val, destination)


def IORLW(literal):
    data.w_register |= literal


def ADDLW(literal):
    data.w_register += literal


def ANDLW(literal):
    data.w_register &= literal


def SUBLW(literal):
    data.w_register = literal - data.w_register


def CALL(subroutine):
    return NotImplemented


def GOTO(label):
    return NotImplemented


def MOVWF(register):
    data.data_memory[register] = data.w_register


def NOP():
    print("nop")


def MOVF(register, destination):
    val = data.data_memory[register]
    WriteInDestination(register, val, destination)


def SUBWF(register, destination):
    val = data.data_memory[register] - data.w_register
    WriteInDestination(register, val, destination)


def DCFSZ(register, destination):
    val = data.data_memory[register] - 1
    simu.skipnext = (val == 0)
    WriteInDestination(register, val, destination)


def INCFSZ(register, destination):
    val = data.data_memory[register] + 1
    simu.skipnext = (val == 0)
    WriteInDestination(register, val, destination)


def RLF(register, destination):
    """Rotate right through carry"""
    c = 1 if data.c_flag else 0
    data.c_flag = False if data.data_memory[register] < 0x80 else True
    val = c | ((data.data_memory[register] << 1) & 0xFF)
    WriteInDestination(register, val, destination)


def RRF(register, destination):
    """Rotate right through carry"""
    c = 0x80 if data.c_flag else 0
    data.c_flag = False if (data.data_memory[register] % 2) == 0 else True
    val = c | (register >> 1)
    WriteInDestination(register, val, destination)


def BSF(register, bit):

    val = data.data_memory[register] | pow(2, bit)
    data.data_memory[register] = val


def BCF(register, bit):

    val = data.data_memory[register] & (pow(2, bit) ^ 0b11111111)
    data.data_memory[register] = val


def BTFSC(register, bit):
    test = data.data_memory[register] & (pow(2, bit))
    simu.skipnext = (test == 0)


def BTFSS(register, bit):
    test = data.data_memory[register] & (pow(2, bit))
    simu.skipnext = (test > 0)


def SLEEP(duration):
    time.sleep(duration)


def SWAPF(register, destination):
    op = data.data_memory[register]
    val = (op >> 4) | ((op & 0b00001111) << 4)
    WriteInDestination(register, val, destination)


def XORWF(register, destination):
    val = data.data_memory[register] ^ data.w_register
    WriteInDestination(register, val, destination)


def XORLW(literal):
    data.w_register ^= literal


def WriteInDestination(register, val, destination):
    """Writes value in specified destination"""
    if destination == 0:
        data.w_register = val
    elif destination == 1:
        data.data_memory[register] = val


if __name__ == '__main__':
    print(bin(0b11110000))
    print(bin(COMF(0b11110000, 0)))

    print(bin(pow(2, 12)))
    print(bin(~(pow(2, 12))))

    print(bin(0b11111111 ^ 0b11110000))


