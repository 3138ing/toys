import sys
sys.path.insert(0, '../toys-data')
import pay

filename_head = '../toys-data/var/paymoneyList_s_'
filename_result = filename_head + 'result'

def tsum(str1, str2):
    int1 = 0
    int2 = 0
    if len(str1) != 0:
        int1 = int(str1.replace(',', ''))
    if len(str2) != 0:
        int2 = int(str2.replace(',', ''))
    return format(-int1 + int2, ',')

def payopen(num):
    filename = filename_head + num
    print(filename)

    with open(filename_result, 'a') as wf:
        with open(filename, 'rb') as rf:
            while True:
                line = rf.readline()
                if not line:
                    break
                line = line.decode()
                splits = line.split(';')
                if len(splits) != 8:
                    continue
                if splits[0].find('-') == -1:
                    continue
                
                part1 = '?'
                part2 = '?'
                title = splits[5]
                description = '?'

                title, part1, part2, description = pay.shinhan(title, part1, part2, description, splits)

                data = []
                data.append(splits[0][0:4] + '년')
                data.append(splits[0][5:7] + '월')
                data.append(splits[0][8:10] + '일')
                data.append('신한')
                data.append(part1)
                data.append(part2)
                data.append(title)
                data.append(description)
                data.append(tsum(splits[3], splits[4]))

                wf.write('\t'.join(data) + '\n')

with open(filename_result, 'w') as f:
    pass

start = 0
end = 0

for i in range(start, end+1):
    num = str(i)
    if num == '83':
        num = '83_start'
    if num == '96':
        num = '96*'
    payopen(num)