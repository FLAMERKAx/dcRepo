import os
import shutil
from datetime import datetime

DESKTOP = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

preferences = {}
if not os.path.exists("Preferences.txt"):
    preferences = {
        "just_move": False,
        "weight_sort": False,
        "weight_text": 0,
        "date_sort": False,
        "year_date_sort": False,
        "month_date_sort": False,
        "day_date_sort": False,
        "type_sort": True,
        "simple_sort": True,
        "photo": True,
        "video": True,
        "text": True,
        "audio": True,
        "archive": True,
        "executable": True,
        "code": True,
        "else": True
    }
    with open("Preferences.txt", "w", encoding="UTF-8") as simple_output:
        keys = list(preferences.keys())
        values = list(preferences.values())
        for i in range(len(keys)):
            simple_output.write(f"{keys[i]}|{values[i]}\n")
else:
    with open("Preferences.txt", "r", encoding="UTF-8") as simple_output:
        lines = simple_output.readlines()
        keys = list(preferences.keys())
        values = list(preferences.values())
        for i in lines:
            values.append(i[i.find("|") + 1:].rstrip("\n"))
            keys.append(i[:i.find("|")])
        for i in range(len(keys)):
            preferences[keys[i]] = values[i]

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
    simple_file_directories = {
        'photo': fr"{list(simple_directories.values())[1]}\photos",
        'video': fr"{list(simple_directories.values())[1]}\videos",
        'text': fr"{list(simple_directories.values())[1]}\text",
        'audio': fr"{list(simple_directories.values())[1]}\audios",
        'archive': fr"{list(simple_directories.values())[1]}\archives",
        'executable': fr"{list(simple_directories.values())[1]}\executables",
        'code': fr"{list(simple_directories.values())[1]}\codes",
        "else": fr"{list(simple_directories.values())[1]}\else"
    }
    with open("SimpleSortFileDirectories.txt", "w", encoding="UTF-8") as simple_output:
        keys = list(simple_file_directories.keys())
        values = list(simple_file_directories.values())
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
        'text': 'text',
        'audio': 'audios',
        'archive': 'archives',
        'executables': 'executables',
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
        self.stop = False

    def get_file_type(self, file_path):
        """Выводит тип файла, на вход принимает его путь"""
        input_file = os.path.splitext(file_path)[1]
        for name, file_type in file_types.items():
            if input_file in file_type:
                return name

    def convert_bytes(self, num):
        """Возвращает вес в самой подходящей для него единице измерения информации"""
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if num < 1024.0:
                return "%3.2f %s" % (num, x)
            num /= 1024.0

    def get_file_size(self, file_path):
        """Возвращает вес файла по его пути"""
        if os.path.isfile(file_path):
            file_info = os.stat(file_path)
            return file_info.st_size

    def get_file_creation_time(self, file_path):
        """Возвращает дату создания файла по его пути"""
        if os.path.isfile(file_path):
            c_time = os.path.getctime(file_path)
            dt_c = datetime.fromtimestamp(c_time)
            return str(dt_c).split(" ")[0].split("-")

    def save_log(self, event, file_path=""):
        """Вписывает лог действия в текстовой файл с логами"""
        if not os.path.exists("logs.txt"):
            log_file = open("logs.txt", "w")
            log_file.close()
        with open("logs.txt", "a", encoding="UTF-8") as log_file:
            now_time = datetime.now()
            date_with_time = now_time.strftime("%d.%m.%Y %H:%M:%S")
            log_file.write(f"{date_with_time}||{event}||{file_path}\n")

    def move_file(self, file_path, final_destination=None, make_log=True, simple_sort=False, exceptions=None):
        """Переносит файл в соответсвующую его типу файла папку или по указанному пути"""
        if exceptions is None:
            exceptions = []
        if simple_sort:
            try:
                final_destination = simple_sort_file_directories[self.get_file_type(file_path)]
            except KeyError:
                final_destination = simple_sort_file_directories["else"]
        else:
            if final_destination is None:
                try:
                    final_destination = file_directories[self.get_file_type(file_path)]
                except KeyError:
                    final_destination = file_directories["else"]
                if final_destination == "":
                    return None
        if os.path.exists(file_path) and os.path.exists(final_destination):
            if (self.get_file_type(file_path) not in exceptions and self.get_file_type(file_path) != None) or (
                    (self.get_file_type(file_path) == None) and ("else" not in exceptions)):
                try:
                    shutil.move(file_path, final_destination)
                    if make_log:
                        self.save_log("Move", f"{file_path}->{final_destination}")
                except shutil.Error:
                    self.stop = True
            else:
                pass
            return True
        else:
            return False

    def just_move(self):
        """Функция переноса файлов из одной папки в другую без сортировки"""
        self.save_log("FolderMove")
        final_destination = list(self.return_simple_directories().values())[1]
        folder_path = list(self.return_simple_directories().values())[0]
        for folder, subfolder, files in os.walk(folder_path):
            for folder_file in files:
                if not self.stop:
                    file_path = fr"{folder}\{folder_file}"
                    if os.path.exists(file_path) and os.path.exists(final_destination):
                        try:
                            shutil.move(file_path, final_destination)
                            self.save_log("Move", f"{file_path}->{final_destination}")
                        except shutil.Error:
                            self.stop = True
                else:
                    self.stop = False
                    return True

    def date_folder_move(self, file_path, date_type):
        """Функция переноса папки для выбранного типа сортировки по дате"""
        files_list = []
        main_folder = ""
        first_folder = ""
        flag = False
        for folder, subfolder, files in os.walk(file_path):
            if first_folder == "":
                first_folder = folder
            if not flag:
                for folder_file in files:
                    if main_folder == "":
                        main_folder = folder
                    else:
                        if main_folder == folder:
                            pass
                        else:
                            flag = True
                            break
                    folder_file = fr"{folder}\{folder_file}"
                    files_list.append(folder_file)
        if date_type == "date_year":
            years = []
            for file in files_list:
                years.append(self.get_file_creation_time(file)[0])
            set_years = set(years)
            for year in list(set_years):
                if not os.path.exists(fr"{first_folder}\{year}"):
                    self.make_directory(first_folder, year)
            for file in files_list:
                file_directory = fr"{first_folder}\{self.get_file_creation_time(file)[0]}"
                self.move_file(file, file_directory, make_log=True)
        if date_type == "date_month":
            months = []
            for file in files_list:
                months.append(self.get_file_creation_time(file)[1])
            set_months = set(months)
            for month in list(set_months):
                if not os.path.exists(fr"{first_folder}\{month}"):
                    self.make_directory(first_folder, month)
            for file in files_list:
                file_directory = fr"{first_folder}\{self.get_file_creation_time(file)[1]}"
                self.move_file(file, file_directory, make_log=True)
        if date_type == "date_day":
            days = []
            for file in files_list:
                days.append(self.get_file_creation_time(file)[2])
            set_days = set(days)
            for day in list(set_days):
                if not os.path.exists(fr"{first_folder}\{day}"):
                    self.make_directory(first_folder, day)
            for file in files_list:
                file_directory = fr"{first_folder}\{self.get_file_creation_time(file)[2]}"
                self.move_file(file, file_directory, make_log=True)

    def move_folder(self, folder_path, simple=False, exceptions_list=None, sort_mode="type", file_weight=0):
        """Перемещает файлы из одной папки в другую"""
        if exceptions_list is None:
            exceptions_list = []
        self.save_log("FolderMove")
        for folder, subfolder, files in os.walk(folder_path):
            for folder_file in files:
                if not self.stop:
                    folder_file = fr"{folder}\{folder_file}"
                    if sort_mode == "weight":
                        if self.get_file_size(folder_file) < file_weight * 1024 * 1024:
                            continue
                        else:
                            self.move_file(folder_file)
                    if sort_mode == "date_year":
                        self.date_folder_move(folder_file, "year")
                    else:
                        self.move_file(folder_file, simple_sort=simple, exceptions=exceptions_list)
                else:
                    self.stop = False
                    return True

    def delete_file(self, file_path):
        """Удаляет файл по его пути"""
        if os.path.exists(file_path):
            os.remove(file_path)
            self.save_log("Delete", f"{file_path}")
            return True
        else:
            return False

    def delete_folder(self, folder_path, with_folder=False):
        """Удаляет папку вместе с файлами внутри нее"""
        if with_folder:
            main_folder = ""
            flag = False
            for folder, subfolder, files in os.walk(folder_path):
                if not flag:
                    for folder_file in files:
                        if main_folder == "":
                            main_folder = folder
                        else:
                            if main_folder == folder:
                                pass
                            else:
                                flag = True
                                break
                        folder_file = fr"{folder}\{folder_file}"
                        self.delete_file(folder_file)
            try:
                os.rmdir(folder_path)
            except OSError:
                for folder, subfolder, files in os.walk(folder_path):
                    for folder_file in files:
                        folder_file = fr"{folder}\{folder_file}"
                        self.delete_file(folder_file)
            self.save_log("FolderWithFilesDeleted")
        else:
            main_folder = ""
            flag = False
            for folder, subfolder, files in os.walk(folder_path):
                if not flag:
                    for folder_file in files:
                        if main_folder == "":
                            main_folder = folder
                        else:
                            if main_folder == folder:
                                pass
                            else:
                                flag = True
                                break
                        folder_file = fr"{folder}\{folder_file}"
                        self.delete_file(folder_file)
            self.save_log("FilesWithoutFolderDeleted")

    def undo_move(self):
        """Отменяет все действия в указанном отрезке времени из логов"""
        with open("logs.txt", "r", encoding="UTF-8") as log_file:
            logs = log_file.readlines()
            logs.reverse()
            counter = 0
            for i in logs:
                counter += 1
                if i.split("||")[1] == "FolderMove":
                    break
            logs.reverse()
            new_logs_files = []
            for event in logs[len(logs) - counter + 1:]:
                list_of_events = event.rstrip("\n").split("||")
                if list_of_events[1] == "Move":
                    file_path = list_of_events[2].split("->")[0]
                    destination_path = list_of_events[2].split("->")[1]
                    file = ""
                    for letter in file_path[::-1]:
                        if letter != "\\":
                            file += letter
                        else:
                            break
                    file = file[::-1]
                    new_file_path = destination_path + "\\" + file
                    new_file_destination = file_path[:len(file_path) - len(file) - 1]
                    new_logs_files.append(f"{new_file_path}->{new_file_destination}")
                    if not self.stop:
                        self.move_file(new_file_path, new_file_destination, make_log=False)
            new_logs = []
            for i in logs[:len(logs) - counter]:
                new_logs.append(f"{i}")
            print(new_logs)
        with open("logs.txt", "w", encoding="UTF-8") as output:
            for i in new_logs:
                output.write(i)
        self.save_log("Undo")

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

    def update_simple_sort(self, dictionary, from_flag=False):
        """Обновляет файл с простой сортировкой"""
        if not from_flag:
            with open("SimpleSortDirectories.txt", "w+", encoding="UTF-8") as output_file:
                for i in range(len(list(dictionary.keys()))):
                    keys = list(dictionary.keys())
                    values = list(dictionary.values())
                    output_file.write(f"{keys[i]}|{values[i]}\n")
            simple_file_directories = {
                'photo': fr"{values[1]}\photos",
                'video': fr"{values[1]}\videos",
                'text': fr"{values[1]}\text",
                'audio': fr"{values[1]}\audios",
                'archive': fr"{values[1]}\archives",
                'executable': fr"{values[1]}\executables",
                'code': fr"{values[1]}\codes",
                "else": fr"{values[1]}\else"
            }
            with open("SimpleSortFileDirectories.txt", "w", encoding="UTF-8") as simple_output:
                keys = list(simple_file_directories.keys())
                values = list(simple_file_directories.values())
                for i in range(len(keys)):
                    simple_output.write(f"{keys[i]}|{values[i]}\n")
        else:
            where = open("SimpleSortDirectories.txt", "r", encoding="UTF-8").readlines()[1].rstrip("\n")
            with open("SimpleSortDirectories.txt", "w", encoding="UTF-8") as output_file:
                from_folder = f"from|{dictionary}"
                output_file.write(f"{from_folder}\n{where}\n")

    def update_file_directories(self, directories_dictionary):
        """Обновляет словарь директорий файлов по запросу пользователя"""
        with open("FileDirectories.txt", "w", encoding="UTF-8") as output_file:
            for i in range(len(list(directories_dictionary.keys()))):
                keys = list(directories_dictionary.keys())
                values = list(directories_dictionary.values())
                output_file.write(f"{keys[i]}|{values[i]}\n")

    def return_file_directories(self):
        """Возвращает словарь директорий файлов"""
        return file_directories

    def return_file_types(self):
        """Возвращает словарь типов файлов"""
        return file_types

    def return_simple_directories(self):
        """Возвращает словарь директорий для простой сортировки"""
        return simple_directories

    def return_simple_file_directories(self):
        """Возвращает словарь директорий типов файлов простой сортировки"""
        return simple_sort_file_directories

    def return_preferences(self):
        """Возвращает словарь с путями простой сортировки"""
        new_preferences = {}
        with open("Preferences.txt", "r", encoding="UTF-8") as simple_output:
            lines = simple_output.readlines()
            keys = list(preferences.keys())
            values = list(preferences.values())
            for i in lines:
                values.append(i[i.find("|") + 1:].rstrip("\n"))
                keys.append(i[:i.find("|")])
            for i in range(len(keys)):
                new_preferences[keys[i]] = values[i]
        return new_preferences

    def reset_file_directories(self):
        """Сбрасывает файл с директориями файлов до базовых значений"""
        new_file_directories = {
            'photo': 'photos',
            'video': 'videos',
            'text': 'text',
            'audio': 'audios',
            'archive': 'archives',
            'executables': 'executables',
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
            'executables': ['.exe', '.apk', '.bat', '.bin', '.msi'],
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

    def reset_simple_sort(self):
        """Сбрасывает файл с простым типом сортировки"""
        simple_directories = {
            "from": DESKTOP,
            "where": "SortedFiles"
        }
        with open("SimpleSortDirectories.txt", "w", encoding="UTF-8") as simple_output:
            keys = list(simple_directories.keys())
            values = list(simple_directories.values())
            for i in range(len(keys)):
                simple_output.write(f"{keys[i]}|{values[i]}\n")
        simple_directories = {
            'photo': fr"{list(simple_directories.values())[1]}\photos",
            'video': fr"{list(simple_directories.values())[1]}\videos",
            'text': fr"{list(simple_directories.values())[1]}\text",
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

    def make_directory(self, directory_path, directory_name):
        """Создает в указанном пути папку с определенным названием"""
        os.mkdir(fr"{directory_path}\{directory_name}")

    def make_simple_sort_directories(self, where_directory):
        """Создает в выбранном пути 7 папок для сортировки в них файлы по их типу"""
        initial_file_direcrtories = ["photos", "videos", "text", "audios", "archives", "executables", "codes", "else"]
        for el in initial_file_direcrtories:
            self.make_directory(where_directory, el)

    def make_user_preference(self, preference_dict):
        """Сохраняет выбранные пользователем настройки"""
        with open("Preferences.txt", "w", encoding="UTF-8") as output_file:
            for i in range(len(list(preference_dict.keys()))):
                keys = list(preference_dict.keys())
                values = list(preference_dict.values())
                output_file.write(f"{keys[i]}|{values[i]}\n")

    def analyze_folder(self, folder_path, subfolder_flag=False):
        """Функция для анализа папки, указанной пользователем"""
        files_with_size = []
        main_folder = ""
        flag = False
        for folder, subfolder, files in os.walk(folder_path):
            if not flag and subfolder_flag is False:
                for folder_file in files:
                    if main_folder == "":
                        main_folder = folder
                    else:
                        if main_folder == folder:
                            pass
                        else:
                            flag = True
                            break
                    folder_file = fr"{folder}\{folder_file}"
                    files_with_size.append((folder_file, self.get_file_size(folder_file)))
            elif subfolder_flag:
                for folder_file in files:
                    folder_file = fr"{folder}\{folder_file}"
                    files_with_size.append((folder_file, self.get_file_size(folder_file)))
        files_with_size = sorted(files_with_size, key=lambda size: size[1])
        folder_size = 0
        for i in files_with_size:
            folder_size += i[1]
        folder_file_types = []
        for i in files_with_size:
            folder_file_types.append(self.get_file_type(i[0]))
        photo = folder_file_types.count("photo")
        video = folder_file_types.count("video")
        audio = folder_file_types.count("audio")
        text = folder_file_types.count("text")
        archive = folder_file_types.count("archive")
        executable = folder_file_types.count("executable")
        code = folder_file_types.count("code")
        else1 = folder_file_types.count(None)
        print(folder_file_types)
        return [folder_path, len(files_with_size), self.convert_bytes(folder_size),
                photo, video, text, audio, archive, executable, code, else1]
