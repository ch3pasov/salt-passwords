import time
import argparse
from modules import sha_256

parser = argparse.ArgumentParser()
parser.add_argument("text", type=str, help="text to hash")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
args = parser.parse_args()

if args.verbose:
    start_time = time.time()

print(hex(sha_256.sha_256_text(args.text).arg))

if args.verbose:
    print("--- %s seconds ---" % (time.time() - start_time))
