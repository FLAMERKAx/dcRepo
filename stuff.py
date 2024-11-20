import dcCode

dc = dcCode.Cleaner()
try:
    final_destination = dcCode.file_directories[dc.get_file_type(fr"D:\test\1.ai")][0]
except KeyError:
    final_destination = dcCode.file_directories["else"]
print(final_destination)
