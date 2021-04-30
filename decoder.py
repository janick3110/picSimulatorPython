
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
    elif(arg == 0x9):
        #RETFIE
    elif(arg == 0x8):
        #RETURN
    elif(arg == 0x63):
        #SLEEP
    else:
        if(arg>>12 == 0b00):
            decodeByteOriented(arg>>8)
        elif(arg>>12 == 0b01):
            decodeBitOriented(arg>>10)
        elif(arg>>12 == 0b10):
            if(arg>>11 == 0b100):
                #CALL
            elif(arg>>11 == 0b101):
                #GOTO
        elif(arg>>12 == 0b11):
            decodeSnowflake(arg>>8)

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
    elif(arg == 0b000101):
        #ANDWF
    elif(arg == 0b000001):
        #CLRF&CLRW
    elif(arg == 0b001001):
        #COMF
    elif(arg == 0b000011):
        #DECF
    elif(arg == 0b001011):
        #DECFSZ
    elif(arg == 0b001010):
        #INCF
    elif(arg == 0b001111):
        #INCFSZ
    elif(arg == 0b000100):
        #IORWF
    elif(arg == 0b001000):
        #MOVF
    elif(arg == 0b000000):
        #MOVWF / NOP
    elif(arg == 0b001101):
        #RLF
    elif(arg == 0b001100):
        #RRF
    elif(arg == 0b000010):
        #SUBWF
    elif(arg == 0b001110):
        #SWAPF
    elif(arg == 0b000110):
        #XORWF

def decodeBitOriented(arg):

    if(arg == 0b0100):
        #BCF
    elif(arg == 0b0101):
        #BSF
    elif(arg == 0b0110):
        #BTFSC
    elif(arg == 0b0111):
        #BTFSS

def decodeSnowflake(arg):
    if(arg == 0b111001):
        #ANDLW
    elif(arg == 0b111000):
        #IORLW
    elif(arg == 0b111010):
        #XORLW
    elif(arg>>1 == 0b11110):
        #SUBLW
    elif(arg>>1 == 0b11111):
        #ADDLW
    elif(arg>>2 == 0b1100):
        #MOVLW
    elif(arg>>2 == 0b1101):
        #RETLW


if __name__ == '__main__':
    decode(0x0084)
    print("-----")
    decode(0x3005)
    print("-----")
    decode(0x080F)
