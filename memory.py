adressspace = [int] * 1024

z_flag = False
c_flag = False
rp0 = False
w_register = 0


def innit_adress():
    for address in range(len(adressspace)):
        print(adressspace[address])


if __name__ == '__main__':
    innit_adress()
