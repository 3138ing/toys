import sys
sys.path.insert(0, '../toys-data')
import pay

import json
import datetime
import sys

def get_node(object, node_name_list):
    search_object = object
    for node_name in node_name_list:
        if node_name in search_object:
            search_object = search_object[node_name]
        else:
            print("no", node_name)
            sys.exit(0)
    return search_object

filename_head = 'paymoneyList_n_'
filename_result = filename_head + 'result'

with open(filename_result, 'w') as f:
    None

요일 = '월화수목금토일'

har = None
with open(pay.get_har_filename(), 'r', encoding='utf-8') as f:
    har = json.load(f)

node_entries = get_node(har, ["log", "entries"])

for item in node_entries:
    node_url = get_node(item, ["request", "url"])
    if node_url == None:
        continue
    if not node_url.endswith("paymoneyList"):
        continue
    node_text = get_node(item, ["response", "content", "text"])

    paymoneyList = json.loads(node_text)

    with open(filename_result, 'a') as f:
        for item in paymoneyList['result']['response']['list']:
            if item["PAYDTTM"] is None:
                print("PAYDTTM", item)
                break
            if item["PAYAMT"] is None:
                print("PAYAMT", item)
                break

            part1 = '?'
            part2 = '?'
            part3 = '-'
            title = item["TITLE"]
            description1 = item["DESCRIPTION"]
            description2 = '-'

            title, part1, part2, part3, description1, description2 = pay.naver(title, part1, part2, part3, description1, description2)

            data = []
            data.append("=date(" + item["PAYDTTM"][0:4] +
                             "," + item["PAYDTTM"][4:6] +
                             "," + item["PAYDTTM"][6:8] + ")")
            data.append("'" + item["PAYDTTM"][0:4])
            data.append("'" + item["PAYDTTM"][4:6])
            data.append("'" + item["PAYDTTM"][6:8])
            data.append(요일[datetime.datetime.strptime(item["PAYDTTM"][0:8], "%Y%m%d").weekday()])
            data.append(title)
            data.append(description1)
            data.append(description2)
            data.append(format(item['PAYAMT'], ','))
            data.append(part3)
            data.append(part2)
            data.append(part1)
            data.append('하나')
            data.append('-')
            data.append('-')
            data.append('-')
            data.append('-')
            
            if data[1] != "'2023" or data[2] != "'05":
                continue

            f.write('\t'.join(data) + '\n')

            if title != "네이버" and description1 not in ['-', '?']:
                if title != "네이버페이충전":
                    print(data)