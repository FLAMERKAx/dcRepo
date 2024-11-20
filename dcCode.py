import os
import shutil
from datetime import datetime, timedelta

DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

simple_directories = {}
if not os.path.exists("SimpleSortDirectories.txt"):
    simple_directories = {
        "from": DESKTOP,
        "where": "SortedFiles"
    }
    with open("SimpleSortDirectories.txt", "w", encoding="UTF-8") as simple_output:
        keys = list(simple_directories.keys())
        values = list(simple_directories.values())
        for i in range(len(keys)):
            simple_output.write(f"{keys[i]}|{values[i]}\n")
else:
    with open("SimpleSortDirectories.txt", "r", encoding="UTF-8") as simple_output:
        lines = simple_output.readlines()
        keys = list(simple_directories.keys())
        values = list(simple_directories.values())
        for i in lines:
            values.append(i[i.find("|") + 1:].rstrip("\n"))
            keys.append(i[:i.find("|")])
        for i in range(len(keys)):
            simple_directories[keys[i]] = values[i]

simple_sort_file_directories = {}
if not os.path.exists("SimpleSortFileDirectories.txt"):
    simple_directories = {
        'photo': fr"{list(simple_directories.values())[1]}\photos",
        'video': fr"{list(simple_directories.values())[1]}\videos",
        'text': fr"{list(simple_directories.values())[1]}\photos",
        'audio': fr"{list(simple_directories.values())[1]}\audios",
        'archive': fr"{list(simple_directories.values())[1]}\archives",
        'executable': fr"{list(simple_directories.values())[1]}\executables",
        'code': fr"{list(simple_directories.values())[1]}\codes",
        "else": fr"{list(simple_directories.values())[1]}\else"
    }
    with open("SimpleSortFileDirectories.txt", "w", encoding="UTF-8") as simple_output:
        keys = list(simple_directories.keys())
        values = list(simple_directories.values())
        for i in range(len(keys)):
            simple_output.write(f"{keys[i]}|{values[i]}\n")
else:
    with open("SimpleSortFileDirectories.txt", "r", encoding="UTF-8") as simple_output:
        lines = simple_output.readlines()
        keys = []
        values = []
        for i in lines:
            values.append(i[i.find("|") + 1:].rstrip("\n"))
            keys.append(i[:i.find("|")])
        for i in range(len(keys)):
            simple_sort_file_directories[keys[i]] = values[i]

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
            values.append(i[i.find("|") + 1:].rstrip("\n"))
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
        self.desktop = DESKTOP

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


    def move_file(self, file_path, final_destination=None, make_log=True, simple_sort=False):
        """Переносит файл в соответсвующую его типу файла папку или по указанному пути"""
        if simple_sort:
            try:
                final_destination = simple_sort_file_directories[self.get_file_type(file_path)][0]
            except KeyError:
                final_destination = simple_sort_file_directories["else"]
        else:
            if final_destination is None:
                final_destination = file_directories[self.get_file_type(file_path)][0]
                if final_destination == "":
                    return None
        if os.path.exists(file_path) and os.path.exists(final_destination):
            try:
                shutil.move(file_path, final_destination)
            except shutil.Error:
                file_path = file_path + "(copy)"
                shutil.move(file_path, final_destination)
            if make_log:
                self.save_log("Move", f"{file_path}->{final_destination}")
            return True
        else:
            return False

    def move_folder(self, folder_path, simple=False):
        """Перемещает файлы из одной папки в другую"""
        for folder, subfolder, files in os.walk(folder_path):
            for folder_file in files:
                folder_file = fr"{folder}\{folder_file}"
                self.move_file(folder_file, simple_sort=simple)
        self.save_log("FolderMove")

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
        with open("logs.txt", "a+", encoding="UTF-8") as log_file:
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
                    # УДАЛИТЬ ПОСЛЕДНИЙ ЛОГ, ДОЛБАЕБ

    def delete_folder_with_files(self, folder_path):
        """Удаляет папку вместе с файлами внутри нее"""
        for folder, subfolder, files in os.walk(folder_path):
            for folder_file in files:
                folder_file = os.path.join(folder, folder_file)
                self.delete_file(folder_file)
        os.rmdir(folder_path)
        self.save_log("FolderWithFilesDeleted")

    def update_file_types(self, types_dictionary):
        """Обновляет словарь типов файла по запросу пользователя"""
        with open("FileTypes.txt", "w", encoding="UTF-8") as output_file:
            values = list(types_dictionary.values())
            keys = list(types_dictionary.keys())
            new_values = values
            buffer_values = ""
            for i in range(len(new_values)):
                for value in new_values:
                    for file_type in value:
                        buffer_values = buffer_values + f"{file_type} "
                    new_values.pop(0)
                    output_file.write(f"{keys[i]}|{buffer_values}\n")
                    buffer_values = ""
                    break

    def update_file_directories(self, directories_dictionary):
        """Обновляет словарь директорий файлов по запросу пользователя"""
        with open("FileDirectories.txt", "w", encoding="UTF-8") as output_file:
            for i in range(len(list(directories_dictionary.keys()))):
                keys = list(directories_dictionary.keys())
                values = list(directories_dictionary.values())
                output_file.write(f"{keys[i]}|{values[i]}\n")

    def return_file_directories(self):
        """Выводит словарь директорий файлов"""
        return file_directories

    def return_file_types(self):
        """Выводит словарь типов файлов"""
        return file_types

    def return_simple_directories(self):
        """Выводит словарь директорий для простой сортировки"""
        return simple_directories

    def return_simple_file_directories(self):
        return simple_sort_file_directories

    def reset_file_directories(self):
        """Сбрасывает файл с директориями файлов до базовых значений"""
        new_file_directories = {
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
            keys = list(new_file_directories.keys())
            values = list(new_file_directories.values())
            for i in range(len(keys)):
                directories.write(f"{keys[i]}|{values[i]}\n")

    def reset_file_types(self):
        """Сбрасывает файл с типами файлов до базовых значений"""
        new_file_types = {
            'photo': ['.jpeg', '.jpg', '.png', '.tiff', '.webp', '.svg'],
            'video': ['.webm', '.mkv', '.flv', '.ogg', '.gif', '.avi', '.wmv', '.mp4', '.m4p', '.m4v'],
            'text': ['.txt', '.rtf', '.pdf', '.doc', '.docx'],
            'audio': ['.mp3', '.flac', '.m4a', '.wma', '.aac', '.ec3', '.flp', '.mtm', '.wav'],
            'archive': ['.zip', '.rar', '.7z', '.pkg', '.z'],
            'executable': ['.exe', '.apk', '.bat', '.bin', '.msi'],
            'code': ['.cpp', '.py', '.pyw', '.jar']
        }
        with open("FileTypes.txt", "w", encoding="UTF-8") as types:
            keys = list(new_file_types.keys())
            values = list(new_file_types.values())
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

    def make_directory(self, directory_name, directory_path):
        """Создает в указанном пути папку с определенным названием"""
        os.mkdir(fr"{directory_path}\{directory_name}")

    def make_simple_sort_directories(self, where_directory):
        """Создает в выбранном пути 7 папок для сортировки в них файлы по их типу"""
        for el in list(file_directories.keys()):
            os.mkdir(fr"{where_directory}\{el}")

    def update_simple_sort(self, dictionary):
        with open("SimpleSortDirectories.txt", "w+", encoding="UTF-8") as output_file:
            for i in range(len(list(dictionary.keys()))):
                keys = list(dictionary.keys())
                values = list(dictionary.values())
                output_file.write(f"{keys[i]}|{values[i]}\n")
