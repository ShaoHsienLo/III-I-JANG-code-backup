import pandas as pd
from scipy.signal import savgol_filter
from scipy.stats import zscore


df = pd.read_csv("../data/data.csv")
# df = pd.read_csv("df_no_noice.csv")
df = df[530000:545000]

sf = savgol_filter(df["CT"], 81, 6)
z_score = zscore(sf)
index = [i for i, x in enumerate(z_score) if x > 0][0]
print(index+530000)

# df_ = pd.DataFrame(columns=df.columns)
# piece_length = 1500
# idx = 0
# idx_list = []
# state = "not working"
# while idx < len(df):
#     mqtt_data = df["CT"][idx: idx + 500]
#     sf = savgol_filter(mqtt_data, 81, 6)
#     if (max(sf) - min(sf) > 10) & (state == "not working"):
#         z_score = zscore(mqtt_data)
#         index = [i for i, x in enumerate(z_score) if x > 0][0]
#         idx_list.append(idx+index+530000)
#         state = "working"
#     elif (max(sf) - min(sf) <= 10) & (state == "working"):
#         state = "not working"
#     idx = idx + 500
#
# print(idx_list)

