import sys
import traceback

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow


class DesktopCleaner(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Main.ui", self)
        self.initUI()

    def initUI(self):
        self.setFixedSize(900, 700)
        self.setWindowTitle('DesktopCleaner')


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("error caught!:")
    print("error message:\n", tb)
    QMainWindow.QApplication.quit()


if __name__ == '__main__':
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    ex = DesktopCleaner()
    ex.show()
    sys.exit(app.exec())
