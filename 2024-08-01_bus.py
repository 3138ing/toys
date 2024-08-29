# %%
import sys
sys.path.insert(0, '../toys-data')
import conf

# %%
"""
좌표표시: https://www.geoplaner.com/
버스정류장ID: https://data.seoul.go.kr/dataList/OA-15067/S/1/datasetView.do
버스노선ID:https://data.seoul.go.kr/dataList/OA-15262/F/1/datasetView.do

세곡동:NODE_ID[122000314] ARS_ID[23421]
361:버스노선ID[100100454]

NEXT:
    데이터 분석
        ### case 2-1 데이터 검토
"""
''

# %%
import requests
from urllib import parse
import xml.etree.ElementTree as ElementTree
import datetime, time

# %%
def log(msg):
    with open('../toys-data/var/log/bus.log', 'ab') as f:
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        text = f'{date},{msg}'
        #
        f.write(f'{text}\n'.encode())
        f.flush()
        #

def elog(msg):
    with open('../toys-data/var/log/bus_error.log', 'ab') as f:
        date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        text = f'{date},{msg}'
        #
        f.write(f'{text}\n'.encode())
        f.flush()
        #
        print(text)

# %%
def get_response():
    try:
        serviceKey = conf.DATA_GO_KR_SERVICEKEY

        url = 'http://ws.bus.go.kr/api/rest/buspos/getBusPosByRouteSt?'
        query = [('serviceKey', serviceKey), ('busRouteId', '100100454'), ('startOrd', '1'), ('endOrd', '6')]

        url += parse.urlencode(query, encoding='UTF-8', doseq=True)
        return requests.get(url)
    except Exception as ex:
        print(ex)
        return None

# %%
def get_items(element):
    if element.tag != 'ServiceResult':
        elog('[Error][xml] ServiceResult')
        return None
    if element[0].tag != 'comMsgHeader':
        elog('[Error][xml] ServiceResult > comMsgHeader')
        return None
    if element[1].tag != 'msgHeader':
        elog('[Error][xml] ServiceResult > msgHeader')
        return None
    if element[2].tag != 'msgBody':
        elog('[Error][xml] ServiceResult > msgBody')
        return None
    if len(element[2]) > 0:
        return element[2]
    return None

# %%
### xml schema

# response = get_response()
# root = ElementTree.fromstring(response.content)
# ElementTree.indent(root)
# print(ElementTree.tostring(root, encoding='unicode'))

# <ServiceResult>
#   <comMsgHeader />
#   <msgHeader>
#     <headerCd>0</headerCd>
#     <headerMsg>정상적으로 처리되었습니다.</headerMsg>
#     <itemCount>0</itemCount>
#   </msgHeader>
#   <msgBody>
#     <itemList>
#       <busType>1</busType> 차량유형 (0:일반버스, 1:저상버스, 2:굴절버스)
#       <congetion>0</congetion> 혼잡도(0 : 없음, 3 : 여유, 4 : 보통, 5 : 혼잡, 6 : 매우혼잡)
#       <dataTm>20240806102316</dataTm> 제공시간
#       <isFullFlag>0</isFullFlag> 만차여부
#       <lastStnId>111000117</lastStnId> 최종정류소 고유 ID
                                        # NODE_ID	ARS_ID	정류소명
                                        # 123000661	24506	복정역환승센터4번승강장
                                        # 122000312	23419	삼일자동차학원.강남자동차검사소
                                        # 122000313	23420	광연자동차학원앞
                                        # 122000746	23467	강남세곡체육공원
                                        # 122000314	23421	세곡동
                                        # 122000719	23405	세곡동주민센터
#       <plainNo>서울74사4573</plainNo>
#       <posX>192704.8333534726</posX>
#       <posY>456948.94109010464</posY>
#       <routeId>100100118</routeId> 노선 ID
#       <sectDist>13</sectDist> 구간옵셋거리(Km)
#       <sectOrd>10</sectOrd> 구간순번
#       <sectionId>111700443</sectionId> 구간 ID
                                        #               lastid 1:1매칭됨
                                        # 123703042
                                        # 122702657
                                        # 122704881
                                        # 122704882
                                        # 122704527
                                        # 122704526     
