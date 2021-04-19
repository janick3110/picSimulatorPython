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


        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        self.statusBar()

        textBox = QPlainTextEdit(self)
        textBox.move(250, 120)
        self.show()

        menubar = self.menuBar()
        program = menubar.addMenu('&Load')
        file = menubar.addMenu('&File')
        program.addAction(exitAct)
        file.addAction(loadingAct)

        self.resize(700, 700)
        self.setWindowTitle('Simple menu')
        self.show()


def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


def triggerExecution():
    if Example.trigger == 1:
        parsing.main()
    Example.trigger = 1


if __name__ == '__main__':
    main()
