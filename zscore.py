import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import zscore

pd.set_option("display.max_rows", 999)

# df = pd.read_csv("df_no_noice.csv")
# df["zscore"] = zscore(df["CT"])
# df["zscore_rolling"] = df["zscore"].rolling(window=200).max()
# df = df.fillna(method="bfill")
# df.to_csv("df_zscore_ct_rolling.csv", index=False)

df = pd.read_csv("df_zscore_ct_rolling.csv")
result = pd.DataFrame(columns=["index", "count"])
i_ = 0
count_ = 0
i = 15000
while i < len(df):
    df_ = df["zscore_rolling"][i - 15000: i].copy()
    count = len(df_[df_ > 0])
    # result = result.append(
    #     {"index": i, "count": count},
    #     ignore_index=True
    # )
    if (count > 1000) & (count - count_ < 0):
        i_ = i - 3000
        print("index: ", i_)
        i = i + 14000
    count_ = count
    i = i + 3000
# print(result)
