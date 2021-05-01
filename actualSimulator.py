import data
import simulationParser
import time
from datetime import datetime
import decoder
import app
import PyQt5.QtWidgets as QtWidgets
from simulator import Ui_PicSimulator

diff = 0
quarz_frequency = 4000000 # 4MHz 1µs 1MHz ^ 4µs
timescale = 1000

skipnext = False

def simulate():
    data.__innit__()
    steps = 0
    datetime1 = datetime.now()

    for i in range(len(simulationParser.lst)):

        if int(simulationParser.lst[i][2]) == simulationParser.queue[steps][0]:

            execution(int(simulationParser.queue[steps][2], 16))
            time.sleep(4 / quarz_frequency * timescale)
            steps += 1

            if steps >= len(simulationParser.queue):
                break
        datetime2 = datetime.now()

        diff = datetime2 - datetime1

        #app.Window.updateClock(diff)



    diff = (datetime2 - datetime1) * 1000
    print(diff)

    # Speicher vorbereiten
    # Befehle abgearbeitet werden

def execution(befehlscode):
    print(hex(befehlscode))
    decoder.decode(befehlscode)

if __name__ == '__main__':
    simulate()
