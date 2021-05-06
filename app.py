import sys
import threading

from PyQt5 import QtCore

import simulationParser
import actualSimulator

from PyQt5.QtWidgets import (

    QApplication, QDialog, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView

)

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

            if not(str(simulationParser.lst[i][0]).strip() == ""):
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

        actualSimulator.breakpoints = []

        # get all breakpoints
        for i in range(self.showCode.rowCount()):
            breakpoint_in_table = self.showCode.item(i, 0)
            if breakpoint_in_table is not None and breakpoint_in_table.checkState() == 2:
                actualSimulator.breakpoints.append((int(self.showCode.item(i, 1).text(), 16)))

        simulationThread = threading.Thread(target=actualSimulator.simulate, args=[self.highlight, ])
        if len(simulationParser.queue) > 0:
            simulationThread.start()


    def highlight(self, index):
        self.showCode.selectRow(index)


    def step_forward(self):
        actualSimulator.index += 1


    def updateClock(self, time):
        self.runtime.setText(time)


class FindReplaceDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        # loadUi("ui/find_replace.ui", self)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())
