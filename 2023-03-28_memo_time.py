# 'timestamp(int)' to 'struct_time'
local_time_1 = time.localtime(timestamp_1)
UTC_1 = time.gmtime(timestamp_1)

# 'struct_time' to 'formatted string'
formatted_string_1 = strftime.strftime('%H:%M:%S', struct_time_1)
