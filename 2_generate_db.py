import time
import os
import string
import numpy as np
import pandas as pd
from modules import sha_256
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--salted", action="store_true",
                    help="salt passwords")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
parser.add_argument("size", type=int, help="size of ur db")
args = parser.parse_args()

adress = os.path.dirname(__file__)
start_time = time.time()

if args.salted:
    db_type = 'salted'

    def sha(salt, text):
        return hex(sha_256.sha_256_text(salt+text).arg)
else:
    db_type = 'unsalt'

    def sha(salt, text):
        return hex(sha_256.sha_256_text(text).arg)

top_200 = pd.read_csv(f'{adress}/files/crafted/top-200.csv')

with open(f'{adress}/files/dont_touch/names') as f:
    tmp = f.readlines()
names = np.array([x.strip() for x in tmp])
with open(f'{adress}/files/dont_touch/surnames') as f:
    tmp = f.readlines()
surnames = np.array([x.strip() for x in tmp])

db_size = args.size
db = pd.DataFrame(np.empty(db_size), columns=('hash',))

db_names = np.random.choice(names, db_size)
db['names'] = db_names

if args.verbose:
    print('1/5 names are ready!')

db_surnames = np.random.choice(surnames, db_size)
db['surnames'] = db_surnames

if args.verbose:
    print('2/5 surnames are ready!')

top_200_len = int(db_size*(0.3+np.random.random(1)*0.4))

top_200_indexes = np.random.choice(np.arange(db_size), top_200_len,
                                   replace=False)


top_200_passwords = np.array(top_200['password'])
top_200_frequencies = np.array(top_200['frequency']) / \
                      np.sum(top_200['frequency'])


def bad_passwords(indexes):
    return np.array([sha(f'id{indexes[i]}+',
                    np.random.choice(top_200_passwords, p=top_200_frequencies))
                    for i in range(len(indexes))])


db.loc[top_200_indexes, 'hash'] = bad_passwords(top_200_indexes)

if args.verbose:
    print('3/5 top_200 hashes are ready!')

noise_indexes = np.setdiff1d(np.arange(db_size), top_200_indexes)


def good_passwords(indexes):
    ALPHABET = np.array(list(string.ascii_letters +
                             string.digits +
                             string.punctuation))
    return np.array([sha(f'id{indexes[i]}+', ''.join(np.random.choice(
                    ALPHABET, size=np.random.randint(low=6, high=12))))
                    for i in range(len(indexes))])


db.loc[noise_indexes, 'hash'] = good_passwords(noise_indexes)

if args.verbose:
    print('4/5 noise hashes are ready! db is ready!')

db.to_csv(f"{adress}/files/crafted/{db_type}_db_{db_size}.csv",
          index=True)

if args.verbose:
    print('5/5 converting to csv is ready!')

if args.verbose:
    print(f"--- {(time.time() - start_time)} seconds ---")
