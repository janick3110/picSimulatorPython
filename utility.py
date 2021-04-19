def integer_to_bool():
    format = "{0:b}".format(173)
    for bit in format:
        if bit == "0":
            print("bit")
        else:
            print("bat")



if __name__ == '__main__':
    integer_to_bool()
