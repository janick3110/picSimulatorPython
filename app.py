import sys


from PyQt5.QtWidgets import (

    QApplication, QDialog, QMainWindow, QMessageBox

)

from simulator import Ui_PicSimulator


class Window(QMainWindow, Ui_PicSimulator):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setupUi(self)

        self.connectSignalsSlots()


    def connectSignalsSlots(self):

        self.actionBeenden.triggered.connect(self.close)

        self.actionDatei_laden.triggered.connect(self.loadFile)


    def loadFile(self):
        return
        # TODO


    def about(self):

        QMessageBox.about(

            self,

            "About Sample Editor",

            "<p>A sample text editor app built with:</p>"

            "<p>- PyQt</p>"

            "<p>- Qt Designer</p>"

            "<p>- Python</p>",

        )


class FindReplaceDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        #loadUi("ui/find_replace.ui", self)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())