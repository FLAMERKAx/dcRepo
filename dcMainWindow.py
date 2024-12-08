import os
import sys
import traceback

from PyQt6 import uic, QtGui
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QFileDialog
from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton

from dcCode import Cleaner as dc


class DesktopCleaner(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Main.ui", self)
        self.initUI()
        self.setWindowIcon(QtGui.QIcon(r"finicon.ico"))
        self.directories_button = QPushButton()
        self.types_button = QPushButton()
        self.directories_window = None
        self.types_window = None
        self.directories_window = DesktopDirectories()
        self.types_window = DesktopTypes()
        self.help_window = DesktopHelp()
        self.dc = dc()

    def initUI(self):
        self.setFixedSize(900, 700)
        self.setWindowTitle('DesktopCleaner')
        self.directories_button.clicked.connect(self.open_directories_window)
        self.types_button.clicked.connect(self.open_types_window)
        self.help_button.clicked.connect(self.open_help_window)
        self.clean_button.clicked.connect(self.clean)
        self.undo_button.clicked.connect(self.undo)
        self.analyze_button.clicked.connect(self.analyze)
        self.get_folder_button.clicked.connect(self.get_directory)
        self.delete_button.clicked.connect(self.delete)
        self.weight_checkbox.stateChanged.connect(self.weight_show_checkboxes)
        self.without_sort_checkbox.stateChanged.connect(self.without_sort)
        self.date_checkbox.stateChanged.connect(self.date_show_checkboxes)
        self.file_type_checkbox.stateChanged.connect(self.type_sort_show_checkboxes)
        self.year_checkbox.stateChanged.connect(self.date_checkboxes)
        self.month_checkbox.stateChanged.connect(self.date_checkboxes)
        self.day_checkbox.stateChanged.connect(self.date_checkboxes)
        self.save_preferences.clicked.connect(self.save_preference)
        self.execute_preferences.clicked.connect(self.execute_pref)

    def clean(self):
        if self.file_type_checkbox.isChecked() and self.file_type_checkbox.isEnabled():
            exeption_dict = {
                "photo": self.photo_checkbox.isChecked(),
                "video": self.video_checkbox.isChecked(),
                "text": self.text_checkbox.isChecked(),
                "audio": self.audio_checkbox.isChecked(),
                "archive": self.archive_checkbox.isChecked(),
                "executable": self.executable_checkbox.isChecked(),
                "code": self.code_checkbox.isChecked(),
                "else": self.else_checkbox.isChecked()
            }
            exeption_list = []
            counter = 0
            for i in list(exeption_dict.values()):
                if i is False:
                    exeption_list.append(list(exeption_dict.keys())[counter])
                counter += 1
            if self.simple_checkbox.isChecked():
                if not os.path.exists(fr"{list(self.dc.return_simple_directories().values())[1]}\photos"):
                    self.dc.make_simple_sort_directories(list(self.dc.return_simple_directories().values())[1])
                self.dc.move_folder(list(self.dc.return_simple_directories().values())[0], simple=True,
                                    exceptions_list=exeption_list, sort_mode="type")
            else:
                self.dc.move_folder(list(self.dc.return_simple_directories().values())[0], sort_mode="type")
        elif self.without_sort_checkbox.isChecked() and self.without_sort_checkbox.isEnabled():
            self.dc.just_move()
        elif self.weight_checkbox.isChecked() and self.weight_checkbox.isEnabled():
            self.dc.move_folder(list(self.dc.return_simple_directories().values())[0], sort_mode="weight",
                                file_weight=int(self.weight_text.toPlainText()))
        elif self.date_checkbox.isChecked() and self.date_checkbox.isEnabled():
            if self.year_checkbox.isChecked():
                self.dc.date_folder_move(list(self.dc.return_simple_directories().values())[0], "date_year")
            elif self.month_checkbox.isChecked():
                self.dc.date_folder_move(list(self.dc.return_simple_directories().values())[0], "date_month")
            elif self.day_checkbox.isChecked():
                self.dc.date_folder_move(list(self.dc.return_simple_directories().values())[0], "date_day")

    def undo(self):
        self.dc.undo_move()

    def analyze(self):
        if self.subfolder_checkbox.isChecked():
            data = self.dc.analyze_folder(self.directories_window.get_directory(), subfolder_flag=True)
        else:
            data = self.dc.analyze_folder(self.directories_window.get_directory(), subfolder_flag=False)
        self.analyze_out.setPlainText(
            f"""{data[0]}\nВсего Файлов: {data[1]}\nВес Файлов {data[2]}\nПо типам:\nФото: {data[3]}
Видео: {data[4]}\nТекст: {data[5]}\nАудио: {data[6]}\nАрхивы: {data[7]}\nПрограммы: {data[8]}
Код: {data[9]}\nПрочие Файлы: {data[10]}""")

    def delete(self):
        if self.confirm_checkbox.isChecked() and self.delete_folder.toPlainText() != "" \
                and self.with_folder_checkbox.isChecked():
            self.dc.delete_folder(self.delete_folder.toPlainText(), with_folder=True)
        elif self.confirm_checkbox.isChecked() and self.delete_folder.toPlainText() != "" \
                and not self.with_folder_checkbox.isChecked():
            self.dc.delete_folder(self.delete_folder.toPlainText())

    def get_directory(self):
        self.delete_folder.setPlainText(self.directories_window.get_directory())

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

    def open_help_window(self):
        if self.help_window is None or not self.help_window.isVisible():
            self.help_window.show()
        else:
            self.help_window.raise_()
            self.help_window.activateWindow()

    def without_sort(self):
        if self.without_sort_checkbox.isChecked():
            self.weight_checkbox.setEnabled(False)
            self.weight_text.setEnabled(False)
            self.label_22.setEnabled(False)
            self.weight_checkbox.setEnabled(False)
            self.date_checkbox.setEnabled(False)
            self.year_checkbox.setEnabled(False)
            self.month_checkbox.setEnabled(False)
            self.day_checkbox.setEnabled(False)
            self.label_23.setEnabled(False)
            self.date_checkbox.setEnabled(False)
            self.file_type_checkbox.setEnabled(False)
            self.simple_checkbox.setEnabled(False)
            self.label_4.setEnabled(False)
            self.photo_checkbox.setEnabled(False)
            self.video_checkbox.setEnabled(False)
            self.text_checkbox.setEnabled(False)
            self.audio_checkbox.setEnabled(False)
            self.archive_checkbox.setEnabled(False)
            self.executable_checkbox.setEnabled(False)
            self.code_checkbox.setEnabled(False)
            self.else_checkbox.setEnabled(False)
            self.label_19.setEnabled(False)
        else:
            if self.weight_checkbox.isChecked():
                self.weight_checkbox.setEnabled(True)
                self.weight_text.setEnabled(True)
                self.label_22.setEnabled(True)
            else:
                self.weight_checkbox.setEnabled(True)
            if self.date_checkbox.isChecked():
                self.date_checkbox.setEnabled(True)
                self.year_checkbox.setEnabled(True)
                self.month_checkbox.setEnabled(True)
                self.day_checkbox.setEnabled(True)
                self.label_23.setEnabled(True)
            else:
                self.date_checkbox.setEnabled(True)
            if self.file_type_checkbox.isChecked():
                self.file_type_checkbox.setEnabled(True)
                self.simple_checkbox.setEnabled(True)
                self.label_4.setEnabled(True)
                self.photo_checkbox.setEnabled(True)
                self.video_checkbox.setEnabled(True)
                self.text_checkbox.setEnabled(True)
                self.audio_checkbox.setEnabled(True)
                self.archive_checkbox.setEnabled(True)
                self.executable_checkbox.setEnabled(True)
                self.code_checkbox.setEnabled(True)
                self.else_checkbox.setEnabled(True)
                self.label_19.setEnabled(True)
            else:
                self.file_type_checkbox.setEnabled(True)

    def weight_show_checkboxes(self):
        if self.weight_checkbox.isChecked():
            self.date_checkbox.setChecked(False)
            self.date_show_checkboxes()
            self.file_type_checkbox.setChecked(False)
            self.type_sort_show_checkboxes()
            self.weight_text.setEnabled(True)
            self.label_22.setEnabled(True)
        else:
            self.weight_text.setEnabled(False)
            self.label_22.setEnabled(False)

    def date_checkboxes(self):
        if not self.year_checkbox.isChecked():
            self.month_checkbox.setChecked(False)
            self.day_checkbox.setChecked(False)
        if not self.month_checkbox.isChecked():
            self.year_checkbox.setChecked(False)
            self.day_checkbox.setChecked(False)
        if not self.day_checkbox.isChecked():
            self.year_checkbox.setChecked(False)
            self.month_checkbox.setChecked(False)

    def date_show_checkboxes(self):
        if self.date_checkbox.isChecked():
            self.file_type_checkbox.setChecked(False)
            self.type_sort_show_checkboxes()
            self.weight_checkbox.setChecked(False)
            self.weight_show_checkboxes()
            self.year_checkbox.setEnabled(True)
            self.month_checkbox.setEnabled(True)
            self.day_checkbox.setEnabled(True)
            self.label_23.setEnabled(True)
        else:
            self.year_checkbox.setEnabled(False)
            self.month_checkbox.setEnabled(False)
            self.day_checkbox.setEnabled(False)
            self.label_23.setEnabled(False)

    def type_sort_show_checkboxes(self):
        if self.file_type_checkbox.isChecked():
            self.weight_checkbox.setChecked(False)
            self.weight_show_checkboxes()
            self.date_checkbox.setChecked(False)
            self.date_show_checkboxes()
            self.simple_checkbox.setEnabled(True)
            self.label_4.setEnabled(True)
            self.photo_checkbox.setEnabled(True)
            self.video_checkbox.setEnabled(True)
            self.text_checkbox.setEnabled(True)
            self.audio_checkbox.setEnabled(True)
            self.archive_checkbox.setEnabled(True)
            self.executable_checkbox.setEnabled(True)
            self.code_checkbox.setEnabled(True)
            self.else_checkbox.setEnabled(True)
            self.label_19.setEnabled(True)
        else:
            self.simple_checkbox.setEnabled(False)
            self.label_4.setEnabled(False)
            self.photo_checkbox.setEnabled(False)
            self.video_checkbox.setEnabled(False)
            self.text_checkbox.setEnabled(False)
            self.audio_checkbox.setEnabled(False)
            self.archive_checkbox.setEnabled(False)
            self.executable_checkbox.setEnabled(False)
            self.code_checkbox.setEnabled(False)
            self.else_checkbox.setEnabled(False)
            self.label_19.setEnabled(False)

    def save_preference(self):
        pref_dict = {
            "just_move": 1 if self.without_sort_checkbox.isChecked() else 0,
            "weight_sort": 1 if self.weight_checkbox.isChecked() else 0,
            "weight_text": self.weight_text.toPlainText(),
            "date_sort": 1 if self.date_checkbox.isChecked() else 0,
            "year_date_sort": 1 if self.year_checkbox.isChecked() else 0,
            "month_date_sort": 1 if self.month_checkbox.isChecked() else 0,
            "day_date_sort": 1 if self.day_checkbox.isChecked() else 0,
            "type_sort": 1 if self.file_type_checkbox.isChecked() else 0,
            "simple_sort": 1 if self.simple_checkbox.isChecked() else 0,
            "photo": 1 if self.photo_checkbox.isChecked() else 0,
            "video": 1 if self.video_checkbox.isChecked() else 0,
            "text": 1 if self.text_checkbox.isChecked() else 0,
            "audio": 1 if self.audio_checkbox.isChecked() else 0,
            "archive": 1 if self.archive_checkbox.isChecked() else 0,
            "executable": 1 if self.executable_checkbox.isChecked() else 0,
            "code": 1 if self.code_checkbox.isChecked() else 0,
            "else": 1 if self.else_checkbox.isChecked() else 0,
        }
        self.dc.make_user_preference(pref_dict)

    def execute_pref(self):
        pref_dict = list(self.dc.return_preferences().values())
        self.without_sort_checkbox.setChecked(bool(int(pref_dict[0])))
        self.weight_checkbox.setChecked(bool(int(pref_dict[1])))
        self.weight_text.setPlainText(pref_dict[2])
        self.date_checkbox.setChecked(bool(int(pref_dict[3])))
        self.year_checkbox.setChecked(bool(int(pref_dict[4])))
        self.month_checkbox.setChecked(bool(int(pref_dict[5])))
        self.day_checkbox.setChecked(bool(int(pref_dict[6])))
        self.file_type_checkbox.setChecked(bool(int(pref_dict[7])))
        self.simple_checkbox.setChecked(bool(int(pref_dict[8])))
        self.photo_checkbox.setChecked(bool(int(pref_dict[9])))
        self.video_checkbox.setChecked(bool(int(pref_dict[10])))
        self.text_checkbox.setChecked(bool(int(pref_dict[11])))
        self.audio_checkbox.setChecked(bool(int(pref_dict[12])))
        self.archive_checkbox.setChecked(bool(int(pref_dict[13])))
        self.executable_checkbox.setChecked(bool(int(pref_dict[14])))
        self.code_checkbox.setChecked(bool(int(pref_dict[15])))
        self.else_checkbox.setChecked(bool(int(pref_dict[16])))

    def closeEvent(self, event):
        self.directories_window.close()
        self.types_window.close()
        self.help_window.close()


class DesktopDirectories(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"Directories.ui", self)
        self.setWindowIcon(QtGui.QIcon(r"finicon.ico"))
        self.dc = dc()
        self.confirm_label.hide()
        self.initUI()

    def initUI(self):
        self.setFixedSize(520, 800)
        self.setWindowTitle('dcDirectories')

        self.simple_checkbox.clicked.connect(self.simple_sort_checkbox)

        self.reset_button.clicked.connect(self.reset_file_directories)
        self.save_all_button.clicked.connect(self.save_all_directories)

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
        directory = QFileDialog.getExistingDirectory(self)
        new_directory = ""
        for i in directory:
            if i != "/":
                new_directory += i
            else:
                new_directory += "\\"
        return new_directory

    def reset_file_directories(self):
        if self.confirm_checkbox.isChecked():
            self.confirm_label.hide()
            self.dc.reset_file_directories()
            self.dc.reset_simple_sort()
            file_directories = self.dc.return_file_directories()
            simple_directories = self.dc.return_simple_directories()
            keys = list(file_directories.keys())
            simple_values = list(simple_directories.values())
            self.from_text.setPlainText(simple_values[0])
            self.where_text.setPlainText(simple_values[1])

            self.photo_text.setPlainText(keys[0])
            self.video_text.setPlainText(keys[1])
            self.text_text.setPlainText(keys[2])
            self.audio_text.setPlainText(keys[3])
            self.archive_text.setPlainText(keys[4])
            self.executable_text.setPlainText(keys[5])
            self.code_text.setPlainText(keys[6])
            self.else_text.setPlainText(keys[7])
        else:
            self.confirm_label.show()

    def save_all_directories(self):
        if not self.simple_checkbox.isChecked():
            new_directories = {
                "photo": self.photo_text.toPlainText(),
                "video": self.video_text.toPlainText(),
                "text": self.text_text.toPlainText(),
                "audio": self.audio_text.toPlainText(),
                "archive": self.archive_text.toPlainText(),
                "executable": self.executable_text.toPlainText(),
                "code": self.code_text.toPlainText(),
                "else": self.else_text.toPlainText(),
            }
            self.dc.update_simple_sort(self.from_text.toPlainText(), from_flag=True)
            self.dc.update_file_directories(new_directories)
        else:
            new_directories = {
                "from": self.from_text.toPlainText(),
                "where": self.where_text.toPlainText()
            }
            self.dc.update_simple_sort(new_directories)


class DesktopTypes(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"FileType.ui", self)
        self.initUI()
        self.setWindowIcon(QtGui.QIcon(r"finicon.ico"))
        self.dc = dc()

    def initUI(self):
        self.setFixedSize(560, 620)
        self.setWindowTitle('dcFileTypes')
        self.show_button.clicked.connect(self.show_types)
        self.save_button.clicked.connect(self.save_types)
        self.reset_button.clicked.connect(self.reset_file_types)

    def format_extensions(self, extensions_list):
        formatted_extensions = [f'{ext}' for ext in extensions_list]
        result_string = ' '.join(formatted_extensions)
        return result_string

    def show_types(self):
        file_types = list(self.dc.return_file_types().values())
        self.photo_text.setPlainText(self.format_extensions(file_types[0]))
        self.video_text.setPlainText(self.format_extensions(file_types[1]))
        self.text_text.setPlainText(self.format_extensions(file_types[2]))
        self.audio_text.setPlainText(self.format_extensions(file_types[3]))
        self.archive_text.setPlainText(self.format_extensions(file_types[4]))
        self.executable_text.setPlainText(self.format_extensions(file_types[5]))
        self.code_text.setPlainText(self.format_extensions(file_types[6]))

    def save_types(self):
        new_file_types = {
            "photo": self.photo_text.toPlainText().split(" "),
            "video": self.video_text.toPlainText().split(" "),
            "text": self.text_text.toPlainText().split(" "),
            "audio": self.audio_text.toPlainText().split(" "),
            "archive": self.archive_text.toPlainText().split(" "),
            "executable": self.executable_text.toPlainText().split(" "),
            "code": self.code_text.toPlainText().split(" "),

        }
        self.dc.update_file_types(new_file_types)

    def reset_file_types(self):
        if self.confirm_checkbox.isChecked():
            self.dc.reset_file_types()
            file_types = self.dc.return_file_types()
            keys = list(file_types.values())
            self.photo_text.setPlainText(self.format_extensions(keys[0]))
            self.video_text.setPlainText(self.format_extensions(keys[1]))
            self.text_text.setPlainText(self.format_extensions(keys[2]))
            self.audio_text.setPlainText(self.format_extensions(keys[3]))
            self.archive_text.setPlainText(self.format_extensions(keys[4]))
            self.executable_text.setPlainText(self.format_extensions(keys[5]))
            self.code_text.setPlainText(self.format_extensions(keys[6]))


class DesktopHelp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_page = 1
        self.setWindowIcon(QtGui.QIcon(r"finicon.ico"))

    def initUI(self):
        self.setFixedSize(540, 540)
        self.setWindowTitle('dcHelp')
        self.pixmap = QPixmap(r"help_resize.png")
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(6480, 540)
        self.image.setPixmap(self.pixmap)

        self.right_button = QPushButton(self)
        self.right_button.resize(108, 27)
        self.right_button.move(427, 508)
        self.right_button.setText("След. Страница")
        self.right_button.clicked.connect(self.change_page_right)

        self.left_button = QPushButton(self)
        self.left_button.resize(108, 27)
        self.left_button.move(5, 508)
        self.left_button.setText("След. Страница")
        self.left_button.clicked.connect(self.change_page_left)

    def change_page_right(self):
        self.image.move((self.current_page * (-540)), 0)
        if self.current_page < 11:
            self.current_page += 1
        else:
            self.current_page = 0
            self.image.move((self.current_page * (-540)), 0)

    def change_page_left(self):
        if self.current_page != 0:
            self.current_page -= 1
        else:
            self.current_page = 12
        if self.current_page != 0:
            self.image.move((self.current_page * (-540)) + 540, 0)
        else:
            self.current_page = 11
            self.image.move((self.current_page * (-540)), 0)


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
