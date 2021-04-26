adressspace = [int] * 1024


def innit_adress():

    for address in range(len(adressspace)):
        print(adressspace[address])


if __name__ == '__main__':
    innit_adress()
