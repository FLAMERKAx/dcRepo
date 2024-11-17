import os
import shutil
from datetime import datetime, timedelta

file_directories = {}
if not os.path.exists("FileDirectories.txt"):
    file_directories = {
        'photo': 'photos',
        'video': 'videos',
        'text': 'photos',
        'audio': 'audios',
        'archive': 'archives',
        'executable': 'executables',
        'code': 'codes',
        'else': 'else'
    }
    with open("FileDirectories.txt", "w+", encoding="UTF-8") as directories:
        keys = list(file_directories.keys())
        values = list(file_directories.values())
        for i in range(len(keys)):
            directories.write(f"{keys[i]}|{values[i]}\n")
else:
    with open("FileDirectories.txt", "r", encoding="UTF-8") as directories:
        lines = directories.readlines()
        keys = []
        values = []
        for i in lines:
            values.append(i[i.find("|") + 1:].rstrip("\n").split())
            keys.append(i[:i.find("|")])
        for i in range(len(keys)):
            file_directories[keys[i]] = values[i]

file_types = {}
if not os.path.exists("FileTypes.txt"):
    file_types = {
        'photo': ['.jpeg', '.jpg', '.png', '.tiff', '.webp', '.svg'],
        'video': ['.webm', '.mkv', '.flv', '.ogg', '.gif', '.avi', '.wmv', '.mp4', '.m4p', '.m4v'],
        'text': ['.txt', '.rtf', '.pdf', '.doc', '.docx'],
        'audio': ['.mp3', '.flac', '.m4a', '.wma', '.aac', '.ec3', '.flp', '.mtm', '.wav'],
        'archive': ['.zip', '.rar', '.7z', '.pkg', '.z'],
        'executable': ['.exe', '.apk', '.bat', '.bin', '.msi'],
        'code': ['.cpp', '.py', '.pyw', '.jar']
    }
    with open("FileTypes.txt", "w", encoding="UTF-8") as types:
        keys = list(file_types.keys())
        values = list(file_types.values())
        new_values = values
        buffer_values = ""
        for i in range(len(new_values)):
            for value in new_values:
                for file_type in value:
                    buffer_values = buffer_values + f"{file_type} "
                new_values.pop(0)
                types.write(f"{keys[i]}|{buffer_values}\n")
                buffer_values = ""
                break
else:
    with open("FileTypes.txt", "r", encoding="UTF-8") as directories:
        lines = directories.readlines()
        keys = []
        values = []
        for i in lines:
            values.append(i[i.find("|") + 1:].rstrip("\n").split())
            keys.append(i[:i.find("|")])
        for i in range(len(keys)):
            file_types[keys[i]] = values[i]


