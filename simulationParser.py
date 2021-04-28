import tkinter as tk
from tkinter import filedialog

queue = []
arguments = []

lst = []

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


def parse_file_for_gui(file_name):
    """Parses the file to make it readable"""
    object = []
    program_memory = ""
    command_code = ""
    line_number = ""
    label = ""
    commands = ""
    comment = ""
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            program_memory = create_element(0,4,line)
            command_code = create_element(5,9,line)
            line_number = create_element(20,25,line)
            label = get_labels(line)
            commands = get_command(line)
            comment = read_comments(line)
            lst.append((program_memory,command_code,line_number,label,commands,comment))

def create_element(minNumber, maxNumber, line):
    element = ""
    for i in range(minNumber, maxNumber):
        element += line[i]
    return element

def get_labels(line):
    space_counter = 0
    element = ""
    for i in range(25,len(line)):
        if line[i] == ";":
            return ""
        elif line[i] == " " and len(element) > 0 and space_counter <= 1:
            space_counter += 1
            element += " "
        elif line[i] == " " and len(element) > 0 and space_counter <= 1:
            return check_useless_space(element)
        elif line[i] != " ":
            element += line[i]
    return check_useless_space(element)

def get_command(line):
    space_counter = 0
    element = ""

    for i in range(36,len(line)):
        if line[i] == ";":
            return check_useless_space(element)
        elif line[i] == " " and space_counter == 0:
            space_counter = 1
            element += " "
        elif line[i] == " " and space_counter == 1:
            return check_useless_space(element)
        else:
            element += line[i]
    return check_useless_space(element)

def read_comments(line):
    element = ""
    comment_start = 0
    for i in range(len(line)):
        if line[i] == ";":
            comment_start = i
    if comment_start > 0:
        for i in range(comment_start, len(line)):
            element += line[i]
    return element

def check_useless_space(string):

    for i in range(len(string)):
        if string[i] != " ":
            return string
    return ""

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
    #scan_arguments(file_path)
    parse_file_for_gui(file_path)
    print(lst)
#    print(queue)


def execute():
    for argument in arguments:
        execution(argument)


def main():
    get_file()


if __name__ == '__main__':
    main()
