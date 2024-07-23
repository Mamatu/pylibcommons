import logging
logging.basicConfig()
log = logging.getLogger(__name__)

from pylibcommons import libprocess
import sys, os

import bson
from pathlib import Path

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--stderr", help = "", type = int, default = 0)
    parser.add_argument("--stdout", help = "", type = int, default = 0)
    args = parser.parse_args()
    for idx in range(args.stderr):
        log.error(f"stderr {idx}")
    for idx in range(args.stdout):
        log.info(f"stdout {idx}")

if __name__ == "__main__":
    main()
