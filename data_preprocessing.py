import json

import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, fftshift


def rms(x):
    return np.sqrt(np.mean(np.power(x.values, 2)))


def ptp(x):
    return np.ptp(x.values)


with open('config.json', 'r') as f:
    config = json.load(f)

read_path = r'C:\Users\samuello\Downloads\III\2022專案\韌性\data'
files = os.listdir(read_path)

for file in files:
    df = pd.read_json(os.path.join(read_path, file), lines=True)
    # df = df[['Timestamp', 'current']]
    # df = df.groupby(by=['Timestamp'], as_index=False).mean().reset_index()
    df = df['current']
    df_current = df[9:]

    df = df.rolling(window=10).agg(['mean', 'median', 'max', 'min', 'std', 'var', 'kurt', 'skew', ptp, rms])
    cols = df.columns
    df.columns = ['current' + '_' + col for col in cols]
    df = df.dropna()
    df = df.reset_index(drop=True)
    df['current'] = df_current.values

    print(df.shape)
    df.to_csv('df.csv', index=False)
    exit(0)

    # df_corr = df.corr()
    # trace = go.Heatmap(
    #     z=df_corr.values,
    #     x=df_corr.index.values,
    #     y=df_corr.columns.values,
    #     zmin=0,
    #     zmax=1,
    #     colorscale=px.colors.sequential.Reds
    # )
    # fig = go.Figure()
    # fig.add_trace(trace)
    # fig.show()

    # fig = px.line(df, x=df.index, y=df.columns)
    # fig.show()

    exit(0)



