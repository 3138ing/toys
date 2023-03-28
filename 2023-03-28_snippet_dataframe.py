import pandas as pd
import numpy as np

# options
pd.set_option('display.max_rows', 500)

# list -> df
column_names_1 = ['column_name_1', 'column_name_2', 'column_name_3']
list_1 = [['a', 1, 2], ['b', 3, 4], ['c', np.NaN, 6], ['d', 17132.5132, 8]]
df_1 = pd.DataFrame(list_1, columns=column_names_1)
#print(df_1)

# index: column to index
df_1.set_index('column_name_1', inplace=True)
#print(df_1)

# index: 함수적용
df_1.index = df_1.index.map(lambda x:x+x) 
#print(df_1)

# column: 누적합(cumsum), 누적Max(cummax), 누적Min(cummin), 누적곱(cumprod)
#print(df_1['column_name_3'].cumsum())

# data: round
#print(df_1.round(-2))

# data: 결측치
#df_1.fillna(0, inplace=True)
#print(df_1)

