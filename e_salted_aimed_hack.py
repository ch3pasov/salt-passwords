import time
import os
import numpy as np
import pandas as pd
from modules import sha_256

adress = os.path.dirname(__file__)
start_time = time.time()


def sha(salt, text):
    return hex(sha_256.sha_256_text(salt+text).arg)


top_200 = pd.read_csv(f'{adress}/files/crafted/top-200.csv', usecols=[0])
top_200_passwords = np.array(top_200['password'])

data = pd.read_csv(f'{adress}/files/dont_touch/salted_sample_db_1000.csv',
                   index_col=0)
data = data.loc[data['surnames'] == 'NAVALNY']
data["password"] = np.nan

hash = data.loc[data.index[0], 'hash']
for j in range(len(top_200)):
    if sha(f'id{str(data.index[0])}+',
           top_200_passwords[j]) == hash:
        data.loc[data.index[0], 'password'] = top_200_passwords[j]
        break

data.to_csv(f"{adress}/files/crafted/vip_hacked.csv",
            index=True)

print(f'vip saved at \
{adress}/files/crafted/vip_hacked.csv')

print(data)

print(f"--- {(time.time() - start_time)} seconds ---")
