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
timescale = 1000
index = 0
timescale = 1000000
breakpoints = []
skipnext = False
isRunning = False
tableUpdater = None

def simulate(highlight, tableUpdate):
    #data.__innit__()
    global index
    global diff
    global tableUpdater
    tableUpdater = tableUpdate


    while index < len(simulationParser.queue):
        if index in breakpoints:
            break

        # table.selectRow(index)

        # app.win.showCode.selectRow(simulationParser.queue[index][0])

        execution(int(simulationParser.queue[index][2], 16), highlight)

        if index >= len(simulationParser.queue):
            break


        # app.Window.updateClock(diff)

    print(diff)

    # Speicher vorbereiten
    # Befehle abgearbeitet werden


def execution(befehlscode, highlight):
    global index
    highlight(simulationParser.queue[index][0])
    index += 1

    #print(hex(befehlscode))
    decoder.decode(befehlscode)

    time.sleep(4 / quartz_frequency * timescale)
    print(hex(data.w_register))


if __name__ == '__main__':
    simulate()
