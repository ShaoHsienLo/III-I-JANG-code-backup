import numpy as np
import pydot
from numpy import newaxis
import pandas as pd
import os

from sklearn.tree import export_graphviz

from datatransformation import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score



def show_performances(rf, X_test_norm, y_test, target_names=None):
    y_pred = rf.predict(X_test_norm)

    print("Confusion metric:\n{}\n".format(classification_report(y_test, y_pred, target_names=target_names)))

    print('importance:\n', rf.feature_importances_)
    # importrances = {'feature': feature_list, 'importance': rf.feature_importances_}
    # importrances_df = pd.DataFrame(data=importrances).sort_values(by=['importance'], ascending=False)
    # print("Feature importances:\n{}\n".format(importrances_df))

    score = roc_auc_score(y_test, rf.predict_proba(X_test)[:, 1])
    print("ROC SUC score:\n{}\n".format(score))


def visualization(rf, feature_list):
    tree = rf.estimators_[5]
    export_graphviz(tree, out_file='./visualization/tree.dot', feature_names=feature_list, rounded=True, precision=1)
    (graph,) = pydot.graph_from_dot_file('./visualization/tree.dot')
    graph.write_png('./visualization/tree.png')


# 標記結果全落在允收範圍(欄位：original-label)，故依照當時情況自行判斷標記結果(欄位：self-label)
# 依焊接先後順序排序
self_labels = [
    ["NG", "NG", "NG", "NG"], ["NG", "NG", "NG", "NG"], ["NG", "OK", "NG", "NG"], ["NG", "NG", "NG", "OK"],
    ["NG", "NG", "NG", "NG"], ["NG", "NG", "NG", "OK"], ["NG", "OK", "NG", "NG"], ["NG", "NG", "NG", "NG"],
    ["NG", "OK", "NG", "NG"]
]
label_lst = []
for _, lst in enumerate(self_labels):
    for label in lst:
        label_lst.append(label)
label_lst = np.array(label_lst)

df = pd.read_json("new-labels.json")
json_data = df["label"][0]
df = pd.DataFrame.from_records(json_data)
df["self-label"] = label_lst
print(df)
exit(0)
# path = r"C:\Users\samuello\Downloads\III\2022專案\韌性\data"
# file = "data.csv"
every_piece_length = 1500
# data = pd.read_csv(os.path.join(path, file))
# data_lst = []
# for i in range(len(df)):
#     start = int(df["start"].iloc[i])
#     data_lst.append(data[start: start + every_piece_length]["CT"].values)
# data_lst = np.array(data_lst)
# data_lst = data_lst[:, :, newaxis]
# np.save("data", data_lst)
data_lst = np.load("data.npy")

idx = int(len(data_lst) * 0.8)
X_train = data_lst[:idx]
X_test = data_lst[idx:]
Y_train = label_lst[:idx]
Y_test = label_lst[idx:]
print(X_train.shape, Y_train.shape, X_test.shape, Y_test.shape)
N = every_piece_length
t_n = 2
T = t_n / N
f_s = 1000
denominator = 10
X_train, y_train = extract_features_labels(X_train, Y_train, T, N, f_s, denominator)
X_test, y_test = extract_features_labels(X_test, Y_test, T, N, f_s, denominator)
print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)

clf = RandomForestClassifier(n_estimators=1000)
clf.fit(X_train, Y_train)
show_performances(clf, X_test, y_test)

print("Accuracy on training set is : {}".format(clf.score(X_train, Y_train)))
print("Accuracy on test set is : {}".format(clf.score(X_test, Y_test)))
Y_test_pred = clf.predict(X_test)
print(classification_report(Y_test, Y_test_pred))






