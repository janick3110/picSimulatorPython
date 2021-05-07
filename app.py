import sys
import threading

from PyQt5 import QtCore

import simulationParser
import actualSimulator
import datetime
import time
from PyQt5.QtWidgets import (

    QApplication, QDialog, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView

)

import data
import simulator
from simulator import Ui_PicSimulator

win = QMainWindow
simulationThread = None


class Window(QMainWindow, Ui_PicSimulator):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setupUi(self)

        self.connectSignalsSlots()

    # IMPORTANT
    def connectSignalsSlots(self):

        self.actionBeenden.triggered.connect(self.close)
        self.actionDatei_laden.triggered.connect(self.fLoadFile)
        self.button_start.pressed.connect(self.fButtonStart)
        self.stepButton.pressed.connect(self.step_forward)
        self.quarzFreq.valueChanged.connect(self.fUpdateFrequency)

        self.create_table()

    def fUpdateFrequency(self):
        actualSimulator.quartz_frequency = int(self.quarzFreq.text())

    def fLoadFile(self):
        simulationParser.queue = []
        # print(simulationParser.lst)
        simulationParser.lst = []
        # print(simulationParser.lst)
        simulationParser.get_file()

        for row in range(self.showCode.rowCount()):
            self.showCode.removeRow(0)

        header = self.showCode.horizontalHeader()
        for i in range(0, 7):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

        for i in range(len(simulationParser.lst)):
            item = QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsUserCheckable |
                          QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)

            self.showCode.insertRow(i)

            if not (str(simulationParser.lst[i][0]).strip() == ""):
                self.showCode.setItem(i, 0, item)

            self.showCode.setItem(i, 1, QTableWidgetItem(str(simulationParser.lst[i][0])))
            self.showCode.setItem(i, 2, QTableWidgetItem(str(simulationParser.lst[i][1])))
            self.showCode.setItem(i, 3, QTableWidgetItem(str(simulationParser.lst[i][2])))
            self.showCode.setItem(i, 4, QTableWidgetItem(str(simulationParser.lst[i][3])))
            self.showCode.setItem(i, 5, QTableWidgetItem(str(simulationParser.lst[i][4])))
            self.showCode.setItem(i, 6, QTableWidgetItem(str(simulationParser.lst[i][5])))

            # marks table row

    def fButtonStart(self):

        # for thread in threading.enumerate():
        #     print(thread.name)
        actualSimulator.isRunning = True
        timeThread = threading.Thread(target=self.updateClock)

        actualSimulator.breakpoints = []

        # get all breakpoints
        for i in range(self.showCode.rowCount()):
            breakpoint_in_table = self.showCode.item(i, 0)
            if breakpoint_in_table is not None and breakpoint_in_table.checkState() == 2:
                actualSimulator.breakpoints.append((int(self.showCode.item(i, 1).text(), 16)))

        simulationThread = threading.Thread(target=actualSimulator.simulate, args=[self.highlight, self.updateGUI,self.updateSpecialRegister, self.getGUIInput])
        if len(simulationParser.queue) > 0:
            simulationThread.start()
            timeThread.start()

    def highlight(self, index):
        self.showCode.selectRow(index)

    def step_forward(self):
        actualSimulator.execution(int(simulationParser.queue[actualSimulator.index][2], 16),self.highlight, self.updateSpecialRegister,self.updateGUI, self.getGUIInput)

    def updateClock(self):

        start = 0
        now = datetime.datetime.now()
        microseconds = 0
        start = datetime.datetime.now()
        while actualSimulator.isRunning:
            actualSimulator.diff = abs(now - start)

            microseconds = actualSimulator.diff.total_seconds() * 4 * actualSimulator.timescale / actualSimulator.quartz_frequency
            output = str(float("{:.2f}".format(microseconds)))
            self.runtime.setText(output)
            now = datetime.datetime.now()
            time.sleep(.1)

    def create_table(self):
        data.__innit__()

        for i in range(len(data.data_memory)):
            row = int(i / 8)
            column = i % 8
            output = str(hex(data.data_memory[i])).replace("0x", "")
            self.data.setItem(row, column, QTableWidgetItem(output.upper()))


    def updateGUI(self):
        for i in range(len(data.data_memory)):
            row = int(i / 8)
            column = i % 8
            output = str(hex(data.data_memory[i])).replace("0x", "")
            self.data.setItem(row, column, QTableWidgetItem(output.upper()))

    def getGUIInput(self):
        for i in range(len(data.data_memory)):
            row = int(i / 8)
            column = i % 8
            data.data_memory[i] = int(self.data.item(row,column).text(), 16)


    def updateDataTable(self,adress):
        row = int(adress / 8)
        column = adress % 8
        output = str(hex(data.data_memory[adress])).replace("0x","")
        print("Update erfolgt " + output + " an Stelle " + str(adress))
        self.data.setItem(row,column,QTableWidgetItem(output.upper()))

    def updateSpecialRegister(self):
        output = str(hex(data.w_register)).replace("0x","")
        self.wRegisterVal.setText(output.upper())

        output = str(hex(data.data_memory[0x02])).replace("0x", "")
        self.pclVal.setText(output.upper())


class FindReplaceDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        # loadUi("ui/find_replace.ui", self)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())
