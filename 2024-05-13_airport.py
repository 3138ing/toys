# %%
import sys
sys.path.insert(0, '../toys-data')
import conf

# %%
import requests
from urllib import parse
import xml.etree.ElementTree as ElementTree
import datetime, time
import pandas as pd

# %%
conf.set_metplot_font('D2Coding')

# %%
column_names = ['국내선 제1주차장'
, '국내선 제2주차장'
, '국제선 주차빌딩'
, '국제선 지하'
, '화물청사']

def log(msg):
    with open('../toys-data/var/log/airport.log', 'ab') as f:
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        text = f'{date}|{msg}'
        #
        f.write(f'{text}\n'.encode())
        f.flush()
        #

def elog(msg):
    with open('../toys-data/var/log/airport_error.log', 'ab') as f:
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        text = f'{date}|{msg}'
        #
        f.write(f'{text}\n'.encode())
        f.flush()
        #
        print(text)

# %%
def get_response():
    try:
        serviceKey = conf.DATA_GO_KR_SERVICEKEY
        schAirportCode = 'GMP'

        url = 'http://openapi.airport.co.kr/service/rest/AirportParking/airportparkingRT?'
        query = [('serviceKey', serviceKey), ('schAirportCode', schAirportCode)]

        url += parse.urlencode(query, encoding='UTF-8', doseq=True)
        return requests.get(url)
    except Exception as ex:
        elog(ex)
        return None

# %%
def get_items(element):
    if element.tag != 'response':
        elog('[Error][xml] response')
        return None
    if element[0].tag != 'header':
        elog('[Error][xml] response > header')
        return None
    if element[0][0].tag != 'resultCode':
        elog('[Error][xml] response > header > resultCode')
        return None
    if element[0][0].text != '00':
        elog(f'[Error][xml] response > header > resultCode > {element[0][0].text} > {element[0][1].text}')
        return None
    if element[1].tag != 'body':
        elog('[Error][xml] response > body')
        return None
    if element[1][0].tag != 'items':
        elog('[Error][xml] response > body > items')
        return None
    if len(element[1][0]) == 0:
        elog(f'[Error][xml] response > body > items > len({len(element[1][0])})')
        return None
    return element[1][0]

# %%
# <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
# <response>
# 	<header>
# 		<resultCode>00</resultCode>
# 		<resultMsg>NORMAL SERVICE.</resultMsg>
# 	</header>
# 	<body>
# 		<items>
# 			<item>
# 				<aprEng>GIMPO INTERNATIONAL AIRPORT</aprEng>
# 				<aprKor>김포국제공항</aprKor>
# 				<parkingAirportCodeName>국내선 제1주차장</parkingAirportCodeName>
# 				<parkingFullSpace>2279</parkingFullSpace>
# 				<parkingGetdate>2024-06-05</parkingGetdate>
# 				<parkingGettime>17:33:02</parkingGettime>
# 				<parkingIincnt>2054</parkingIincnt>
# 				<parkingIoutcnt>1302</parkingIoutcnt>
# 				<parkingIstay>2135</parkingIstay>
# 			</item>
# 			<item>
# 				<aprEng>GIMPO INTERNATIONAL AIRPORT</aprEng>
# 				<aprKor>김포국제공항</aprKor>
# 				<parkingAirportCodeName>국내선 제2주차장</parkingAirportCodeName>
# 				<parkingFullSpace>1733</parkingFullSpace>
# 				<parkingGetdate>2024-06-05</parkingGetdate>
# 				<parkingGettime>17:33:02</parkingGettime>
# 				<parkingIincnt>1029</parkingIincnt>
# 				<parkingIoutcnt>610</parkingIoutcnt>
# 				<parkingIstay>1434</parkingIstay>
# 			</item>
# 			<item>
# 				<aprEng>GIMPO INTERNATIONAL AIRPORT</aprEng>
# 				<aprKor>김포국제공항</aprKor>
# 				<parkingAirportCodeName>국제선 주차빌딩</parkingAirportCodeName>
# 				<parkingFullSpace>567</parkingFullSpace>
# 				<parkingGetdate>2024-06-05</parkingGetdate>
# 				<parkingGettime>17:33:02</parkingGettime>
# 				<parkingIincnt>512</parkingIincnt>
# 				<parkingIoutcnt>359</parkingIoutcnt>
# 				<parkingIstay>506</parkingIstay>
# 			</item>
# 			<item>
# 				<aprEng>GIMPO INTERNATIONAL AIRPORT</aprEng>
# 				<aprKor>김포국제공항</aprKor>
# 				<parkingAirportCodeName>국제선 지하</parkingAirportCodeName>
# 				<parkingFullSpace>1200</parkingFullSpace>
# 				<parkingGetdate>2024-06-05</parkingGetdate>
# 				<parkingGettime>17:33:02</parkingGettime>
# 				<parkingIincnt>452</parkingIincnt>
# 				<parkingIoutcnt>263</parkingIoutcnt>
# 				<parkingIstay>1200</parkingIstay>
# 			</item>
# 			<item>
# 				<aprEng>GIMPO INTERNATIONAL AIRPORT</aprEng>
# 				<aprKor>김포국제공항</aprKor>
# 				<parkingAirportCodeName>화물청사</parkingAirportCodeName>
# 				<parkingFullSpace>737</parkingFullSpace>
# 				<parkingGetdate>2024-06-05</parkingGetdate>
# 				<parkingGettime>17:33:02</parkingGettime>
# 				<parkingIincnt>3190</parkingIincnt>
# 				<parkingIoutcnt>2579</parkingIoutcnt>
# 				<parkingIstay>737</parkingIstay>
# 			</item>
# 		</items>
# 	</body>
# </response>