#       <stopFlag>1</stopFlag>정류소도착여부 (0:운행중, 1:도착)
#       <tmX>126.917365</tmX>
#       <tmY>37.612057</tmY>
#       <vehId>111049702</vehId>
#     </itemList>
#   </msgBody>
# </ServiceResult>


# <ServiceResult>
#   <comMsgHeader />
#   <msgHeader>
#     <headerCd>4</headerCd>
#     <headerMsg>결과가 없습니다.</headerMsg>
#     <itemCount>0</itemCount>
#   </msgHeader>
#   <msgBody />
# </ServiceResult>


# %%
def main():
    response = get_response()
    if response == None:
        return
    items = None
    try:
        root = ElementTree.fromstring(response.content)
        items = get_items(root)
    except Exception as ex:
        elog(ex)

    line = ''
    if items is not None:
        for item in items:
            for index in range(len(item)):
                line += ',' + item[index].text
    log(str(int(datetime.datetime.now().timestamp())) + line)

# %%
while True:
    main()
    time.sleep(60)

# %%
### df 만들기: log to df

info_length = 16
rows = []
linenumber = 0
with open('../toys-data/var/log/bus.log', 'r') as f:
    while True:
        line = f.readline()
        if not line:
            break
        linenumber += 1
        line = line.strip()
        # if len(line) == 0:
        #     continue

        splits = line.split(',')
        splits_length = len(splits)
        col = [-1] * (info_length + 2)
        if splits_length == (info_length + 2):
            col = splits.copy()
            rows.append(col.copy())
        elif splits_length == 2:
            col[:2] = splits[:2]
            rows.append(col.copy())
        elif splits_length == info_length * 2 + 2:
            col[:info_length + 2] = splits[:info_length + 2]
            rows.append(col.copy())
            col[:2] = splits[:2]
            col[2:info_length * 1 + 2] = splits[info_length * 1 + 2:info_length * 2 + 2]
            rows.append(col.copy())
        elif splits_length == info_length * 3 + 2:
            col[:info_length + 2] = splits[:info_length + 2]
            rows.append(col.copy())
            col[:2] = splits[:2]
            col[2:info_length * 1 + 2] = splits[info_length * 1 + 2:info_length * 2 + 2]
            rows.append(col.copy())
            col[:2] = splits[:2]
            col[2:info_length * 2 + 2] = splits[info_length * 2 + 2:info_length * 3 + 2]
            rows.append(col.copy())
        else:
            print('type1', splits_length, linenumber, line, col)
            break

import pandas as pd
col_name = ['datetime', 'ticket', 'busType', 'congetion', 'dataTm', 'isFullFlag', 'lastStnId', 'plainNo', 'posX', 'posY', 'routeId', 'sectDist', 'sectOrd', 'sectionId', 'stopFlag', 'tmX', 'tmY', 'vehId']
df = pd.DataFrame(rows, columns=col_name)
df.set_index('datetime', inplace=True)
df = df[(df != -1).all(axis=1)]

# %%
### 컬럼추가 vehOrd, uuid

last_date = ''
plainNo_dict = {} # plainNo_dict[plainNo] = (count, )
rows_vehOrd = []
rows_uuid = []
for row in df.itertuples(index=True, name='Pandas'):
    current_plainNo = row[7]
    current_date = row[0][:10]
    currnet_sectOrd = row[12]

    if last_date != current_date:
        count = 0
        plainNo_dict = {}
        last_date = current_date
    if current_plainNo == -1:
        plainNo_dict[-1] = (-1, -1)
    else: 
        if current_plainNo not in plainNo_dict:
            count += 1
            plainNo_dict[current_plainNo] = (count, currnet_sectOrd)
        else:
            if currnet_sectOrd == '1' and plainNo_dict[current_plainNo][1] != '1':
                plainNo_dict[current_plainNo] = (count, currnet_sectOrd)
                count += 1
            else:
                plainNo_dict[current_plainNo] = (plainNo_dict[current_plainNo][0], currnet_sectOrd)
    rows_vehOrd.append(plainNo_dict[current_plainNo][0])
    rows_uuid.append(str(plainNo_dict[current_plainNo][0]) + '_' + row[13] + '_' + current_date)
df['vehOrd'] = rows_vehOrd
df['uuid'] = rows_uuid

