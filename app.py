import sys

from PyQt5 import QtCore

import simulationParser

from PyQt5.QtWidgets import (

    QApplication, QDialog, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView

)

from simulator import Ui_PicSimulator


class Window(QMainWindow, Ui_PicSimulator):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setupUi(self)

        self.connectSignalsSlots()


    def connectSignalsSlots(self):

        self.actionBeenden.triggered.connect(self.close)
        self.actionDatei_laden.triggered.connect(self.fLoadFile)
        self.button_start.pressed.connect(self.fButtonStart)


    def fLoadFile(self):
        simulationParser.get_file()


        header = self.showCode.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)

        for i in range(len(simulationParser.queue)):

            item = QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsUserCheckable |
                          QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)

            self.showCode.insertRow(i)
            self.showCode.setItem(i, 0, item)
            self.showCode.setItem(i, 1, QTableWidgetItem(str(simulationParser.queue[i][0])))
            self.showCode.setItem(i, 2, QTableWidgetItem(str(simulationParser.queue[i][1]) + str(simulationParser.queue[i][2])))
            self.showCode.setItem(i, 3, QTableWidgetItem())




    def fButtonStart(self):
        return


class FindReplaceDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        #loadUi("ui/find_replace.ui", self)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())