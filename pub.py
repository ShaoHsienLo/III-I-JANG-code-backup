import paho.mqtt.client as mqtt
import datetime
import random
import json
import time
import pandas as pd


df = pd.read_csv("data.csv")
df = df[100000:]

ISOTIMEFORMAT = "%Y-%m-%d %H:%M:%S"
# client = mqtt.Client(transport="websockets")
client = mqtt.Client()
client.username_pw_set("iii", "iii05076416")
client.connect("192.168.1.115", 1883, 60)
i = 0
while True:
    payload = df[i: i + 500].to_json()
    print(json.dumps(payload))
    client.publish("test", json.dumps(payload))
    i = i + 500
    time.sleep(1)
