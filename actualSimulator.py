import commands
import data
import simulationParser
import time
from datetime import datetime
import decoder
import PyQt5.QtWidgets as QtWidgets

import simulator
from simulator import Ui_PicSimulator

diff = 0
quartz_frequency = 4000000  # 4MHz 1µs 1MHz ^ 4µs
index = 0
timescale = 100000
breakpoints = []
skipnext = False
isRunning = False

stop = False

def simulate(highlight, updateAll):
    # data.__innit__()
    global index
    global diff
    global stop
    global isRunning

    while index < len(simulationParser.queue):

        if stop:
            stop = False
            break

        if index in breakpoints:
            break

        # table.selectRow(index)

        # app.win.showCode.selectRow(simulationParser.queue[index][0])

        execution(int(simulationParser.queue[index][2], 16), highlight, updateAll)

        if index >= len(simulationParser.queue):
            break
    isRunning = False
    # Speicher vorbereiten
    # Befehle abgearbeitet werden


def execution(befehlscode, highlight, updateAll):
    global index
    global skipnext

    index += 1

    # print(hex(befehlscode))
    if not skipnext:
        decoder.decode(befehlscode)
        print("Info: Executed")
    else:
        skipnext = False

    commands.doTimer()

    time.sleep((4 / quartz_frequency) * timescale)

    data.data_memory[0x02] = index & 0b11111111

    highlight(simulationParser.queue[index][0])

    updateAll()



if __name__ == '__main__':
    simulate()