# %%
def main():
    # global response
    # if response == None:
    #     response = get_response()
    response = get_response()
    if response == None:
        return
    items = None
    try:
        root = ElementTree.fromstring(response.content)
        items = get_items(root)
    except Exception as ex:
        elog(ex)
    if items == None:
        return
# <aprEng>GIMPO INTERNATIONAL AIRPORT</aprEng>    # 0
# <aprKor>김포국제공항</aprKor>    # 1
# <parkingAirportCodeName>화물청사</parkingAirportCodeName>    # 2 <-
# <parkingFullSpace>737</parkingFullSpace>    # 3 <-
# <parkingGetdate>2024-06-05</parkingGetdate>    # 4 <-
# <parkingGettime>17:33:02</parkingGettime>    # 5 <-
# <parkingIincnt>3190</parkingIincnt>    # 6
# <parkingIoutcnt>2579</parkingIoutcnt>    # 7
# <parkingIstay>737</parkingIstay>    # 8 <-
    # row_names = {}
    # for item in items:
    #     key = item[4].text + ' ' + item[5].text
    #     if key not in row_names:
    #         row_names[key] = ['-100','-100','-100','-100','-100']
    #     index = column_names.index(item[2].text)
    #     row_names[key][index] = str(int(item[3].text) - int(item[8].text))
    # for key in row_names:
    #     text = f'{key}|{"|".join(row_names[key])}'
    #     log(text)
    item_time = ''
    item_values = ['-100','-100','-100','-100','-100']
    for item in items:
        if item_time == '':
            item_time = item[4].text + ' ' + item[5].text
        index = column_names.index(item[2].text)
        item_values[index] = str(int(item[3].text) - int(item[8].text))
    text = f'{item_time}|{"|".join(item_values)}'
    log(text)

# %%
while True:
    main()
    time.sleep(60 * 10)

# %%
### set which airport

# df
names = ['assign_time']
names.extend(column_names)
df = pd.read_csv('../toys-data/var/log/airport.log', sep='|', header=None, names=names)
# drop: -100 
for column_name in column_names:
    df.drop(df[df[column_name] < -1].index, inplace=True)

# drop: date
for column_name in column_names:
    df.drop(df[df.index < '2024-07-01'].index, inplace=True)

# target column
target_column_name = column_names[0]
print(target_column_name)

# tick    
prev_tick = ''
xticks_1 = []
for index, assign_time in enumerate(df['assign_time']):
    if prev_tick != assign_time[:13]:
        hh = int(assign_time[11:13])
        if hh in (4, 5, 6):
            xticks_1.append(index)
        prev_tick = assign_time[:13]
prev_tick = ''
xticks_2 = []
for index, assign_time in enumerate(df['assign_time']):
    if prev_tick != assign_time[:13]:
        hh = int(assign_time[11:13])
        if hh in (7, 8, 18, 19):
            xticks_2.append(index)
        prev_tick = assign_time[:13]
xticks = xticks_1.copy()
xticks.extend(xticks_2)
#  plot


#df_plot = df
df_plot = df[target_column_name]
ax_one = df_plot.plot(figsize=(20,5), rot=45)
#ax_one.vlines(x=xticks_1, ymin=df_plot.min(numeric_only=True).min(), ymax=df_plot.max(numeric_only=True).max(), color='grey', linewidth=0.4)#2279
#ax_one.vlines(x=xticks_2, ymin=df_plot.min(numeric_only=True).min(), ymax=df_plot.max(numeric_only=True).max(), color='red', linewidth=0.4)


# %%
df

# %%
# df
prev_hh = -1
df_new = df[0:0].copy()
yticks = []
for index, row in df.iterrows():
    assign_time = row['assign_time']
    hh = int(assign_time[11:13])
    if prev_hh == hh:
        continue
    prev_hh = hh
    if hh != (20): # 시간
        continue
    df_new.loc[assign_time] = row
# tick
xticks_new = []
for index, assign_time in enumerate(df_new['assign_time']):
    if int(datetime.datetime.strptime(assign_time[:10], '%Y-%m-%d').strftime('%u')) == 5: # 요일:일(0)월(1)화(2)수(3)목(4)금(5)토(6)
        xticks_new.append(index)
        yticks.append(df_new.loc[assign_time][target_column_name])
# plot    
ax = df_new[target_column_name].plot(figsize=(20,5), rot=45)
ax.vlines(x=xticks_new, ymin=df_new[target_column_name].min(), ymax=df_new[target_column_name].max(), color='grey', linewidth=0.4)#2279
ax.hlines(y=yticks, xmin=0, xmax=len(df_new), color='grey', linewidth=0.4)#2279


# %%
# df
prev_hh = -1
df_new = df[0:0].copy()
yticks = []
for index, row in df.iterrows():
    assign_time = row['assign_time']
    if int(datetime.datetime.strptime(assign_time[:10], '%Y-%m-%d').strftime('%u')) != 5: # 요일:일(0)월(1)화(2)수(3)목(4)금(5)토(6)
        continue
    hh = int(assign_time[11:13])
    if prev_hh == hh:
        continue
    prev_hh = hh
    if hh != (20): # 시간
        continue
    df_new.loc[assign_time] = row
# plot    
df_new[target_column_name].plot(figsize=(20,5), rot=45)




