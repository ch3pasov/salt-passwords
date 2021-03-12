import time
import os
import numpy as np
import pandas as pd
from modules import sha_256
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("size", type=int, help="size of ur db")
args = parser.parse_args()

adress = os.path.dirname(__file__)
start_time = time.time()


def sha(salt, text):
    return hex(sha_256.sha_256_text(salt+text).arg)


top_200 = pd.read_csv(f'{adress}/files/crafted/top-200.csv', usecols=[0])
top_200_passwords = np.array(top_200['password'])

db_size = args.size
data = pd.read_csv(f'{adress}/files/crafted/salted_db_{db_size}.csv',
                   index_col=0, usecols=[0, 1])
data["password"] = np.nan

indexes = np.array(data.index)
benchmark = False
start_loop_time = time.time()
for i in range(len(data)):
    for j in range(len(top_200)):
        if sha(f'id{str(indexes[i])}+',
               top_200_passwords[j]) == data.loc[data.index[i]]['hash']:
            data.loc[data.index[i], 'password'] = top_200_passwords[j]
            break

    if not benchmark:
        wasted = (time.time() - start_loop_time)
        if wasted > 60:
            print(f'{i+1} rows by {wasted} seconds.')
            print(f'{db_size/(i+1)*wasted - wasted} seconds remaining')
            benchmark = True

data.to_csv(f"{adress}/files/crafted/salted_db_hacked_{db_size}.csv",
            index=True)

print(f'hacked db saved at \
{adress}/files/crafted/salted_db_hacked_{db_size}.csv')

print(f"--- {(time.time() - start_time)} seconds ---")
