import time
import pandas as pd
import paho.mqtt.client as mqtt
import json

from scipy.signal import savgol_filter
from scipy.stats import zscore
from sqlalchemy import create_engine, types
from datetime import datetime


# 建立全域變數，讓函數內可以使用該變數
data_ = pd.DataFrame()
data = pd.DataFrame()


def on_connect(client, userdata, flags, rc):
    # 連接程序得到響應時所做的動作(印出回應碼rc)
    print("Connected with result code " + str(rc))

    # 訂閱/再訂閱
    client.subscribe("WANG_TSUNG_1")


def on_message(client, userdata, msg):
    global data_
    global data

    data_ = pd.DataFrame(json.loads(msg.payload.decode("utf-8")))
    data_ = data_.drop(columns=["pie"])
    # data_ = pd.DataFrame(data_.mean(numeric_only=True)).transpose()
    # data_.insert(0, "timestamp", datetime.now())
    # data = data_.copy()


# mqtt連線設定
client = mqtt.Client(transport="websockets")
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("iii", "iii05076416")

# mqtt連線迴圈起始
client.loop_start()

# mqtt連線
client.connect("139.162.96.124", 8087, 60)

# 建立一個存放mqtt即時數據的變數，以下稱df
df = pd.DataFrame(columns=["timestamp", "ingot", "discharge", "mould", "oil_pressure", "bucket"])

# 顯示更新頻率(秒)
display_freqency = 0.5

# 連接postgres與設定資料型態(無自定義統一當作TEXT存入資料庫)
# engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
# sql_types = {
#     "timestamp": types.DateTime, "ingot": types.FLOAT, "discharge": types.FLOAT, "oil_pressure": types.FLOAT,
#     "mould": types.FLOAT, "bucket": types.FLOAT
# }

idx_list = []
state = "not working"

while True:

    if len(data_) == 0:
        continue

    if not data_.equals(data):
        data = data_
    else:
        continue

    mqtt_data = data.copy()
    sf = savgol_filter(mqtt_data, 81, 6)
    if (max(sf) - min(sf) > 10) & (state == "not working"):
        z_score = zscore(mqtt_data)
        index = [i for i, x in enumerate(z_score) if x > 0][0]
        idx_list.append(index)
        state = "working"
    elif (max(sf) - min(sf) <= 10) & (state == "working"):
        state = "not working"

    assert len(idx_list) % 2 == 0

    idx_list = []
    state = "not working"

    # insert_data_to_postgres(df.iloc[-1:], engine, sql_types)

    # 即時數據圖更新頻率(秒)
    time.sleep(display_freqency)

# mqtt連線迴圈結束
client.loop_stop()


def insert_data_to_postgres(df, engine, sql_types):
    try:
        df.to_sql('realtime', engine, index=False, dtype=sql_types)
    except ValueError as e:
        df.to_sql('realtime', engine, if_exists="append", index=False, dtype=sql_types)
