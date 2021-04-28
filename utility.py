def integer_to_binary(register):
    format = "{0:014b}".format(register)

    return format

def binary_to_integer(binary):
    value = 0
    print(binary)
    for n in range(13):
        if binary[13-n] == "1":
            value = value + pow(2, n)
    print(value)
    return value


if __name__ == '__main__':
    integer_to_binary()
