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
quarz_frequency = 4000000 # 4MHz 1µs 1MHz ^ 4µs
timescale = 1000
index = 0
timescale = 1000000
breakpoints = []
skipnext = False

def simulate():
    data.__innit__()
    global index
    global diff
    datetime1 = datetime.now()

    while index < len(simulationParser.queue):

        currentIndex = index
        index += 1

        app.win.showCode.selectRow(index)

        execution(int(simulationParser.queue[currentIndex][2], 16))
        time.sleep(4 / quarz_frequency * timescale)
        print(hex(data.w_register))

        if index >= len(simulationParser.queue):
            break
        datetime2 = datetime.now()

        diff = datetime2 - datetime1

        # app.Window.updateClock(diff)



    diff = (datetime2 - datetime1) * 1000
    print(diff)

    # Speicher vorbereiten
    # Befehle abgearbeitet werden

def execution(befehlscode):
    #print(hex(befehlscode))
    decoder.decode(befehlscode)

if __name__ == '__main__':
    simulate()
