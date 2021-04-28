import data
import simulationParser
from datetime import datetime
import app


diff = 0
quarz_frequency = 4000

def simulate():
    data.__innit__()
    print(len(simulationParser.queue))
    steps = 0
    datetime1 = datetime.now()
    for i in range(len(simulationParser.lst)):
        print(str(int(simulationParser.lst[i][2])) + " + " + str(simulationParser.queue[steps][0]))
        if int(simulationParser.lst[i][2]) == simulationParser.queue[steps][0]:
            print(simulationParser.queue[steps][0])
            steps += 1
            if steps >= len(simulationParser.queue):
                break
        datetime2 = datetime.now()

        diff = datetime2 - datetime1
        print(diff)
        #app.Window.updateClock(diff)

    diff = (datetime2 - datetime1)*1000
    print(diff)
    print(steps)
    # Speicher vorbereiten
    # Befehle abgearbeitet werden




if __name__ == '__main__':
    simulate()
