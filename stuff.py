file_types = {
    'photo': ['.jpeg', '.jpg', '.png', '.tiff', '.webp', '.svg'],
    'video': ['.webm', '.mkv', '.flv', '.ogg', '.gif', '.avi', '.wmv', '.mp4', '.m4p', '.m4v'],
    'text': ['.txt', '.rtf', '.pdf', '.doc', '.docx'],
    'audio': ['.mp3', '.flac', '.m4a', '.wma', '.aac', '.ec3', '.flp', '.mtm', '.wav'],
    'archive': ['.zip', '.rar', '.7z', '.pkg', '.z'],
    'executable': ['.exe', '.apk', '.bat', '.bin', '.msi'],
    'code': ['.cpp', '.py', '.pyw', '.jar']
}
new_values = list(file_types.values())
buffer_values = ""
for _ in range(len(new_values)):
    for file_types in new_values:
        for file_type in file_types:
            buffer_values = buffer_values + f"{file_type} "
        new_values.pop(0)
        break
print(buffer_values)
