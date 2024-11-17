import sys
import traceback

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QPushButton, QCheckBox
from PyQt6.QtWidgets import QMainWindow


class DesktopCleaner(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Main.ui", self)
        self.initUI()
        self.directories_button = QPushButton()
        self.types_button = QPushButton()
        self.directories_window = None
        self.types_window = None

    def initUI(self):
        self.setFixedSize(900, 700)
        self.setWindowTitle('DesktopCleaner')
        self.directories_button.clicked.connect(self.open_directories_window)
        self.types_button.clicked.connect(self.open_types_window)

    def open_directories_window(self):
        if self.directories_window is None or not self.directories_window.isVisible():
            self.directories_window = DesktopDirectories()
            self.directories_window.show()
        else:
            self.directories_window.raise_()
            self.directories_window.activateWindow()

    def open_types_window(self):
        if self.types_window is None or not self.types_window.isVisible():
            self.types_window = DesktopTypes()
            self.types_window.show()
        else:
            self.types_window.raise_()
            self.types_window.activateWindow()


class DesktopDirectories(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Directories.ui", self)
        self.initUI()

    def initUI(self):
        self.setFixedSize(520, 820)
        self.setWindowTitle('dcDirectories')
        self.simple_checkbox.clicked.connect(self.simple_sort)

    def simple_sort(self):
        if not self.simple_checkbox.isChecked():
            self.photo_label.setEnabled(True)
            self.photo_text.setEnabled(True)
            self.photo_button.setEnabled(True)

            self.video_label.setEnabled(True)
            self.video_text.setEnabled(True)
            self.video_button.setEnabled(True)

            self.text_label.setEnabled(True)
            self.text_text.setEnabled(True)
            self.text_button.setEnabled(True)

            self.audio_label.setEnabled(True)
            self.audio_text.setEnabled(True)
            self.audio_button.setEnabled(True)

            self.archive_label.setEnabled(True)
            self.archive_text.setEnabled(True)
            self.archive_button.setEnabled(True)

            self.executable_label.setEnabled(True)
            self.executable_text.setEnabled(True)
            self.executable_button.setEnabled(True)

            self.else_label.setEnabled(True)
            self.else_text.setEnabled(True)
            self.else_button.setEnabled(True)
        else:
            self.photo_label.setEnabled(False)
            self.photo_text.setEnabled(False)
            self.photo_button.setEnabled(False)

            self.video_label.setEnabled(False)
            self.video_text.setEnabled(False)
            self.video_button.setEnabled(False)

            self.text_label.setEnabled(False)
            self.text_text.setEnabled(False)
            self.text_button.setEnabled(False)

            self.audio_label.setEnabled(False)
            self.audio_text.setEnabled(False)
            self.audio_button.setEnabled(False)

            self.archive_label.setEnabled(False)
            self.archive_text.setEnabled(False)
            self.archive_button.setEnabled(False)

            self.executable_label.setEnabled(False)
            self.executable_text.setEnabled(False)
            self.executable_button.setEnabled(False)

            self.else_label.setEnabled(False)
            self.else_text.setEnabled(False)
            self.else_button.setEnabled(False)


class DesktopTypes(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("FileType.ui", self)
        self.initUI()

    def initUI(self):
        self.setFixedSize(620, 660)
        self.setWindowTitle('dcFileTypes')


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
