import time
import os
import pandas as pd
from modules import sha_256
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--salted", action="store_true",
                    help="salt passwords")
parser.add_argument("size", type=int, help="size of ur db")
args = parser.parse_args()

adress = os.path.dirname(__file__)
start_time = time.time()

db_size = args.size
if args.salted:
    db_type = 'salted'
else:
    db_type = 'unsalt'
data = pd.read_csv(f'{adress}/files/crafted/{db_type}_db_{db_size}.csv',
                   index_col=0, usecols=[0, 1])

toshow = data.hash.value_counts()

print(toshow[:10])

# if not args.salted:
#     top_1 = toshow[:1].index[0]
#
#     top_200_1 = hex(sha_256.sha_256_text('12345').arg)
#
#     print(f'top-1 from  bd : {top_1}')
#     print(f'top-1 from song: {top_200_1}')
#
#     print('PWNED! Password is "12345"' * (top_1 == top_200_1) +
#           'nice try, bad luck' * ((top_1 != top_200_1)))
#
#     print(f"--- {(time.time() - start_time)} seconds ---")
