import data
import time
import actualSimulator as simu
import stack


flags = [0x02, 0x82, 0x3, 0x83, 0x4, 0x84, 0xa, 0x8a, 0xb, 0x8b]


def MOVLW(literal):
    """The contents of the W register are
added to the eight bit literal ’k’ and the
result is placed in the W register."""
    check(literal, 255)
    data.w_register = literal


def COMF(register, destination):
    val = data.data_memory[register] ^ 0xFF
    zero(val)
    writeInDestination(register, val, destination)


def ADDWF(register, destination):
    val = data.data_memory[register] + data.w_register
    carry(val)
    digitalCarry(data.data_memory[register], data.w_register, addf)
    zero(val % 256)
    writeInDestination(register, val % 256, destination)


def ANDWF(register, destination):
    val = data.data_memory[register] & data.w_register
    zero(val)
    writeInDestination(register, val, destination)


def CLRX(register, destination):
    data.setZF()

    # if(destination == 0):
    #     data.w_register = 0x0
    # elif(destination == 1):
    #     data.data_memory[register] = 0x0
    #
    writeInDestination(register, 0, destination)


def DECF(register, destination):
    val = data.data_memory[register] - 1
    zero(val)
    writeInDestination(register, val % 256, destination)


def INCF(register, destination):
    val = data.data_memory[register] + 1
    zero(val % 256)
    writeInDestination(register, val % 256, destination)


def IORWF(register, destination):
    val = data.data_memory[register] | data.w_register
    zero(val)
    writeInDestination(register, val, destination)


def IORLW(literal):
    val = data.w_register | literal
    zero(val)
    data.w_register = val


def ADDLW(literal):
    val = data.w_register + literal
    carry(val)
    digitalCarry(data.w_register, literal, addf)
    zero(val % 256)
    data.w_register = val % 256


def ANDLW(literal):
    val = data.w_register & literal
    zero(val)
    data.w_register = val


def SUBLW(literal):
    val = literal - data.w_register
    zero(val % 256)
    carry(-1 * val)
    digitalCarry(literal, data.w_register, subf)

    data.w_register = val % 256


def CALL(jumpAddress):
    stack.pushAddress(simu.index)
    simu.index = jumpAddress


def GOTO(jumpAddress):
    simu.index = jumpAddress


def MOVWF(register):
    #data.data_memory[register] = data.w_register
    writeInDestination(register,data.w_register,1)


def NOP():
    print("nop")


def MOVF(register, destination):
    val = data.data_memory[register]
    writeInDestination(register, val, destination)


def SUBWF(register, destination):
    val = data.data_memory[register] - data.w_register
    zero(val % 256)
    digitalCarry(data.data_memory[register], data.w_register, subf)
    carry(-1 * val)

    writeInDestination(register, val % 256, destination)


def DCFSZ(register, destination):
    val = data.data_memory[register] - 1
    simu.skipnext = (val == 0)
    writeInDestination(register, val, destination)


def INCFSZ(register, destination):
    val = data.data_memory[register] + 1
    simu.skipnext = (val == 0)
    writeInDestination(register, val, destination)


def RLF(register, destination):
    """Rotate right through carry"""
    c = data.getCF()
    data.clearCF() if data.data_memory[register] < 0x80 else data.setCF()
    val = c | ((data.data_memory[register] << 1) & 0xFF)
    writeInDestination(register, val, destination)


def RRF(register, destination):
    """Rotate right through carry"""
    #TODO Überprüfe auf Richtigkeit
    c = data.getCF() * 0x80
    data.clearCF() if (data.data_memory[register] % 2) == 0 else data.setCF()
    val = c | (register >> 1)
    writeInDestination(register, val, destination)


def BSF(register, bit):

    val = data.data_memory[register] | pow(2, bit)
    writeInDestination(register, val, 1)


def BCF(register, bit):

    val = data.data_memory[register] & (pow(2, bit) ^ 0b11111111)
    writeInDestination(register, val, 1)


def BTFSC(register, bit):
    test = data.data_memory[register] & (pow(2, bit))
    #simu.skipnext = (test == 0)
    if test == 0:
        simu.index += 1


def BTFSS(register, bit):
    test = data.data_memory[register] & (pow(2, bit))
    #simu.skipnext = (test > 0)
    if test == pow(2,bit):
        simu.index += 1


def RETURN():
    simu.index = stack.popAddress()


def RETLW(literal):
    data.w_register = literal
    simu.index = stack.popAddress()


def RETFIE():
    data.setGIE()
    simu.index = stack.popAddress()


def SLEEP(duration):
    time.sleep(duration)


def SWAPF(register, destination):
    op = data.data_memory[register]
    val = ((op & 0b11110000) >> 4) | ((op & 0b00001111) << 4)
    writeInDestination(register, val, destination)


def XORWF(register, destination):
    val = data.data_memory[register] ^ data.w_register
    zero(val)
    writeInDestination(register, val, destination)


def XORLW(literal):
    val = data.w_register ^ literal
    zero(val)
    data.w_register = val

def writeInDestination(register, val, destination):
    """Writes value in specified destination"""
    if destination == 0:
        data.w_register = val
    elif destination == 1:
        # mirroring shit
        if register in flags:
            data.data_memory[register % 0x80] = val
            data.data_memory[register % 0x80 + 0x80] = val
        else:
            data.data_memory[register] = val


def check(tocheck, max):
    if tocheck > max or tocheck < 0:
        raise ValueError(tocheck)


def zero(z):
    if z == 0:
        data.setZF()
    else:
        data.clearZF()


def carry(c):
    if c > 255 or c < 0:
        data.setCF()
    else:
        data.clearCF()


def addf(a, b):
    return (a + b) >> 4


def subf(a, b):
    return 1+((a-b) >> 4)


def digitalCarry(a, b, f):
    a &= 0x0F
    b &= 0x0F
    a = f(a, b)

    data.setDCF() if a == 1 else data.clearDCF()


if __name__ == '__main__':
    data.__innit__()
    digitalCarry(0x0, 0xF, addf)


