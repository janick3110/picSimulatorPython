import data
import simulationParser
from datetime import datetime
import app
import PyQt5.QtWidgets as QtWidgets
from simulator import Ui_PicSimulator

diff = 0
quarz_frequency = 4000

def simulate():
    data.__innit__()
    steps = 0
    datetime1 = datetime.now()
    for i in range(len(simulationParser.lst)):
        if int(simulationParser.lst[i][2]) == simulationParser.queue[steps][0]:
            execution(simulationParser.queue[steps][2])
            steps += 1
            if steps >= len(simulationParser.queue):
                break
        datetime2 = datetime.now()

        diff = datetime2 - datetime1

        #app.Window.updateClock(diff)

    diff = (datetime2 - datetime1)*1000
    print(diff)

    # Speicher vorbereiten
    # Befehle abgearbeitet werden

def execution(befehlscode):
    print(befehlscode)
    return NotImplementedError


if __name__ == '__main__':
    simulate()
