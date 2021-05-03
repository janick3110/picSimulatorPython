import commands as c


##Bank A
# TMR0
# PCL
# Status
# FSR
# PortA
# PortB
# EEDATA
# EEADR
# PCLATH
# INTCON

##Bank B
# Option
# PCL
# STATUS
# FSR
# TRISA
# TRISB
# EECON1
# EECON2
# PCLATH
# INTCON


w_register = 0

data_memory = []


def __innit__():
    """Initialize data memory"""
    for i in range(0xFF):
        data_memory.append(0)
    power_on_or_reset()
    print("Initialization done")


def power_on_or_reset():
    # BANK A
    data_memory[0x00] = 0
    data_memory[0x01] = data_memory[0x01] & 0xFF
    data_memory[0x02] = 0
    data_memory[0x03] = data_memory[0x02] & 0x1F
    data_memory[0x04] = data_memory[0x04] & 0xFF
    data_memory[0x05] = data_memory[0x05] & 0x1F
    data_memory[0x06] = data_memory[0x06] & 0xFF
    data_memory[0x07] = 0
    data_memory[0x08] = data_memory[0x08] & 0xFF
    data_memory[0x09] = data_memory[0x09] & 0xFF
    data_memory[0x0A] = 0
    data_memory[0x0B] = data_memory[0x0B] & 0x1

    data_memory[0x80] = 0
    data_memory[0x81] = 0xFF
    data_memory[0x82] = 0
    data_memory[0x83] = data_memory[0x83] & 0x1F
    data_memory[0x84] = data_memory[0x83] & 0xFF
    data_memory[0x85] = 0x1F
    data_memory[0x86] = 0xFF
    data_memory[0x87] = 0
    data_memory[0x88] = data_memory[0x83] & 0x8
    data_memory[0x89] = 0
    data_memory[0x8A] = 0  # check again in sheet I'm not sure
    data_memory[0x8B] = data_memory[0x8B] & 0x1  # check again in sheet I'm not sure


def other_reset():
    # BANK A
    data_memory[0x00] = 0
    data_memory[0x01] = data_memory[0x01] & 0xFF
    data_memory[0x02] = 0
    data_memory[0x03] = data_memory[0x02] & 0x1F
    data_memory[0x04] = data_memory[0x04] & 0xFF
    data_memory[0x05] = data_memory[0x05] & 0x1F
    data_memory[0x06] = data_memory[0x06] & 0xFF
    data_memory[0x07] = 0
    data_memory[0x08] = data_memory[0x08] & 0xFF
    data_memory[0x09] = data_memory[0x09] & 0xFF
    data_memory[0x0A] = 0
    data_memory[0x0B] = data_memory[0x0B] & 0x1

    data_memory[0x80] = 0
    data_memory[0x81] = 0xFF
    data_memory[0x82] = 0
    data_memory[0x83] = data_memory[0x83] & 0x1F
    data_memory[0x84] = data_memory[0x83] & 0xFF
    data_memory[0x85] = 0x1F
    data_memory[0x86] = 0xFF
    data_memory[0x87] = 0
    data_memory[0x88] = data_memory[0x83] & 0x8
    data_memory[0x89] = 0
    data_memory[0x8A] = 0  # check again in sheet I'm not sure
    data_memory[0x8B] = data_memory[0x8B] & 0x1  # check again in sheet I'm not sure


def getCF():
    return data_memory[0x03] & 0x01


def getDCF():
    return (data_memory[0x03] & 0x02) >> 1


def getZF():
    return (data_memory[0x03] & 0x04) >> 2


def setCF():
    c.BSF(0x03, 0)


def clearCF():
    c.BCF(0x03, 0)


def setDCF():
    c.BSF(0x03, 1)


def clearDCF():
    c.BCF(0x03, 1)


def setZF():
    c.BSF(0x03, 2)


def clearZF():
    c.BCF(0x03, 2)


def setGIE():
    c.BSF(0x0B, 7)


def clearGIE():
    c.BCF(0x0B, 7)


def checkFlag(c):
    if c not in range(0, 2):
        raise ValueError(c)


if __name__ == '__main__':
    checkFlag(2)
