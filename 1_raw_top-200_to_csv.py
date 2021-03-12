import os
import numpy as np
import pandas as pd

adress = os.path.dirname(__file__)

np_csv = np.array([['password', 'frequency']])

with open(f"{adress}/files/dont_touch/top-200_raw") as f:
    for line in f:
        l_splitted = line.split()
        if l_splitted != []:
            np_csv = np.append(np_csv,
                               [[l_splitted[1], l_splitted[3]]], axis=0)

# print(np_csv)
pd_csv = pd.DataFrame(data=np_csv)
new_header = pd_csv.iloc[0]
pd_csv = pd_csv[1:]
pd_csv.columns = new_header
print(pd_csv)

pd_csv.to_csv(f"{adress}/files/crafted/top-200.csv", index=False)