class Cleaner:
    def __init__(self):
        """Класс для переноса, удаления и сортировки файлов"""

    def get_file_type(self, file_path):
        """Выводит тип файла, на вход принимает его путь"""
        input_file = os.path.splitext(file_path)[1]
        for name, file_type in file_types.items():
            if input_file in file_type:
                return name

    def save_log(self, event, file_path=""):
        """Вписывает лог действия в текстовой файл с логами"""
        if not os.path.exists("logs.txt"):
            log_file = open("logs.txt", "w")
            log_file.close()
        with open("logs.txt", "a", encoding="UTF-8") as log_file:
            now_time = datetime.now()
            date_with_time = now_time.strftime("%d.%m.%Y %H:%M:%S")
            log_file.write(f"{date_with_time}||{event}||{file_path}\n")

    def move_file(self, file_path, final_destination="", make_log=True):
        """Переносит файл в соответсвующую его типу файла папку или по указанному пути"""
        if final_destination == "":
            final_destination = file_directories[self.get_file_type(file_path)][0]
        if os.path.exists(file_path) and os.path.exists(final_destination):
            shutil.move(file_path, final_destination)
            if make_log:
                self.save_log("Move", f"{file_path}->{final_destination}")
            return True
        else:
            return False

    def delete_file(self, file_path):
        """Удаляет файл по его пути"""
        if os.path.exists(file_path):
            os.remove(file_path)
            self.save_log("Delete", f"{file_path}")
            return True
        else:
            return False

    def undo_move(self, date, time_start, time_stop):
        """Отменяет все действия в указанном отрезке времени из логов"""
        with open("logs.txt", "a+") as log_file:
            logs = log_file.readlines()
            real_time_start = str(timedelta(seconds=time_start))
            real_time_stop = str(timedelta(seconds=time_stop))
            for line in logs:
                time_start_position = 0
                if line.find(f"{date} {real_time_start}") != -1:
                    time_start_position += 1
                    break
                else:
                    time_start_position += 1
            for line in logs[time_start_position:]:
                time_stop_position = 0
                if line.find(f"{date} {real_time_stop}") != -1:
                    time_stop_position += 1
                    break
                else:
                    time_stop_position += 1
            for event in logs[time_start_position:time_stop_position]:
                list_of_events = event.rstrip("\n").split("||")
                if list_of_events[1] == "Move":
                    file_path = list_of_events[2].split("->")[0]
                    destination_path = list_of_events[2].split("->")[1]
                    self.move_file(file_path, destination_path, make_log=False)
                    self.save_log("Undo", file_path)

    def move_folder(self, folder_path, destination_folder=""):
        """Перемещает файлы из одной папки в другую"""
        if destination_folder == "":
            for folder, subfolder, files in os.walk(folder_path):
                for folder_file in files:
                    folder_file = os.path.join(folder, folder_file)
                    self.move_file(folder_file)
            self.save_log("FolderMove")
        else:
            for folder, subfolder, files in os.walk(folder_path):
                for folder_file in files:
                    folder_file = os.path.join(folder, folder_file)
                    self.move_file(folder_file, final_destination=destination_folder)
            self.save_log("FolderMoveWithDestination")

    def delete_folder_with_files(self, folder_path):
        """Удаляет папку вместе с файлами внутри нее"""
        for folder, subfolder, files in os.walk(folder_path):
            for folder_file in files:
                folder_file = os.path.join(folder, folder_file)
                self.delete_file(folder_file)
        os.rmdir(folder_path)
        self.save_log("FolderWithFilesDeleted")

    def update_file_types(self, types_list):
        """Обновляет словарь типов файла по запросу пользователя"""
        with open("FileTypes.txt") as dict_directories:
            dict_lines = dict_directories.readlines()
            dict_keys = []
            dict_values = types_list
            for dict_line in dict_lines:
                dict_values.append(dict_line[dict_line.find("|") + 1:].rstrip("\n").split())
                dict_keys.append(dict_line[:dict_line.find("|")])
            for dict_line in range(len(dict_keys)):
                file_types[dict_keys[dict_line]] = dict_values[dict_line]

    def update_file_directories(self, dir_list):
        """Обновляет словарь директорий файлов по запросу пользователя"""
        with open("FileDirectories.txt") as dict_directories:
            dict_lines = dict_directories.readlines()
            dict_keys = []
            dict_values = dir_list
            for dict_line in dict_lines:
                dict_values.append(dict_line[dict_line.find("|") + 1:].rstrip("\n").split())
                dict_keys.append(dict_line[:dict_line.find("|")])
            for dict_line in range(len(dict_keys)):
                file_directories[dict_keys[dict_line]] = dict_values[dict_line]

    def return_file_directories(self):
        """Выводит словарь директорий файлов"""
        return file_directories

    def return_file_types(self):
        """Выводит словарь типов файлов"""
        return file_types


# TODO: в коде
#   1. Добавить создание папок из файла с директориями
#   2. Добавить создание одной папки
#   3. Добавить удаление папки без файлов
#   4. Добавить CSV файл(возможно со статистикой)
#   5. Добавить сортировку по размеру или времени создания или по пользовательскому условию
#   (один тип данных, определенное количество, не все файлы сразу)
#   6. Инструкции быстрого доступа
#   7. Добавить условия для отката действий
#   8. Добавить функционал для else типа файла в move_file
#   9. Добавить создание одной папки "Очистка от {Дата}" в которой будут все папки
#   10. Добавить возможность переименовывать файлы
#   11. Добавить возможность сделать для каждой папки создать свое название
#   13. Обновлять словари по христиански
#   14. json типа?

# TODO: В дизайнере
#   1. Добавить диалоговое окно для ввода директорий
#   2. Добавить кнопки для действий(сохранить, отобразить)
#   3. Добавить на главный экран подсказки, также как и на другие окна
#   4. Добавить UI для пользовательских сценариев
#   5. Добавить либо окно либо на главном экране статистику по программе(количество действий и прочее)
#   6. Добавить возможность менять цвет фона для пользовательского сценария
#   7. (Каким-то способом) Добавить диалоговое окно с чекбоксами для выбора директорий
#   8. Добавить выбор условий и настройки текущей очистки на главный экран
