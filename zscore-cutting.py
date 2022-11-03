import pandas as pd


df = pd.read_csv("1112 10片2448網片偏移量與焊接測試結果/1102(label-studio-ver).csv")
ct = df["CT_zscore"].values

state = "not working"
i = 0
threshold = -0.45
start_lst = []
end_lst = []

while i < len(ct):
    if ((i > 294400) & (i < 295700)) | \
            ((i > 403000) & (i < 407000)):
        i = i + 1
        continue

    if (ct[i] > threshold) & (state == "not working"):
        start_lst.append(i)
        state = "working"
    elif (ct[i] <= threshold) & (state == "working"):
        if max(ct[i: i+100]) < 0:
            end_lst.append(i)
            state = "not working"
    i = i + 1
i = 0

# print(len(start_lst))
# for i in range(len(start_lst)):
#     print(start_lst[i], end_lst[i])
# print()
# th = [0, 100000, 360000, 460000, 550000, 635000, 700000,
#       770000, 840000, 900000, len(ct)]
# i = 0
# while i < len(th):
#     print(len([x for x in end_lst
#                if (x > th[i]) & (x < th[i + 1])]))
#     i = i + 1

with open("1112 10片2448網片偏移量與焊接測試結果/cutting-index.txt", "w") as f:
    f.write(str(start_lst))
    f.write("\n")
    f.write(str(end_lst))


