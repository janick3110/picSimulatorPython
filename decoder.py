
import commands as c

jumpAdress = 0
fileRegAdress = 0
constant = 0
bitAdress = 0
destination = 0

def decode(arg):
    getParameters(arg)

    if(arg == 0x64):
        #CLRWDT
        return NotImplemented
    elif(arg == 0x9):
        #RETFIE
        return NotImplemented
    elif(arg == 0x8):
        #RETURN
        return NotImplemented
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
                return NotImplemented
            elif(arg>>11 == 0b101):
                #GOTO
                return NotImplemented
        elif(arg>>12 == 0b11):
            decodeSpecialCases(arg >> 8)

def getParameters(arg):
    jumpAdress = (arg & 0x7FF)
    fileRegAdress = (arg & 0x7F)
    constant = (arg & 0xFF)
    bitAdress = (arg & 0x380)>>7
    destination = (arg & 0x80)>>7

    print("jump " + str(jumpAdress))
    print("file " + str(fileRegAdress))
    print("const " + str(constant))
    print("bitad " + str(bitAdress))
    print("desti " + str(destination))


def decodeByteOriented(arg):
    if(arg == 0b000111):
        #ADDWF
        c.ADDWF(fileRegAdress,destination)
    elif(arg == 0b000101):
        #ANDWF
        c.ADDWF(fileRegAdress,destination)
    elif(arg == 0b000001):
        #CLRF&CLRW
        c.CLRX(fileRegAdress,destination)
    elif(arg == 0b001001):
        #COMF
        c.COMF(fileRegAdress,destination)
    elif(arg == 0b000011):
        #DECF
        c.DECF(fileRegAdress,destination)
    elif(arg == 0b001011):
        #DCFSZ
        c.DCFSZ(fileRegAdress,destination)
    elif(arg == 0b001010):
        #INCF
        c.INCF(fileRegAdress,destination)
    elif(arg == 0b001111):
        #INCFSZ
        c.INCFSZ(fileRegAdress,destination)
    elif(arg == 0b000100):
        #IORWF
        c.IORWF(fileRegAdress,destination)
    elif(arg == 0b001000):
        #MOVF
        c.MOVF(fileRegAdress,destination)
    elif(arg == 0b000000):
        # MOVWF / NOP
        if(destination == 0):
            c.NOP()
        elif(destination == 1):
            c.MOVWF(fileRegAdress)
    elif(arg == 0b001101):
        #RLF
        c.RLF(fileRegAdress, destination)
    elif(arg == 0b001100):
        #RRF
        c.RRF(fileRegAdress, destination)
    elif(arg == 0b000010):
        #SUBWF
        c.SUBWF(fileRegAdress,destination)
    elif(arg == 0b001110):
        #SWAPF
        c.SUBWF(fileRegAdress,destination)
    elif(arg == 0b000110):
        #XORWF
        c.XORWF(fileRegAdress,destination)

def decodeBitOriented(arg):

    if(arg == 0b0100):
        #BCF
        c.BCF(fileRegAdress,bitAdress)
    elif(arg == 0b0101):
        #BSF
        c.BSF(fileRegAdress, bitAdress)
    elif(arg == 0b0110):
        #BTFSC
        c.BTFSC(fileRegAdress, bitAdress)
    elif(arg == 0b0111):
        #BTFSS
        c.BTFSS(fileRegAdress, bitAdress)

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
        return NotImplemented



