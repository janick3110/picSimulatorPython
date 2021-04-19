


adressspace = [int] * 1024
z_flag = False
c_flag = False
rp0 = False


def innit_adress():
    for adress in range(len(adressspace)):
        print(adressspace[adress])

if __name__ == '__main__':
    innit_adress()