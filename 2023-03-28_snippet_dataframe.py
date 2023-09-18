import pandas as pd
import numpy as np

# options
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 1000)

# from: list
column_names_1 = ['column_name_1', 'column_name_2', 'column_name_3', 'column_name_4']
list_1 = [['a', 1, 2, '2'], ['b', 3, 4, '4'], ['c', np.NaN, 6, '6'], ['d', 17132.5132, 8, '8']]
list_1 = [('a', 1, 2, '2'), ('b', 3, 4, '4'), ('c', np.NaN, 6, '6'), ('d', 17132.5132, 8, '8')]
df_1 = pd.DataFrame(list_1, columns=column_names_1)
print(df_1)

# from: read_csv
# encoding: 'euc-kr', 'cp949', 'utf-8'
# df_1 = pd.read_csv('d:\\test.csv', sep='\t', header=None, names=['t1', 't2'], encoding='euc-kr', skiprows=0, index_col=0)

# index: column to index
# df_1.set_index('column_name_1', inplace=True)
# print(df_1)

# index: 함수적용
# df_1.index = df_1.index.map(lambda x: x+x)
# print(df_1)

# column: type 변환
# df_1 = ddf_1.astype({'column_name_4':'int'})

# column: 누적합(cumsum), 누적Max(cummax), 누적Min(cummin), 누적곱(cumprod)
# print(df_1['column_name_3'].cumsum())

# column: 순서바꾸기
# df_1[['column_name_2', 'column_name_3', 'column_name_1']]
# column: 추가하기

# column: 이름바꾸기
# print(df_1['column_name_3'].cumsum())
# df_1.rename(columns = {'column_name_1':'column_name_10','column_name_3':'column_name_30'},inplace=True)

# column: 추가하기
# df_1['column_name_4'] = 'usa'
# df_1.loc[:, 'column_name_5'] = 'korea'
# print(df_1)

# data: round
# print(df_1.round(-2))

# data: 결측치 확인
# print(df_1.isnull().values.any()) # 결측치 있는지 True/False
# print(df_1.isnull().sum()) # 컬럼별 결측치 갯수

# data: 결측치 처리
# print(df_1.fillna(9.9999))
# print(df_1.dropna()) # "결측치 행 삭제"
# print(df_1[df_1.index.notnull()]) # index가 결측치일 경우 "결측치 행 삭제"

# data: 합치기
# pd.concat([df1, df2]) # 위아래
# pd.concat([df1, df2], axis=0) # 위아래
# pd.concat([df1, df2], axis=1) # 좌우

# groupby
# df_1[['column_name_2', 'column_name_3']].groupby('column_name_2').count()

