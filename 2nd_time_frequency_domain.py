import pandas as pd
import json
import numpy as np
from scipy.fftpack import fft


def read_data():
    df = pd.read_csv("./1112 10片2448網片偏移量與焊接測試結果/1102(label-studio-ver).csv")
    return df


def read_label_index():
    cols = ["start", "end"]
    df_labels = pd.DataFrame(columns=cols)
    with open("./1112 10片2448網片偏移量與焊接測試結果/cutting-index.txt", "r") as f:
        lines = f.readlines()
        start = json.loads(lines[0])
        end = json.loads(lines[1])
        for s, e in zip(start, end):
            df_lab = pd.DataFrame([[s, e]], columns=cols)
            df_labels = pd.concat([df_labels, df_lab], ignore_index=True)
    return df_labels


def split_data(df, df_labels):
    json_data = {}
    for i in range(len(df_labels)):
        json_data[str(i)] = df.loc[(df.index >= df_labels["start"].iloc[i]) &
                                   (df.index <= df_labels["end"].iloc[i]), "CT"].tolist()
    return json.dumps(json_data)


def save_json_data(json_data):
    with open("./1112 10片2448網片偏移量與焊接測試結果/output.txt", "w") as f:
        json.dump(json_data, f)


def read_json_data():
    with open("./1112 10片2448網片偏移量與焊接測試結果/output.txt", "r") as f:
        json_data = json.loads(json.loads(f.read().replace('\'', "")))
    return json_data


def read_aoi_labels():
    excel = pd.read_excel("./1112 10片2448網片偏移量與焊接測試結果/1112 10片2448網片偏移量與焊接測試結果_AOI.xlsx")
    e1 = excel.iloc[:20, 5: 9]
    e2 = excel.iloc[:20, 14: 18]
    e2.columns = e1.columns
    df_excel = pd.concat([e1, e2], ignore_index=True)
    labels = list(df_excel.values.flatten())
    return labels


def rms(x):
    return np.sqrt(np.mean(np.power(x.values, 2)))


def power(x):
    return np.mean(np.power(x.values, 2))


def peak(x):
    return np.max(np.abs(x.values))


def p2p(x):
    return np.ptp(x.values)


def crest_factor(x):
    return np.max(np.abs(x)) / np.sqrt(np.mean(np.power(x.values, 2)))


# df = read_data()
# df_labels = read_label_index()
# json_data = split_data(df, df_labels)
# save_json_data(json_data)

json_data = read_json_data()
labels = read_aoi_labels()

agg_funcs = ["min", "max", "mean", rms, "var", "std", power, peak, p2p, crest_factor, "skew", "kurt"]
features = ["min", "max", "mean", "rms", "var", "std", "power", "peak", "p2p", "crest_factor", "skew", "kurt"]
agg_funcs_f = ["max", "sum", "mean", "var", peak, "skew", "kurt"]
features_f = ["max_f", "sum_f", "mean_f", "var_f", "peak_f", "skew_f", "kurt_f"]
df = pd.DataFrame()

for key, label in zip(json_data.keys(), labels):
    # Time domain
    time_domain_list = pd.Series(json_data[key]).agg(agg_funcs).to_list()

    # Frequency domain
    N = len(json_data)
    t_n = 2
    T = t_n / N

    ft_values = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
    ft_ = fft(json_data[key])
    ft = 2.0 / N * np.abs(ft_[0: N // 2])
    frequency_domain_list = pd.Series(ft).agg(agg_funcs_f).tolist()

    df = pd.concat([df, pd.DataFrame(time_domain_list + frequency_domain_list).T],
                   ignore_index=True)

df.columns = features + features_f
df["label"] = labels
df.to_csv("./1112 10片2448網片偏移量與焊接測試結果/2nd_output.csv", index=False)


