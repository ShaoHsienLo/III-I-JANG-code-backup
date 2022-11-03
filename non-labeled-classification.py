import pandas as pd
import numpy as np
import os
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Clustering via KMeans
df = pd.read_csv('20220520InspectData.csv')
df = df.drop(columns=['isPass'])
df.rename(columns={'VerC': 'y_diff', 'LevC': 'x_diff'}, inplace=True)
df = df[['x_diff', 'y_diff']]
print('未分類前x軸最大公差:{}，x軸最小公差:{}'.format(max(df['x_diff']), min(df['x_diff'])))
print('未分類前y軸最大公差:{}，y軸最小公差:{}'.format(max(df['y_diff']), min(df['y_diff'])))

print('分類中...')
n_clusters = np.arange(6) + 2
for n_cluster in n_clusters:
    kmeans = KMeans(n_clusters=n_cluster, random_state=n_cluster).fit(df.to_numpy())
    df['label'] = kmeans.labels_
    filtered_label_dict = {}
    # colors = ['red', 'blue', 'green', 'black', 'ornange']
    for i in range(n_cluster):
        filtered_label_dict['label_{}'.format(i)] = df[df['label'] == i]
    for i in range(n_cluster):
        plt.scatter(filtered_label_dict['label_{}'.format(i)]['x_diff'],
                    filtered_label_dict['label_{}'.format(i)]['y_diff'])
    plt.legend(['label {}'.format(i) for i in range(n_cluster)])
    # plt.show()
    plt.savefig('{}_clusters.png'.format(n_cluster))
    plt.close()

# n_clusters = np.arange(4) + 2
# for n_cluster in n_clusters:
#     kmeans = KMeans(n_clusters=n_cluster, random_state=n_cluster).fit(df.to_numpy())
#     df['label'] = kmeans.labels_
#     labels = np.unique(kmeans.labels_)
#     print('共分{}類:'.format(n_cluster))
#     for label in labels:
#         statis_x_df = df.loc[df['label'] == label, 'x_diff'].rolling(window=10).agg(['mean', 'median', 'max', 'min',
#                                                                                      'std', 'var'])
#         statis_y_df = df.loc[df['label'] == label, 'y_diff'].rolling(window=10).agg(['mean', 'median', 'max', 'min',
#                                                                                      'std', 'var'])
#         statis_x_df = statis_x_df.dropna()
#         statis_x_df = statis_x_df.reset_index(drop=True)
#         statis_x_df.to_csv('x_label{}_of_clusters{}.csv'.format(label, n_cluster), index=False)
#         statis_y_df = statis_y_df.dropna()
#         statis_y_df = statis_y_df.reset_index(drop=True)
#         statis_y_df.to_csv('y_label{}_of_clusters{}.csv'.format(label, n_cluster), index=False)
#     print()

