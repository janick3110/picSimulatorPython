#!/usr/bin/python

import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QPlainTextEdit, QWidget
from PyQt5.QtGui import QIcon
import simulationParser as parsing




class Example(QMainWindow):
    trigger = 0

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        loadingAct = QAction(QIcon('load.png'), '&Load', self)
        loadingAct.setShortcut('Ctrl+L')
        loadingAct.setStatusTip('Load file')
        loadingAct.triggered.connect(self.triggerExecution)

        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        self.statusBar()



        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        program = menubar.addMenu('&Program')
        program.addAction(exitAct)
        file.addAction(loadingAct)

        self.resize(300, 100)
        self.setWindowTitle('PicSim')
        self.show()


    def triggerExecution(self):
        parsing.get_file()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
