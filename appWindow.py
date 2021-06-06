import datetime
import threading

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QTableWidgetItem, QApplication

import sys

import actualSimulator
import data
import time
import simulationParser
import stack

from commands import getBit, doInterrupt, BSF, BCF
from simulator import Ui_PicSimulator
from PyQt5 import QtCore, QtGui
from multiprocessing import Lock, Process


class Window(QMainWindow, Ui_PicSimulator):
    ports = []

    lastRow = None

    debugMode = True
    debugLocks = False

    stop = False

    portLock = Lock()
    dataLock = Lock()

    # region Initialize: Connect and create

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setupUi(self)

        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        """Connect signals and slots with specified methods"""

        self.actionBeenden.triggered.connect(self.close)
        self.actionDatei_laden.triggered.connect(self.fLoadFile)
        self.button_start.pressed.connect(self.fButtonStart)
        self.button_stop.pressed.connect(self.fButtonStop)
        self.button_step.pressed.connect(self.step_forward)
        self.button_reset.pressed.connect(self.fButtonReset)

        # self.quarzFreq.valueChanged.connect(self.fUpdateFrequency)
        self.quarzFreq.editingFinished.connect(self.fUpdateFrequency)

        self.tableData.cellChanged.connect(self.updateCells)

        self.connectPorts("portAPin", 5)
        self.connectPorts("portATris", 8)
        self.connectPorts("portBPin", 8)
        self.connectPorts("portBTris", 8)

        self.create_table()

        self.updateAll()

    def connectPorts(self, prefix, maxi):
        """Connect all ports with function"""
        for i in range(maxi):
            portName = prefix + str(i)
            port = getattr(self, portName)

            self.ports.append((portName, port))
            port.stateChanged.connect(lambda ch, p=portName: self.getPortChange(p))
            # port.stateChanged.connect(self.getGUIInput)

    def create_table(self):
        data.__innit__()
        self.mapDataToTable()

    # endregion

    # region Button: Load File

    def fLoadFile(self):
        """Call subfunctions in order to load file"""
        self.fButtonReset()
        self.resetCodeFile()
        simulationParser.get_file()
        self.setCodeTableHeader()
        self.fillCodeTable()

    def resetCodeFile(self):
        """Empty queue, list and remove all rows from table"""
        # empty queue in simulationParser
        simulationParser.queue = []

        # empty list in simulationParser
        simulationParser.lst = []

        # empty code window
        for row in range(self.showCode.rowCount()):
            self.showCode.removeRow(0)

    def setCodeTableHeader(self):
        """Set and resize header of Code table"""
        header = self.showCode.horizontalHeader()
        for i in range(0, 7):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

    def fillCodeTable(self):
        """Insert rows in table for every entry"""
        for i in range(len(simulationParser.lst)):
            self.insertCheckboxRow(i)

    def insertCheckboxRow(self, i):
        """Insert one single row in table"""
        item = QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsUserCheckable |
                      QtCore.Qt.ItemIsEnabled)
        item.setCheckState(QtCore.Qt.Unchecked)

        self.showCode.insertRow(i)

        if not (str(simulationParser.lst[i][0]).strip() == ""):
            self.showCode.setItem(i, 0, item)

        for n in range(1, 7):
            widget = QTableWidgetItem(str(simulationParser.lst[i][n - 1]))
            widget.setFlags(Qt.ItemIsEnabled)
            self.showCode.setItem(i, n, widget)


    # endregion

    # region Checkbox: Port state changed
    def getPortChange(self, portName):

        self.debug("Info: Manual Port Change Triggered")

        port = self.getPort(portName)

        register = 0
        if portName.find("APin") >= 0:
            register = 0x05
        elif portName.find("ATris") >= 0:
            register = 0x85
        elif portName.find("BPin") >= 0:
            register = 0x06
        elif portName.find("BTris") >= 0:
            register = 0x86

        bit = self.extractBit(portName)

        self.readPortBit(port, register, bit)

        self.updateAll()

        return

    def getPort(self, portName):
        """Get the port from its name"""
        port = None
        for n in range(len(self.ports)):
            if self.ports[n][0] == portName:
                port = self.ports[n][1]
                return port

        print("Warning: " + portName + " is None or Undef!")
        return None

    def extractBit(self, portName):
        """Extract exact bit from PortName"""

        # portName = ""

        portName = portName.replace("port", "")
        portName = portName.replace("Pin", "")
        portName = portName.replace("Tris", "")
        portName = portName.replace("A", "")
        portName = portName.replace("B", "")

        if not portName.isnumeric():
            print("Warning: Bit is not Numeric --> " + portName)
            return None
        return int(portName)

    def readPortBit(self, checkbox, address, pos):

        self.lockPorts()
        checkboxVal = checkbox.isChecked()
        self.unlockPorts()

        newVal = 1 if checkboxVal else 0
        oldVal = getBit(address, pos)

        self.testInterruptCondition(address, pos, newVal, oldVal)

        self.lockData()
        if checkboxVal:
            BSF(address, pos)
        else:
            BCF(address, pos)
        self.unlockData()

    def testInterruptCondition(self, address, pos, newVal, oldVal):
        """Tests for a port change that would cause an interrupt"""

        positions = [0, 4, 5, 6, 7]

        # Interrupt Edge Selection Bit 1 Rising 0 Falling
        intedge = True if getBit(0x81, 6) == 1 else False

        if address == 0x06 and pos in positions:
            if (oldVal > newVal and not intedge) or (oldVal < newVal and intedge):
                if pos == 0:
                    BSF(0x0B, 1)

            elif newVal is not oldVal and pos in [4, 5, 6, 7]:
                BSF(0x0B, 0)


    # endregion

    # region Table: Data changed

    def updateCells(self):
        """Update data according to table in view"""
        self.lockData()
        for i in range(len(data.data_memory)):
            row = int(i / 8)
            column = i % 8
            oldVal = data.data_memory[i]
            newVal = int(self.tableData.item(row, column).text(), 16)
            if oldVal != newVal:
                print("Info: Changed " + str(row) + ":" + str(column) + " from " + str(oldVal) + " to " + str(newVal))
                data.data_memory[i] = newVal
        self.unlockData()

        self.updateAll()

    # endregion

    # region Run

    def step_forward(self):
        index = int(simulationParser.queue[actualSimulator.index][2], 16)
        actualSimulator.execution(index, self.highlight, self.updateAll)

    def fButtonStart(self):

        # for thread in threading.enumerate():
        #     print(thread.name)
        actualSimulator.isRunning = True

        timeThread = threading.Thread(target=self.updateClock)
        timeThread.daemon = True

        actualSimulator.breakpoints = []

        # get all breakpoints
        for i in range(self.showCode.rowCount()):
            breakpoint_in_table = self.showCode.item(i, 0)
            if breakpoint_in_table is not None and breakpoint_in_table.checkState() == 2:
                actualSimulator.breakpoints.append((int(self.showCode.item(i, 1).text(), 16)))

        simulationThread = threading.Thread(target=actualSimulator.simulate,
                                            args=[self.highlight, self.updateAll, ])
        simulationThread.daemon = True

        if len(simulationParser.queue) > 0:
            simulationThread.start()
            timeThread.start()

    def fButtonStop(self):
        if actualSimulator.isRunning:
            actualSimulator.stop = True

    def fButtonReset(self):
        self.fButtonStop()
        time.sleep(0.3)
        data.__innit__()
        self.resetCodeFile()
        self.create_table()
        data.w_register = 0
        actualSimulator.index = 0
        self.updateAll()

    # endregion

    # region View: Update

    def updateAll(self):
        self.updateSpecialRegister()
        # print("Info: Updated Special")
        self.mapDataToTable()
        # print("Info: Mapped Data")
        self.updateStack()
        # print("Info: Updated Stack")
        self.updateIOPins()
        # print("updated IO")

    def updateSpecialRegister(self):

        self.lockData()

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
        self.optionVal.setText(output.upper())


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

        option = data.data_memory[0x81] # Intcon
        self.ps0BitVal.setText(str( option & 0x00000001))
        self.ps1BitVal.setText(str((option & 0b00000010) >> 1))
        self.ps2BitVal.setText(str((option & 0b00000100) >> 2))
        self.psaBitVal.setText(str((option & 0b00001000) >> 3))
        self.tseBitVal.setText(str((option & 0b00010000) >> 4))
        self.tcsBitVal.setText(str((option & 0b00100000) >> 5))
        self.iegBitVal.setText(str((option & 0b01000000) >> 6))
        self.rpuBitVal.setText(str((option & 0b10000000) >> 7))

        intcon = data.data_memory[0x0b]
        self.rifBitVal.setText(str( intcon & 0x00000001))
        self.ifBitVal.setText(str(( intcon & 0b00000010) >> 1))
        self.tifBitVal.setText(str((intcon & 0b00000100) >> 2))
        self.rieBitVal.setText(str((intcon & 0b00001000) >> 3))
        self.ieBitVal.setText(str(( intcon & 0b00010000) >> 4))
        self.tieBitVal.setText(str((intcon & 0b00100000) >> 5))
        self.eieBitVal.setText(str((intcon & 0b01000000) >> 6))
        self.gieBitVal.setText(str((intcon & 0b10000000) >> 7))

        self.unlockData()

    def mapDataToTable(self):
        """Safely update table from data"""
        self.tableData.blockSignals(True)
        self.lockData()

        for i in range(len(data.data_memory)):
            row = int(i / 8)
            column = i % 8
            output = str(hex(data.data_memory[i])).replace("0x", "")
            self.tableData.setItem(row, column, QTableWidgetItem(output.upper()))

        self.tableData.hide()
        self.tableData.show()

        self.unlockData()
        self.tableData.blockSignals(False)

    def updateStack(self):



        self.stack0Val.setText(hex(stack.stack[0]).replace("0x", "").upper())
        self.stack1Val.setText(hex(stack.stack[1]).replace("0x", "").upper())
        self.stack2Val.setText(hex(stack.stack[2]).replace("0x", "").upper())
        self.stack3Val.setText(hex(stack.stack[3]).replace("0x", "").upper())
        self.stack4Val.setText(hex(stack.stack[4]).replace("0x", "").upper())
        self.stack5Val.setText(hex(stack.stack[5]).replace("0x", "").upper())
        self.stack6Val.setText(hex(stack.stack[6]).replace("0x", "").upper())
        self.stack7Val.setText(hex(stack.stack[7]).replace("0x", "").upper())

    def updateIOPins(self):
        """Safely update IO Pins"""
        self.debug("Info: Entering Pin Group update")



        self.updateIOPinGroup("portAPin", 5, 0x5)
        self.updateIOPinGroup("portBPin", 8, 0x6)
        self.updateIOPinGroup("portATris", 8, 0x85)
        self.updateIOPinGroup("portBTris", 8, 0x86)

        self.debug("Info: Groups done")

        self.updatePinTrisEnabeling()

    def updateIOPinGroup(self, prefix, max, reg):
        # print(prefix)

        for i in range(max):

            portName = prefix + str(i)
            # print(portName)



            port = self.getPort(portName)
            self.UpdateIOPin(port, reg, i)

    def UpdateIOPin(self, checkbox, address, pos):
        self.lockData()
        output = data.data_memory[address] & pow(2, pos)

        self.unlockData()

        self.lockPorts()
        checkbox.blockSignals(True)

        # checkbox = self.portAPin1

        # checked = checkbox.checkState()

        checked = checkbox.isChecked()
        self.unlockPorts()



        if output == 0 and checked:
            time.sleep(0.01)
            self.lockPorts()

            checkbox.setChecked(False)

            self.unlockPorts()
            time.sleep(0.01)
        elif output == pow(2, pos) and not checked:

            time.sleep(0.01)
            self.lockPorts()

            checkbox.setChecked(True)

            self.unlockPorts()
            time.sleep(0.01)


        checkbox.blockSignals(False)

    def updatePinTrisEnabeling(self):

        self.lockData()
        self.lockPorts()

        if data.data_memory[0x03] & 0b00100000 == 0:
            self.enablePins(True, False)
            time.sleep(0.002)
        elif data.data_memory[0x03] & 0b00100000 == 32:
            self.enablePins(False, True)
            time.sleep(0.002)

        self.unlockPorts()
        self.unlockData()

    def enablePins(self, ports, tris):
        """Enable either Pins or Tris' """

        self.enableIOPinGroup("portAPin", 5, ports)
        self.enableIOPinGroup("portBPin", 8, ports)
        self.enableIOPinGroup("portATris", 8, tris)
        self.enableIOPinGroup("portBTris", 8, tris)

    def enableIOPinGroup(self, prefix, max, enable):
        print("Info: Entered enabeling")
        for i in range(max):
            portName = prefix + str(i)

            port = self.getPort(portName)

            port.blockSignals(True)
            port.setEnabled(enable)
            port.blockSignals(False)

        return

    # endregion

    # region Time related

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

    def fUpdateFrequency(self):
        actualSimulator.quartz_frequency = int(self.quarzFreq.text())

    # endregion

    # region Helper Functions

    def lockData(self):
        self.debugLocksMSG("--> | Data |")
        self.dataLock.acquire()
        self.debugLocksMSG("| --> Data |")

    def unlockData(self):
        self.dataLock.release()
        self.debugLocksMSG("| Data | -->")

    def lockPorts(self):
        self.debugLocksMSG("--> | Ports |")
        self.portLock.acquire()
        self.debugLocksMSG("| --> Ports |")

    def unlockPorts(self):
        self.portLock.release()
        self.debugLocksMSG("| Ports | -->")

    def highlight(self, index):



        if self.lastRow is not None:
            for j in range(self.showCode.columnCount()):
                self.showCode.item(self.lastRow, j).setBackground(QtGui.QColor(0xFF, 0xFF, 0xFF))

        for j in range(self.showCode.columnCount()):
            self.showCode.item(index, j).setBackground(QtGui.QColor(0xA0, 0xA0, 0xFF))

        self.showCode.selectRow(index)

        self.lastRow = index

        self.showCode.hide()
        self.showCode.show()





    def debug(self, info):
        if self.debugMode:
            print(info)

    def debugLocksMSG(self, info):
        if self.debugLocks:
            print(info)
    # endregion


if __name__ == "__main__":
    app = QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())
