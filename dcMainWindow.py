import sys
import traceback

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QPushButton, QFileDialog
from PyQt6.QtWidgets import QMainWindow
from dcCode import Cleaner as dc


class DesktopCleaner(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Main.ui", self)
        self.initUI()
        self.directories_button = QPushButton()
        self.types_button = QPushButton()
        self.directories_window = None
        self.types_window = None
        self.directories_window = DesktopDirectories()
        self.types_window = DesktopTypes()

    def initUI(self):
        self.setFixedSize(900, 700)
        self.setWindowTitle('DesktopCleaner')
        self.directories_button.clicked.connect(self.open_directories_window)
        self.types_button.clicked.connect(self.open_types_window)

    def open_directories_window(self):
        if self.directories_window is None or not self.directories_window.isVisible():
            self.directories_window.show()
        else:
            self.directories_window.raise_()
            self.directories_window.activateWindow()

    def open_types_window(self):
        if self.types_window is None or not self.types_window.isVisible():
            self.types_window.show()
        else:
            self.types_window.raise_()
            self.types_window.activateWindow()

    def closeEvent(self, event):
        self.directories_window.close()
        self.types_window.close()


class DesktopDirectories(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Directories.ui", self)
        self.dc = dc()
        self.confirm_label.hide()
        self.initUI()

    def initUI(self):
        self.setFixedSize(520, 800)
        self.setWindowTitle('dcDirectories')

        self.simple_checkbox.clicked.connect(self.simple_sort_checkbox)

        self.reset_button.clicked.connect(self.reset_file_directories)

        self.where_button.clicked.connect(lambda: self.where_text.setPlainText(self.get_directory()))
        self.from_button.clicked.connect(lambda: self.from_text.setPlainText(self.get_directory()))
        self.photo_button.clicked.connect(lambda: self.photo_text.setPlainText(self.get_directory()))
        self.video_button.clicked.connect(lambda: self.video_text.setPlainText(self.get_directory()))
        self.text_button.clicked.connect(lambda: self.text_text.setPlainText(self.get_directory()))
        self.audio_button.clicked.connect(lambda: self.audio_text.setPlainText(self.get_directory()))
        self.archive_button.clicked.connect(lambda: self.archive_text.setPlainText(self.get_directory()))
        self.executable_button.clicked.connect(lambda: self.executable_text.setPlainText(self.get_directory()))
        self.code_button.clicked.connect(lambda: self.code_text.setPlainText(self.get_directory()))
        self.else_button.clicked.connect(lambda: self.else_text.setPlainText(self.get_directory()))

    def simple_sort_checkbox(self):
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

            self.code_label.setEnabled(True)
            self.code_text.setEnabled(True)
            self.code_button.setEnabled(True)

            self.else_label.setEnabled(True)
            self.else_text.setEnabled(True)
            self.else_button.setEnabled(True)

            self.where_button.setEnabled(False)
            self.where_label.setEnabled(False)
            self.where_text.setEnabled(False)
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

            self.code_label.setEnabled(False)
            self.code_text.setEnabled(False)
            self.code_button.setEnabled(False)

            self.else_label.setEnabled(False)
            self.else_text.setEnabled(False)
            self.else_button.setEnabled(False)

            self.where_button.setEnabled(True)
            self.where_label.setEnabled(True)
            self.where_text.setEnabled(True)

    def get_directory(self):
        return QFileDialog.getExistingDirectory(self)

    def reset_file_directories(self):
        file_directories = self.dc.return_file_directories()
        if self.confirm_checkbox.isChecked():
            self.confirm_label.hide
            # self.dc.reset_file_directories()
            self.from_text.setPlainText("")
            self.where_text.setPlainText("")

            self.photo_text.setPlainText(list(file_directories.keys())[0])
            self.video_text.setPlainText(list(file_directories.keys())[1])
            self.text_text.setPlainText(list(file_directories.keys())[2])
            self.audio_text.setPlainText(list(file_directories.keys())[3])
            self.archive_text.setPlainText(list(file_directories.keys())[4])
            self.executable_text.setPlainText(list(file_directories.keys())[5])
            self.code_text.setPlainText(list(file_directories.keys())[6])
            self.else_text.setPlainText(list(file_directories.keys())[7])
        else:
            self.confirm_label.show()

    def save_all_directories(self):
        new_directories = {
            "photo":"da"
        }
        self.dc.update_file_directories(new_directories)


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
