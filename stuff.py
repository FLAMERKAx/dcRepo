import os
import datetime
path = "logs.txt"

# file creation timestamp in float
c_time = os.path.getctime(path)
# convert creation timestamp into DateTime object
dt_c = datetime.datetime.fromtimestamp(c_time)
print(str(dt_c).split(" ")[0])
