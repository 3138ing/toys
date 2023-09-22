import json
import datetime

pay = __import__('2023-08-29_pay')

filename_head = 'paymoneyList_n_'
filename_result = filename_head + 'result'

요일 = '월화수목금토일'

def payopen(num):
    filename = filename_head + num
    print(filename)

    with open(filename, 'r') as f:
        paymoneyList = json.load(f)

    with open(filename_result, 'a') as f:
        for item in paymoneyList['result']['response']['list']:
            if item["PAYDTTM"] is None:
                print("PAYDTTM", item)
                break
            if item["PAYAMT"] is None:
                print("PAYAMT", item)
                break

            part1 = '-'
            part2 = '-'
            title = item["TITLE"]
            description = item["DESCRIPTION"]

            title, part1, part2, description = pay.naver(title, part1, part2, description)

            data = []
            data.append("'" + item["PAYDTTM"][0:4])
            data.append("'" + item["PAYDTTM"][4:6])
            data.append("'" + item["PAYDTTM"][6:8])
            data.append(요일[datetime.datetime.strptime(item["PAYDTTM"][0:8], "%Y%m%d").weekday()])
            data.append('하나')
            data.append(part1)
            data.append(part2)
            data.append(title)
            data.append(description)
            data.append(format(item['PAYAMT'], ','))

            f.write('\t'.join(data) + '\n')

            if title != "네이버파이낸셜" and description != '-':
                if title != "네이버페이충전":
                    print(data)

with open(filename_result, 'w') as f:
    pass

start = 0
end = 1

for i in range(start, end+1):
    num = str(i)
    if num == '83':
        num = '83_start'
    if num == '96':
        num = '96*'
    payopen(num)
