import tkinter as tk
from tkinter import filedialog

queue = []
arguments = []
fileText = ''


def prepare_arguments():
    arguments.append("movlw")
    arguments.append("andlw")
    arguments.append("iorlw")
    arguments.append("sublw")
    arguments.append("xorlw")
    arguments.append("addlw")


def scan_arguments(file_name):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    line_number = 0
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            if line[5] != ' ':
                argument = line[5] + line[6]
                address = line[7] + line[8]
                queue.append((line_number, argument, address))
                line_number += 1


def execution(argument):
    if argument == "movlw":
        print("MOVLW")
    elif argument == "andlw":
        print("ANDLW")
    elif argument == "iorlw":
        print("IORLW")
    elif argument == "sublw":
        print("SUBLW")
    elif argument == "addlw":
        print("ADDLW")
    elif argument == "xorlw":
        print("XORLW")


def get_file():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(filetypes=[("Listing-Files", "*.LST")])
    prepare_arguments()
    scan_arguments(file_path)
    print(queue)


def execute():
    for argument in arguments:
        execution(argument)


def main():
    get_file()

if __name__ == '__main__':
    main()
