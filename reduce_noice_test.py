import pandas as pd
import statsmodels.api as sm
from tsmoothie.smoother import *
import os
import plotly.graph_objects as go
from scipy.signal import lfilter, savgol_filter

# 原始數據
path = r"C:\Users\samuello\Downloads\III\2022專案\韌性\data"
filename = "data.csv"
data = pd.read_csv(os.path.join(path, filename))
start_index = 150500
end_index = 152100
index = pd.RangeIndex(start_index, end_index)
data = data[start_index:end_index]
data = data["CT"]

# signal lfilter
# n = 10
# b = [1.0 / n] * n
# a = 1
# data_lfilter = lfilter(b, a, data)

# rolling window -> mean
# data_mean = data.rolling(window=10).mean()
# data_mean[:10] = data[:10]

# rolling window -> max
# data_max = data.rolling(window=10).max()

# signal savgol_filter
fig = go.Figure()
fig.add_trace(go.Scatter(x=index, y=data, mode='lines', name='original'))
window_length = [41, 51, 61, 71, 81]
polyorder = [3, 4, 5, 6, 6]
for w_len, poly in zip(window_length, polyorder):
    data_savgol_filter = savgol_filter(data, w_len, poly)
    fig.add_trace(go.Scatter(x=index, y=data_savgol_filter, mode='lines',
                             name='len:{}, poly:{}'.format(w_len, poly)))
fig.write_html("./filter/savgol_filter/params_compare.html")

# smoother
# smoother = ConvolutionSmoother(window_len=20, window_type='ones')
# smoother.smooth(data)

# sm
# sm_ = sm.nonparametric.lowess(data, index, frac = 0.3)

# plotly
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=index, y=data, mode='lines', name='original'))
# fig.add_trace(go.Scatter(x=index, y=data_lfilter, mode='lines', name='signal lfilter'))
# fig.add_trace(go.Scatter(x=index, y=data_mean, mode='lines', name='rolling mean'))
# fig.add_trace(go.Scatter(x=index, y=data_max, mode='lines', name='rolling max'))
# fig.add_trace(go.Scatter(x=index, y=data_savgol_filter, mode='lines', name='signal savgol_filter'))
# fig.add_trace(go.Scatter(x=index, y=smoother.smooth_data[0], mode='lines', name='smoother'))
# fig.add_trace(go.Scatter(x=sm_[:, 0], y=sm_[:, 1], mode='lines', name='sm'))