# %%
### 분석

pd.set_option('display.max_rows', 10)
# df[(df['busType'] != -1) & (df['plainNo'] == '서울74사7840')][['plainNo', 'vehOrd', 'sectOrd', 'vehId']]

# %%
### 분석

# df[(df['plainNo'] == '서울74사1948')&(df['lastStnId'] == '123000661')]
# df[(df['sectDist'] != '0')&(df['sectionId'] == '123703042')]
# df[df['plainNo'] == '서울74사1948']
# df[df['lastStnId'] == '122000719']['sectionId'].unique()
# df['stopFlag'].unique()
# pd.set_option('display.max_rows', 1000)

# %%
### case 2-1 동일 UUID 중 가장 큰(작은) 시간만 남기기

df.loc[df.groupby('uuid')['dataTm'].idxmax()].sort_index()
#df
#df_merge = df.loc[df.groupby('A')['B'].idxmax()]


# %%
### case 1-1
### sectionId 가 123703042일 때 => meaning: 첫번째 정류장
### 거리(sectDist)가 0이 아닐 때로 merge => meaning: 출발했다

df_start = df[(df['sectionId'] == '123703042')].copy()
### columns
# print(df_start.columns)
# Index(['ticket', 'busType', 'congetion', 'dataTm', 'isFullFlag', 'lastStnId',#  1 2 3 4 5 6
#        'plainNo', 'posX', 'posY', 'routeId', 'sectDist', 'sectOrd', # 7 8 9 10 11 12
#        'sectionId', 'stopFlag', 'tmX', 'tmY', 'vehId'], # 13 14 15 16 17
#       dtype='object')
last_vehId = '0'
last_datetime = None

rows_time = []
for row in df_start.itertuples(index=True, name='Pandas'):
    if last_vehId == row[-1]:
        continue
    last_vehId = row[-1]
    gap = 0

    current_datetime = datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
    if last_datetime != None:
        gap = current_datetime - last_datetime
    last_datetime = current_datetime
    rows_time.append([row[0].split(' ')[1]])
    print(row[17])
    #rows_time.append([row[0].split(' ')[1][:5]])
    #print(row[0].split(' ')[1])

col_name = ['time']
df_time = pd.DataFrame(rows_time, columns=col_name)
df_time.sort_values('time', inplace=True)
#df_time['time'] = pd.to_datetime(df_time['time'], format='%H:%M:%S')
#df_time.groupby('time')['time'].count().sort_index()
#df_time

# %%
### case 1-2

rows_time = []
last_time = None
for row in df_time.itertuples(index=True, name='Pandas'):
    if last_time == None:
        last_time = datetime.datetime.strptime(row[1], "%H:%M:%S")
    else:
        current_time = datetime.datetime.strptime(row[1], "%H:%M:%S")
        if current_time - last_time > datetime.timedelta(minutes=5): 
            rows_time.append(row[1]) # 수정(평균치로 append)
        last_time = current_time

col_name = ['time']
df_time_merge = pd.DataFrame(rows_time, columns=col_name)
#df_time_merge.sort_values('time', inplace=True)
df_time_merge['time'] = pd.to_datetime(df_time_merge['time'], format='%H:%M:%S')
#df_time_merge.groupby('time')['time'].count().sort_index()
#df_time_merge

# %%
### case 1-3

import matplotlib.pyplot as plt

df_copy = df_time_merge.copy()

# df_time = pd.DataFrame({
#     'time': ['13:42:11', '15:23:45', '09:12:34']
# })
# df_time['time'] = pd.to_datetime(df_time['time'], format='%H:%M:%S')

import matplotlib.dates as mdates
start_time = datetime.datetime.strptime('03:00:00', '%H:%M:%S')
end_time = datetime.datetime.strptime('20:00:00', '%H:%M:%S')
df_copy = df_copy[(df_copy['time'] >= start_time) & (df_copy['time'] <= end_time)]
plt.figure(figsize=(20, 6))
plt.plot(df_copy['time'], [1]*len(df_copy), 'o')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
plt.xlim([start_time, end_time])

plt.xlabel('Time')
plt.yticks([])
plt.title('Time Distribution')
plt.grid(True)
plt.xticks(rotation=45)

# 그래프 출력
plt.show()


