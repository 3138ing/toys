import pandas as pd
import matplotlib.pyplot as plt

column_names_1 = ['column_name_1', 'column_name_2', 'column_name_3']
list_1 = [['aaaa', 1, 2], ['bbbb', 3, 4], ['cccc', 5, 6], ['dddd', 7, 8]]
df_1 = pd.DataFrame(list_1, columns=column_names_1)
df_1.set_index('column_name_1', inplace=True)

plt.figure(figsize = (20, 10))
plt.plot(df_1)
plt.axvline(x='bbbb', color='orange', linestyle='--', linewidth=1)
plt.axhline(y=5, color='red', linestyle='-.', linewidth=1)
plt.xticks(df_1.index, rotation=45)
plt.legend()

# Tableau color
#'tab:blue'
#'tab:orange'
#'tab:green'
#'tab:red'
#'tab:purple'
#'tab:brown'
#'tab:pink'
#'tab:gray'
#'tab:olive'
#'tab:cyan'
