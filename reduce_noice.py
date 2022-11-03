from scipy.signal import savgol_filter
import pandas as pd
import os


# 原始數據
path = r"C:\Users\samuello\Downloads\III\2022專案\韌性\data"
filename = "data.csv"
data = pd.read_csv(os.path.join(path, filename))
t = data["Timestamp"]
print(data.shape)
# start_index = 150500
# end_index = 152100
# data = data[start_index:end_index]
data = data["CT"]

# savgol_filter
data_savgol_filter = savgol_filter(data, 81, 6)
data_savgol_filter = pd.DataFrame(data_savgol_filter, columns=["CT"])
data_savgol_filter.insert(0, "Timestamp", t)
print(data_savgol_filter)
# print(data.shape)
# exit(0)
data_savgol_filter.to_csv("df_no_noice.csv", index=False)

