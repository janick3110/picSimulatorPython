
import commands as c




jumpAddress = None
fileRegAddress = None
constant = None
bitAddress = None
destination = None


def decode(arg):
    getParameters(arg)

    if(arg == 0x64):
        #CLRWDT
        raise NotImplemented
    elif(arg == 0x9):
        #RETFIE
        raise NotImplemented
    elif(arg == 0x8):
        #RETURN
        raise NotImplemented
    elif(arg == 0x63):
        #SLEEP
        c.SLEEP(15)
    else:
        if(arg>>12 == 0b00):
            decodeByteOriented(arg>>8)
        elif(arg>>12 == 0b01):
            decodeBitOriented(arg>>10)
        elif(arg>>12 == 0b10):
            if(arg>>11 == 0b100):
                #CALL
                raise NotImplemented
            elif(arg>>11 == 0b101):
                #GOTO
                raise NotImplemented
        elif(arg>>12 == 0b11):
            decodeSpecialCases(arg >> 8)

def getParameters(arg):
    global jumpAddress
    jumpAddress = (arg & 0x7FF)
    global fileRegAddress
    fileRegAddress = (arg & 0x7F)
    global constant
    constant = (arg & 0xFF)
    global bitAddress
    bitAddress = (arg & 0x380) >> 7
    global destination
    destination = (arg & 0x80) >> 7

    print("jump " + str(jumpAddress))
    print("file " + str(fileRegAddress))
    print("const " + str(constant))
    print("bitad " + str(bitAddress))
    print("desti " + str(destination))


def decodeByteOriented(arg):
    if(arg == 0b000111):
        #ADDWF
        c.ADDWF(fileRegAddress, destination)
    elif(arg == 0b000101):
        #ANDWF
        c.ADDWF(fileRegAddress, destination)
    elif(arg == 0b000001):
        #CLRF&CLRW
        c.CLRX(fileRegAddress, destination)
    elif(arg == 0b001001):
        #COMF
        c.COMF(fileRegAddress, destination)
    elif(arg == 0b000011):
        #DECF
        c.DECF(fileRegAddress, destination)
    elif(arg == 0b001011):
        #DCFSZ
        c.DCFSZ(fileRegAddress, destination)
    elif(arg == 0b001010):
        #INCF
        c.INCF(fileRegAddress, destination)
    elif(arg == 0b001111):
        #INCFSZ
        c.INCFSZ(fileRegAddress, destination)
    elif(arg == 0b000100):
        #IORWF
        c.IORWF(fileRegAddress, destination)
    elif(arg == 0b001000):
        #MOVF
        c.MOVF(fileRegAddress, destination)
    elif(arg == 0b000000):
        # MOVWF / NOP
        if(destination == 0):
            c.NOP()
        elif(destination == 1):
            c.MOVWF(fileRegAddress)
    elif(arg == 0b001101):
        #RLF
        c.RLF(fileRegAddress, destination)
    elif(arg == 0b001100):
        #RRF
        c.RRF(fileRegAddress, destination)
    elif(arg == 0b000010):
        #SUBWF
        c.SUBWF(fileRegAddress, destination)
    elif(arg == 0b001110):
        #SWAPF
        c.SUBWF(fileRegAddress, destination)
    elif(arg == 0b000110):
        #XORWF
        c.XORWF(fileRegAddress, destination)

def decodeBitOriented(arg):

    if(arg == 0b0100):
        #BCF
        c.BCF(fileRegAddress, bitAddress)
    elif(arg == 0b0101):
        #BSF
        c.BSF(fileRegAddress, bitAddress)
    elif(arg == 0b0110):
        #BTFSC
        c.BTFSC(fileRegAddress, bitAddress)
    elif(arg == 0b0111):
        #BTFSS
        c.BTFSS(fileRegAddress, bitAddress)

def decodeSpecialCases(arg):
    if(arg == 0b111001):
        #ANDLW
        c.ANDLW(constant)
    elif(arg == 0b111000):
        #IORLW
        c.IORLW(constant)
    elif(arg == 0b111010):
        #XORLW
        c.XORLW(constant)
    elif(arg>>1 == 0b11110):
        #SUBLW
        c.SUBLW(constant)
    elif(arg>>1 == 0b11111):
        #ADDLW
        c.ADDLW(constant)
    elif(arg>>2 == 0b1100):
        #MOVLW
        c.MOVLW(constant)
    elif(arg>>2 == 0b1101):
        #RETLW
        raise NotImplemented



