import pandas as pd
import json
import numpy as np
from scipy.fftpack import fft


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


data = pd.read_csv("df_no_noice.csv")
df_labels = pd.read_json("new-labels.json")
df_labels = pd.DataFrame.from_records(df_labels["label"][0])
df_labels['timeserieslabels'] = [','.join(map(str, l)) for l in df_labels['timeserieslabels']]
df_labels['timeserieslabels'] = df_labels['timeserieslabels'].map({"normal": "OK", "abnormal": "NG"})

agg_funcs = ["min", "max", "mean", rms, "var", "std", power, peak, p2p, crest_factor, "skew", "kurt"]
features = ["min", "max", "mean", "rms", "var", "std", "power", "peak", "p2p", "crest_factor", "skew", "kurt"]
agg_funcs_f = ["max", "sum", "mean", "var", peak, "skew", "kurt"]
features_f = ["max_f", "sum_f", "mean_f", "var_f", "peak_f", "skew_f", "kurt_f"]
df = pd.DataFrame()

for start, end in zip(df_labels["start"], df_labels["end"]):
    data_ = data["CT"].iloc[start: end]

    # Time domain
    time_domain_list = data_.agg(agg_funcs).to_list()

    # Frequency domain
    N = len(data_)
    t_n = 2
    T = t_n / N

    ft_values = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)
    ft_ = fft(data_.values)
    ft = 2.0 / N * np.abs(ft_[0: N // 2])
    frequency_domain_list = pd.Series(ft).agg(agg_funcs_f).tolist()

    df = pd.concat([df, pd.DataFrame(time_domain_list + frequency_domain_list).T],
                   ignore_index=True)

df.columns = features + features_f
df["label"] = df_labels["timeserieslabels"]
print(df)
df.to_csv("./1112 10片2448網片偏移量與焊接測試結果/1st_output.csv", index=False)


