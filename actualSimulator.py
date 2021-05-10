import commands
import data
import simulationParser
import time
from datetime import datetime
import decoder
import app
import PyQt5.QtWidgets as QtWidgets

import simulator
from simulator import Ui_PicSimulator

diff = 0
quartz_frequency = 4000000 # 4MHz 1µs 1MHz ^ 4µs
index = 0
timescale = 400000
breakpoints = []
skipnext = False
isRunning = False


def simulate(highlight, guiUpdate, updateSpecialRegister, guiInput):
    #data.__innit__()
    global index
    global diff



    while index < len(simulationParser.queue):
        if index in breakpoints:
            break


        # table.selectRow(index)

        # app.win.showCode.selectRow(simulationParser.queue[index][0])

        execution(int(simulationParser.queue[index][2], 16), highlight, updateSpecialRegister, guiUpdate, guiInput)

        if index >= len(simulationParser.queue):
            break


    # Speicher vorbereiten
    # Befehle abgearbeitet werden


def execution(befehlscode, highlight, updateSpecialRegister, guiUpdate, guiInput):
    global index
    global skipnext
    guiInput()

    index += 1

    #print(hex(befehlscode))
    if not skipnext:
        decoder.decode(befehlscode)
    else:
        skipnext = False

    commands.doTimerStuff()

    time.sleep(4 / quartz_frequency * timescale)

    data.data_memory[0x02] = index & 0b11111111
    #print(hex(data.w_register))

    highlight(simulationParser.queue[index][0])
    updateSpecialRegister()

    # print("BeforeGUI" + str(index))

    guiUpdate()

    # print("AfterGUI" + str(index))

if __name__ == '__main__':
    simulate()
