import time
import os
import numpy as np
import pandas as pd
from modules import sha_256
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("size", type=int, help="size of ur db")
parser.add_argument("-s", "--salted", action="store_true",
                    help="salt passwords")
args = parser.parse_args()


adress = os.path.dirname(__file__)
start_time = time.time()

db_size = args.size
if args.salted:
    db_type = 'salted'
else:
    db_type = 'unsalt'
data = pd.read_csv(f'{adress}/files/crafted/{db_type}_db_hacked_{db_size}.csv',
                   index_col=0)

non_nan = data.count()

print(f"hacked {non_nan['password']}/{non_nan['hash']} password. \
it's {round(non_nan['password']/non_nan['hash'], 3)} of total number")

print(f"--- {(time.time() - start_time)} seconds ---")
