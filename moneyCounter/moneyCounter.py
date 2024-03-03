from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
import sys
import pathlib
from mainWindow import MainWindow

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

class MoneyCounterApp(QApplication):

    def __init__(self, argv):
        super().__init__(argv)
        QtGui.QFontDatabase.addApplicationFont("resources/Montserrat_Alternates/MontserratAlternates-Bold.ttf")
        QtGui.QFontDatabase.addApplicationFont("resources/Montserrat_Alternates/MontserratAlternates-Medium.ttf")
        font = QFont("Montserrat Alternates", 50)
        self.setFont(font)


if __name__ == "__main__":
    app = MoneyCounterApp(sys.argv)

    main_window = MainWindow()
    main_window.show()

    pathlib.PosixPath = temp
    sys.exit(app.exec())