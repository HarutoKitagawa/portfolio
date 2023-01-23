import numpy as np
import pandas as pd
import  matplotlib.pyplot as plt

# 政府統計による、2000年から2015年の都道府県別人口推移エクセルデータを読み込む。
df = pd.read_excel('05k5-5.xlsx')

# 数値の部分のみを切り取る。
df = df.iloc[9: 57, 3:]
# 列名を設定する。一列目が県名、それ以降は年(西暦)
df.columns = ['Prefectures']+[str(i) for i in range(2000, 2016)]
# 県名の列、数値の列を分け、県名は数値データのインデックスにする。
prefectures = df.iloc[:, 0]
df = df.iloc[:, 1:]
df.index = prefectures

# 2000年から2015年までの人口増加率の列を追加し、人口増加率の降順で都道府県をソート
df['increace_rate'] = (df['2015'] - df['2000'])/df['2000']
df_sorted = df.sort_values('increace_rate', ascending=False)

#人口増加率上位・下位k県を取得
k = input('上位・下位何県を表示しますか？(整数値を入力): ')
k = int(k)
high_increace_rate_prefectures = df_sorted[0: k]
low_increace_rate_prefectures = df_sorted[df.shape[0]-k: df.shape[0]]

# ここからはデータの可視化。
x = np.arange(2000, 2016)

def listing_time_series_data(k, dataframe, prefectures):
    '時系列データを県ごとにリスト化する'
    y_list = []
    for i in range(0, k):
        y = prefectures.iloc[i, :dataframe.shape[1]-1]
        # 人口は2000年を基準に標準化
        y_normalized = y/y['2000']
        y_list.append(y_normalized)
    return y_list

# 上位・下位k県の時系列データを県ごとにリスト化
y_list_high = listing_time_series_data(k, df, high_increace_rate_prefectures)
y_list_low = listing_time_series_data(k, df, low_increace_rate_prefectures)

fig, axes = plt.subplots(1, 2, figsize=(10, 4))

for i in range(0, k):
    axes[0].plot(x, y_list_high[i], label=y_list_high[i].name)
axes[0].set_title('Upper '+str(k))
axes[0].set_xlabel('Year')
axes[0].set_ylabel('Population standardized by that of 2000')
axes[0].legend()


for i in range(0, k):
    axes[1].plot(x, y_list_low[i], label=y_list_low[i].name)
axes[1].set_title('Lower '+str(k))
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Population standardized by that of 2000')
axes[1].legend()

plt.show()