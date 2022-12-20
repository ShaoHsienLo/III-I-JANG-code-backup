import pandas as pd
import tsfresh.examples
from tsfresh import extract_features
import json
from tsfresh.examples import load_robot_execution_failures


with open("./1112 10片2448網片偏移量與焊接測試結果/output.txt", "r") as f:
    data = json.loads(json.loads(f.read()))
for k, v in data.items():
    data[k] = v[:500]

# df = pd.DataFrame.from_dict(data)
# extracted_features = extract_features(df)
# print(extracted_features)

df, _ = load_robot_execution_failures()
X = extract_features(df, column_id='id', column_sort='time')
# print(df)
print(X)

