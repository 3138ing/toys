import json
from html.parser import HTMLParser

class gmarket_parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.outters = []
    def handle_data(self, data):
        self.outters.append(data)

pay = __import__('2023-08-29_pay')

filename_head = 'paymoneyList_g_'
filename_result = filename_head + 'result'

def payopen(num):
    filename = filename_head + num
    print(filename)

    with open(filename, 'r') as f:
        paymoneyList = json.load(f)

    with open(filename_result, 'a') as f:
        for data in paymoneyList['data']:
            # FirstColumn
            parser = gmarket_parser()
            parser.feed(data['FirstColumn'])
            info_date = "'" + parser.outters[0].replace('\t', '_')

            # SecondColumn
            html = data['SecondColumn']

            # option
            info_option = '-'
            option_html = ''
            index_option_begin = html.find('<li class="option">')
            if index_option_begin != -1:
                index_option_last = html.find('<span>닫기</span>', index_option_begin)
                if index_option_last != -1:
                    option_html = html[index_option_begin:index_option_last + 15]
                    html = html.replace(option_html, '')
                    parser = gmarket_parser()
                    parser.feed(option_html)
                    parser.outters.pop(0) # 옵션 전체 보기
                    parser.outters.pop(0) # title
                    info_option = ''
                    for outter in parser.outters:
                        info_option += outter + '\t'
                    info_option = info_option.strip()
                    if info_option[-2:] == '닫기':
                        info_option = info_option[:-2]
                        
            #
            parser = gmarket_parser()
            parser.feed(html)
            info_seller = parser.outters[0].replace('\t', '_')
            info_name = parser.outters[1].replace('\t', '_')
            info_amount = parser.outters[2].split('/')[0].replace('\t', '_')
            info_price = parser.outters[3].replace('\t', '_')

            info_date = info_date.strip().replace('\t', '_')
            info_seller = info_seller.strip().replace('\t', '_')
            info_name = info_name.strip().replace('\t', '_')
            info_amount = info_amount.strip().replace('\t', '_').replace('수량 : ', '').replace('개', '')
            info_option = info_option.strip().replace('\t', '_')
            info_price = info_price.strip().replace('\t', '_')

            data = []
            data.append(info_date)
            data.append(info_seller)
            data.append(info_name)
            data.append(info_amount)
            data.append(info_option)
            data.append(info_price)

            f.write('\t'.join(data) + '\n')
        
with open(filename_result, 'w') as f:
    pass

start = 0
end = 6

for i in range(start, end+1):
    num = str(i)
    if num == '83':
        num = '83_start'
    if num == '96':
        num = '96*'
    payopen(num)

