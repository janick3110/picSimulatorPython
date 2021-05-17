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
from commands import BCF, BSF, getBit, doInterrupt
from simulator import Ui_PicSimulator

win = QMainWindow
simulationThread = None

outdateTime = 0.005

ports = []

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


        self.connectPorts("portAPin", 5)
        self.connectPorts("portATris", 8)
        self.connectPorts("portBPin", 8)
        self.connectPorts("portBTris", 8)

        #endregion

        self.create_table()

    def updateCells(self):
        if self.automaticChange:
            return
        for i in range(len(data.data_memory)):
            row = int(i / 8)
            column = i % 8
            data.data_memory[i] = int(self.tableData.item(row, column).text(), 16)

    def connectPorts(self, prefix, max):

        if self.automaticChange:
            return
        
        for i in range(max):
            portName = prefix + str(i)
            port = getattr(self, portName)

            ports.append((portName, port))
            

            
            port.stateChanged.connect(self.getGUIInput)


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
            output = str(float("{:.1f}".format(microseconds)))
            self.runtime.setText(output)
            now = datetime.datetime.now()
            time.sleep(.1)

    def create_table(self):
        data.__innit__()

        self.automaticChange = True
        for i in range(len(data.data_memory)):
            row = int(i / 8)
            column = i % 8
            output = str(hex(data.data_memory[i])).replace("0x", "")
            self.tableData.setItem(row, column, QTableWidgetItem(output.upper()))

        self.automaticChange = False

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

        # print("stack done")

        self.updateIOPins("portAPin", 5, 0x5)
        self.updateIOPins("portBPin", 8, 0x6)
        self.updateIOPins("portATris", 8, 0x85)
        self.updateIOPins("portBTris", 8, 0x86)

        # print("ports done")

        if data.data_memory[0x03] & 0b00100000 == 0:
            self.enablePins(True, False)
        elif data.data_memory[0x03] & 0b00100000 == 32:
            self.enablePins(False, True)

        # print("enabeling done")

        self.automaticChange = True
        for i in range(len(data.data_memory)):
            row = int(i / 8)
            column = i % 8
            output = str(hex(data.data_memory[i])).replace("0x", "")
            self.tableData.setItem(row, column, QTableWidgetItem(output.upper()))
        self.automaticChange = False

        self.repaint()
        self.update()
        # print("table done")

    def updateIOPins(self, prefix, max, reg):

        # print(prefix)
        self.automaticChange = True
        for i in range(max):
            portName = prefix + str(i)
            port = None
            for n in range(len(ports)):
                if ports[n][0] == portName:
                    port = ports[n][1]
                    continue
            time.sleep(outdateTime)
            self.UpdateIOPin(port, reg, i)
        self.automaticChange = False

    def UpdateIOPin(self, checkbox, address, pos):
        output = data.data_memory[address] & pow(2, pos)

        if output == 0:
            checkbox.setChecked(False)
        elif output == pow(2, pos):
            checkbox.setChecked(True)


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
        comp1 =  1 if checkbox.isChecked() else 0
        comp2 = getBit(address, pos)

        positions = [0, 4, 5, 6, 7]

        intedge = True if getBit(0x81, 6) == 1 else False

        if address == 0x06 and pos in positions:
            if (comp2 > comp1 and not intedge) or (comp2 < comp1 and intedge):
                if pos == 0:
                    BSF(0x0B, 1)
                    doInterrupt()
            elif comp1 is not comp2 and pos in [4, 5, 6, 7]:
                BSF(0x0B, 0)
                doInterrupt()

        if checkbox.isChecked():
            BSF(address, pos)

        else:
            BCF(address, pos)

    def readPin(self, prefix, max, register):
        for i in range(max):
            portName = prefix + str(i)
            port = None
            for n in range(len(ports)):
                if ports[n][0] == portName:
                    port = ports[n][1]
                    continue
            if port is None:
                print(portName)

            self.readPortBit(port, register, i)


    def getGUIInput(self):
            self.readPin("portAPin", 5, 0x05)
            self.readPin("portATris", 8, 0x85)

            self.readPin("portBPin", 8, 0x06)
            self.readPin("portBTris", 8, 0x86)


    def updateSpecialRegister(self):

        output = str(hex(data.data_memory[0x01])).replace("0x", "")
        self.timer0Val.setText(output.upper())
        output = str(hex(data.w_register)).replace("0x", "")
        self.wRegisterVal.setText(output.upper())
        output = str(hex(data.data_memory[0x02])).replace("0x", "")
        self.pclVal.setText(output.upper())
        output = str(hex(data.data_memory[0x03])).replace("0x", "")
        self.statusVal.setText(output.upper())
        output = str(hex(data.data_memory[0x04])).replace("0x", "")
        self.fsrVal.setText(output.upper())
        output = str(hex(data.data_memory[0x81])).replace("0x", "")
        self.optionVal




        # region Region: set view bits
        status = data.data_memory[0x3]
        self.carryBitVal.setText(str(status & 0x00000001))
        self.digitalCarryBitVal.setText(str((status & 0b00000010) >> 1))
        self.zeroBitVal.setText(str((status & 0b00000100) >> 2))
        self.pdBitVal.setText(str((status & 0b00001000) >> 3))
        self.toBitVal.setText(str((status & 0b00010000) >> 4))
        self.rp0BitVal.setText(str((status & 0b00100000) >> 5))
        self.rp1BitVal.setText(str((status & 0b01000000) >> 6))
        self.irpBitVal.setText(str((status & 0b10000000) >> 7))

        intcon = data.data_memory[0x0b]
        self.ps0BitVal.setText(str(intcon & 0x00000001))
        self.ps1BitVal.setText(str((intcon & 0b00000010) >> 1))
        self.ps2BitVal.setText(str((intcon & 0b00000100) >> 2))
        self.psaBitVal.setText(str((intcon & 0b00001000) >> 3))
        self.tseBitVal.setText(str((intcon & 0b00010000) >> 4))
        self.tcsBitVal.setText(str((intcon & 0b00100000) >> 5))
        self.iegBitVal.setText(str((intcon & 0b01000000) >> 6))
        self.rpuBitVal.setText(str((intcon & 0b10000000) >> 7))

        option = data.data_memory[0x81]
        self.rifBitVal.setText(str(option & 0x00000001))
        self.ifBitVal.setText(str((option & 0b00000010) >> 1))
        self.tifBitVal.setText(str((option & 0b00000100) >> 2))
        self.rieBitVal.setText(str((option & 0b00001000) >> 3))
        self.ieBitVal.setText(str((option & 0b00010000) >> 4))
        self.tieBitVal.setText(str((option & 0b00100000) >> 5))
        self.eieBitVal.setText(str((option & 0b01000000) >> 6))
        self.gieBitVal.setText(str((option & 0b10000000) >> 7))

        #endregion

# class FindReplaceDialog(QDialog):
#
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#         # loadUi("ui/find_replace.ui", self)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())
