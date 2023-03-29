import time

timestamp_1 = 1677723600
print(timestamp_1)

# 'timestamp(int)' -> 'struct_time'
local_time_1 = time.localtime(timestamp_1)
UTC_1 = time.gmtime(timestamp_1)
print(local_time_1, UTC_1)

# 'struct_time' -> 'formatted string'
formatted_string_1 = time.strftime('%Y-%m-%d %H:%M:%S', local_time_1)
print(formatted_string_1)



import datetime

# 'formatted string' -> int
timestamp_1 = datetime.datetime.strptime(formatted_string_1, "%Y-%m-%d %H:%M:%S").timestamp()
print(timestamp_1)

# int -> 'formatted string'
formatted_string_1 = datetime.datetime.fromtimestamp(timestamp_1).strftime('%Y-%m-%d %H:%M:%S')
print(formatted_string_1)

# datetime -> int
datetime_1 = datetime.datetime.fromtimestamp(timestamp_1)
timestamp_1 = datetime.datetime.timestamp(datetime_1)
print(timestamp_1)
