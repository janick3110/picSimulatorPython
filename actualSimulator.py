import data
import simulationParser


def simulate():
    time_delta = 0
    data.__innit__()
    simulationParser.get_file()
    print(len(simulationParser.queue))
    steps = 0

    for i in range(len(simulationParser.lst)):
        print(str(int(simulationParser.lst[i][2])) + " + " + str(simulationParser.queue[steps][0]))
        if int(simulationParser.lst[i][2]) == simulationParser.queue[steps][0]:
            print(simulationParser.queue[steps][0])
            steps += 1
            if steps >= len(simulationParser.queue):
                break

    print(steps)
    # Speicher vorbereiten
    # Befehle abgearbeitet werden


if __name__ == '__main__':
    simulate()
