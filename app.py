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

        #region Connect Ports
        self.portAPin0.stateChanged.connect(self.getGUIInput)
        self.portAPin1.stateChanged.connect(self.getGUIInput)
        self.portAPin2.stateChanged.connect(self.getGUIInput)
        self.portAPin3.stateChanged.connect(self.getGUIInput)
        self.portAPin4.stateChanged.connect(self.getGUIInput)

        self.portATris0.stateChanged.connect(self.getGUIInput)
        self.portATris1.stateChanged.connect(self.getGUIInput)
        self.portATris2.stateChanged.connect(self.getGUIInput)
        self.portATris3.stateChanged.connect(self.getGUIInput)
        self.portATris4.stateChanged.connect(self.getGUIInput)
        self.portATris5.stateChanged.connect(self.getGUIInput)
        self.portATris6.stateChanged.connect(self.getGUIInput)
        self.portATris7.stateChanged.connect(self.getGUIInput)

        self.portBPin0.stateChanged.connect(self.getGUIInput)
        self.portBPin1.stateChanged.connect(self.getGUIInput)
        self.portBPin2.stateChanged.connect(self.getGUIInput)
        self.portBPin3.stateChanged.connect(self.getGUIInput)
        self.portBPin4.stateChanged.connect(self.getGUIInput)
        self.portBPin5.stateChanged.connect(self.getGUIInput)
        self.portBPin6.stateChanged.connect(self.getGUIInput)
        self.portBPin7.stateChanged.connect(self.getGUIInput)

        self.portBTris0.stateChanged.connect(self.getGUIInput)
        self.portBTris1.stateChanged.connect(self.getGUIInput)
        self.portBTris2.stateChanged.connect(self.getGUIInput)
        self.portBTris3.stateChanged.connect(self.getGUIInput)
        self.portBTris4.stateChanged.connect(self.getGUIInput)
        self.portBTris5.stateChanged.connect(self.getGUIInput)
        self.portBTris6.stateChanged.connect(self.getGUIInput)
        self.portBTris7.stateChanged.connect(self.getGUIInput)
        #endregion

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

        simulationThread = threading.Thread(target=actualSimulator.simulate,
                                            args=[self.highlight, self.updateGUI, self.updateSpecialRegister,
                                                  self.getGUIInput])
        if len(simulationParser.queue) > 0:
            simulationThread.start()
            timeThread.start()

    def highlight(self, index):
        self.showCode.selectRow(index)

    def step_forward(self):
        actualSimulator.execution(int(simulationParser.queue[actualSimulator.index][2], 16), self.highlight,
                                  self.updateSpecialRegister, self.updateGUI, self.getGUIInput)

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

        # region Updating GUI
        self.stack0Val.setText(str(stack.stack[0]))
        self.stack1Val.setText(str(stack.stack[1]))
        self.stack2Val.setText(str(stack.stack[2]))
        self.stack3Val.setText(str(stack.stack[3]))
        self.stack4Val.setText(str(stack.stack[4]))
        self.stack5Val.setText(str(stack.stack[5]))
        self.stack6Val.setText(str(stack.stack[6]))
        self.stack7Val.setText(str(stack.stack[7]))

        self.UpdateIOPin(self.portAPin0, 5, 0)
        self.UpdateIOPin(self.portAPin1, 5, 1)
        self.UpdateIOPin(self.portAPin2, 5, 2)
        self.UpdateIOPin(self.portAPin3, 5, 3)
        self.UpdateIOPin(self.portAPin4, 5, 4)

        self.UpdateIOPin(self.portBPin0, 6, 0)
        self.UpdateIOPin(self.portBPin1, 6, 1)
        self.UpdateIOPin(self.portBPin2, 6, 2)
        self.UpdateIOPin(self.portBPin3, 6, 3)
        self.UpdateIOPin(self.portBPin4, 6, 4)
        self.UpdateIOPin(self.portBPin5, 6, 5)
        self.UpdateIOPin(self.portBPin6, 6, 6)
        self.UpdateIOPin(self.portBPin7, 6, 7)

        self.UpdateIOPin(self.portBTris0, 0x86, 0)
        self.UpdateIOPin(self.portBTris1, 0x86, 1)
        self.UpdateIOPin(self.portBTris2, 0x86, 2)
        self.UpdateIOPin(self.portBTris3, 0x86, 3)
        self.UpdateIOPin(self.portBTris4, 0x86, 4)
        self.UpdateIOPin(self.portBTris5, 0x86, 5)
        self.UpdateIOPin(self.portBTris6, 0x86, 6)
        self.UpdateIOPin(self.portBTris7, 0x86, 7)

        self.UpdateIOPin(self.portATris0, 0x85, 0)
        self.UpdateIOPin(self.portATris1, 0x85, 1)
        self.UpdateIOPin(self.portATris2, 0x85, 2)
        self.UpdateIOPin(self.portATris3, 0x85, 3)
        self.UpdateIOPin(self.portATris4, 0x85, 4)
        self.UpdateIOPin(self.portATris5, 0x85, 5)
        self.UpdateIOPin(self.portATris6, 0x85, 6)
        self.UpdateIOPin(self.portATris7, 0x85, 7)
        # endregion

        if data.data_memory[0x03] & 0b00100000 == 0:
            self.enablePins(True,False)
        elif data.data_memory[0x03] & 0b00100000 == 32:
            self.enablePins(False,True)

        for i in range(len(data.data_memory)):
            row = int(i / 8)
            column = i % 8
            output = str(hex(data.data_memory[i])).replace("0x", "")
            self.data.setItem(row, column, QTableWidgetItem(output.upper()))


    def enablePins(self, ports, tris):
        self.portAPin0.setEnabled(ports)
        self.portAPin1.setEnabled(ports)
        self.portAPin2.setEnabled(ports)
        self.portAPin3.setEnabled(ports)
        self.portAPin4.setEnabled(ports)

        self.portBPin1.setEnabled(ports)
        self.portBPin2.setEnabled(ports)
        self.portBPin3.setEnabled(ports)
        self.portBPin4.setEnabled(ports)
        self.portBPin5.setEnabled(ports)
        self.portBPin6.setEnabled(ports)
        self.portBPin7.setEnabled(ports)
        self.portBPin0.setEnabled(ports)

        self.portATris1.setEnabled(tris)
        self.portATris2.setEnabled(tris)
        self.portATris3.setEnabled(tris)
        self.portATris4.setEnabled(tris)
        self.portATris5.setEnabled(tris)
        self.portATris6.setEnabled(tris)
        self.portATris7.setEnabled(tris)
        self.portATris0.setEnabled(tris)

        self.portBTris1.setEnabled(tris)
        self.portBTris2.setEnabled(tris)
        self.portBTris3.setEnabled(tris)
        self.portBTris4.setEnabled(tris)
        self.portBTris5.setEnabled(tris)
        self.portBTris6.setEnabled(tris)
        self.portBTris7.setEnabled(tris)
        self.portBTris0.setEnabled(tris)

    def readPortBit(self, checkbox, address, pos):
        if checkbox.isChecked():
            data.data_memory[address] += pow(2,pos)

    def UpdateIOPin(self, checkbox, address, pos):
        output = data.data_memory[address] & pow(2,pos)
        if output == 0:
            checkbox.setChecked(False)
        elif output == pow(2,pos):
            checkbox.setChecked(True)

    def getGUIInput(self):
            #region read Port Values
            data.data_memory[0x05] = 0
            data.data_memory[0x06] = 0
            data.data_memory[0x85] = 0
            data.data_memory[0x86] = 0


            self.readPortBit(self.portAPin0, 0x5, 0)
            self.readPortBit(self.portAPin1, 0x5, 1)
            self.readPortBit(self.portAPin2, 0x5, 2)
            self.readPortBit(self.portAPin3, 0x5, 3)
            self.readPortBit(self.portAPin4, 0x5, 4)

            self.readPortBit(self.portBPin0, 0x6, 0)
            self.readPortBit(self.portBPin1, 0x6, 1)
            self.readPortBit(self.portBPin2, 0x6, 2)
            self.readPortBit(self.portBPin3, 0x6, 3)
            self.readPortBit(self.portBPin4, 0x6, 4)
            self.readPortBit(self.portBPin5, 0x6, 5)
            self.readPortBit(self.portBPin6, 0x6, 6)
            self.readPortBit(self.portBPin7, 0x6, 7)

            self.readPortBit(self.portATris0, 0x85, 0)
            self.readPortBit(self.portATris1, 0x85, 1)
            self.readPortBit(self.portATris2, 0x85, 2)
            self.readPortBit(self.portATris3, 0x85, 3)
            self.readPortBit(self.portATris4, 0x85, 4)
            self.readPortBit(self.portATris5, 0x85, 5)
            self.readPortBit(self.portATris6, 0x85, 6)
            self.readPortBit(self.portATris7, 0x85, 7)

            self.readPortBit(self.portBTris0, 0x86, 0)
            self.readPortBit(self.portBTris1, 0x86, 1)
            self.readPortBit(self.portBTris2, 0x86, 2)
            self.readPortBit(self.portBTris3, 0x86, 3)
            self.readPortBit(self.portBTris4, 0x86, 4)
            self.readPortBit(self.portBTris5, 0x86, 5)
            self.readPortBit(self.portBTris6, 0x86, 6)
            self.readPortBit(self.portBTris7, 0x86, 7)

            # endregion

            for i in range(len(data.data_memory)):
                row = int(i / 8)
                column = i % 8
                data.data_memory[i] = int(self.data.item(row, column).text(), 16)

    def updateDataTable(self, adress):
        row = int(adress / 8)
        column = adress % 8
        output = str(hex(data.data_memory[adress])).replace("0x", "")
        print("Update erfolgt " + output + " an Stelle " + str(adress))
        self.data.setItem(row, column, QTableWidgetItem(output.upper()))

    def updateSpecialRegister(self):
        output = str(hex(data.w_register)).replace("0x", "")
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
