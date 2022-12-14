import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def read_aoi_diff_and_labels():
    excel = pd.read_excel("./1112 10片2448網片偏移量與焊接測試結果/1112 10片2448網片偏移量與焊接測試結果_AOI_sorted.xlsx")
    e1 = excel.iloc[:20, 4: 7]
    e2 = excel.iloc[:20, 17: 20]
    e2.columns = e1.columns
    df_excel = pd.concat([e1, e2], ignore_index=True)
    df_excel.columns = ["AOI偏差值", "品質(上)", "品質(下)"]
    return df_excel


df = read_aoi_diff_and_labels()
lst = []
for i, j in zip(df["品質(上)"], df["品質(下)"]):
    if (i == j) & (i == "OK"):
        lst.append(i)
    else:
        lst.append(j)
df["label"] = lst

df_OK = df[df["label"] == "OK"]
df_NG = df[df["label"] == "NG"]

threshold1 = 0.75
threshold2 = 1.5

print("[OK] 總個數: ", len(df_OK))
print("[OK] < 0.75 個數: ", len(df_OK[df_OK["AOI偏差值"] < threshold1]))
print("[OK] 0.75 ~ 1.5 個數: ", len(df_OK[(df_OK["AOI偏差值"] >= threshold1) & (df_OK["AOI偏差值"] <= threshold2)]))
print("[OK] > 1.5 個數: ", len(df_OK[df_OK["AOI偏差值"] > threshold2]))
print("[NG] 總個數: ", len(df_NG))
print("[NG] < 0.75 個數: ", len(df_NG[df_NG["AOI偏差值"] < threshold1]))
print("[NG] 0.75 ~ 1.5 個數: ", len(df_NG[(df_NG["AOI偏差值"] >= threshold1) & (df_NG["AOI偏差值"] <= threshold2)]))
print("[NG] > 1.5 個數: ", len(df_NG[df_NG["AOI偏差值"] > threshold2]))

exit(0)
fig = make_subplots(rows=1, cols=3, shared_yaxes=True)
fig.add_trace(
    go.Box(y=df["AOI偏差值"], name="Original"),
    row=1, col=1
)
fig.add_trace(
    go.Box(y=df_OK["AOI偏差值"], name="OK"),
    row=1, col=2
)
fig.add_trace(
    go.Box(y=df_NG["AOI偏差值"], name="NG"),
    row=1, col=3
)
fig.update_layout(height=600, width=1200, title_text="AOI偏差比較")
fig.show()
