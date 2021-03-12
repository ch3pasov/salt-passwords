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
top_200['hash'] = [sha('', top_200['password'][i])
                   for i in range(len(top_200))]

db_size = args.size
data = pd.read_csv(f'{adress}/files/crafted/unsalt_db_{db_size}.csv',
                   index_col=0, usecols=[0, 1])
data["password"] = np.nan
for i in range(len(top_200)):
    data.loc[data['hash'] ==
             top_200['hash'][i], 'password'] = top_200['password'][i]
    if i % 10 == 0:
        print(f'{i}/{len(top_200)}')

data.to_csv(f"{adress}/files/crafted/unsalt_db_hacked_{db_size}.csv",
            index=True)

print(f'hacked db saved at \
{adress}/files/crafted/unsalt_db_hacked_{db_size}.csv')

print(f"--- {(time.time() - start_time)} seconds ---")
