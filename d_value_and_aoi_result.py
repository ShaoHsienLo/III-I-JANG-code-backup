import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def read_exsx_file():
    excel = pd.read_excel("./1112 10片2448網片偏移量與焊接測試結果/1112 10片2448網片偏移量與焊接測試結果_AOI_sorted.xlsx")
    return excel


def read_aoi_labels_and_d_values():
    excel = read_exsx_file()
    e1 = excel.iloc[:20, 9: 15]
    e2 = excel.iloc[:20, 24: 30]
    e1.columns = ["品質(上)", "品質(下)", "品質(上)-對角", "品質(下)-對角", "d值", "d值-對角"]
    e2.columns = e1.columns
    df = pd.concat([e1, e2], ignore_index=True)
    return df


# 分短邊與長邊
# df = read_aoi_labels_and_d_values()
# df["品質組合"] = df["品質(上)"] + df["品質(下)"]
# df["品質組合-對角"] = df["品質(上)-對角"] + df["品質(下)-對角"]
# df = df.replace("OKOK", "OK").replace("NGNG", "NG")
# df = df[["品質組合", "d值", "品質組合-對角", "d值-對角"]]
#
# df_long = pd.DataFrame()
# df_short = pd.DataFrame()
# i = 0
#
# while i < len(df):
#
#     df_long = pd.concat([df_long, df.loc[df.index == i, ["品質組合", "d值"]]], ignore_index=True)
#     df_ = df.loc[df.index == i + 1, ["品質組合-對角", "d值-對角"]]
#     df_.columns = df_long.columns
#     df_long = pd.concat([df_long, df_], ignore_index=True)
#
#     df_short = pd.concat([df_short, df.loc[df.index == i + 1, ["品質組合", "d值"]]], ignore_index=True)
#     df_ = df.loc[df.index == i, ["品質組合-對角", "d值-對角"]]
#     df_.columns = df_long.columns
#     df_short = pd.concat([df_short, df_], ignore_index=True)
#
#     i = i + 2
#
# fig = go.Figure()
# fig.add_trace(go.Box(x=df_long["品質組合"], y=df_long["d值"], name="長邊"))
# fig.add_trace(go.Box(x=df_short["品質組合"], y=df_short["d值"], name="短邊"))
# fig.write_html("./1219 d值量測結果/長邊-短邊.html")
# # fig.show()
# exit(0)

# 分OK與NG
df = read_aoi_labels_and_d_values()
df["品質組合"] = df["品質(上)"] + df["品質(下)"]
df["品質組合-對角"] = df["品質(上)-對角"] + df["品質(下)-對角"]
df = df.replace("OKOK", "OK").replace("NGNG", "NG")
df1 = df[["品質組合", "d值"]]
df2 = df[["品質組合-對角", "d值-對角"]]
df2.columns = df1.columns
df = pd.concat([df1, df2], ignore_index=True)

df_OK = df[df["品質組合"] == "OK"]
df_NG = df[df["品質組合"] == "NG"]
df_OKNG = df[df["品質組合"] == "OKNG"]
df_NGOK = df[df["品質組合"] == "NGOK"]

print("OK占比：{}/{}".format(len(df_OK), len(df)))
print("OKNG占比：{}/{}".format(len(df_OKNG), len(df)))
print("NGOK占比：{}/{}".format(len(df_NGOK), len(df)))
print("NG占比：{}/{}".format(len(df_NG), len(df)))

fig = px.box(df, x="品質組合", y="d值", points="all")
fig.write_html("./1219 d值量測結果/OK-NG.html")
# fig.show()

