import sys
import threading

from PyQt5 import QtCore
import stack
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

    automaticChange = False

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setupUi(self)

        self.connectSignalsSlots()

    # IMPORTANT
    def connectSignalsSlots(self):

        self.actionBeenden.triggered.connect(self.close)
        self.actionDatei_laden.triggered.connect(self.fLoadFile)
        self.button_start.pressed.connect(self.fButtonStart)
        self.button_step.pressed.connect(self.step_forward)
        self.quarzFreq.valueChanged.connect(self.fUpdateFrequency)

        self.tableData.cellChanged.connect(self.updateCells)

        self.portAPin1.


        self.create_table()


    def create_table(self):
        data.__innit__()

        self.automaticChange = True
        for i in range(len(data.data_memory)):
            row = int(i / 8)
            column = i % 8
            output = str(hex(data.data_memory[i])).replace("0x", "")
            self.tableData.setItem(row, column, QTableWidgetItem(output.upper()))

        self.automaticChange = False

if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())
