#!/usr/bin/env python3

# Sneakernet/read-log.py

import binascii
import json
import logging
import os
import pprint
import sys

import lib.gg     as gg
import lib.pcap   as log
import lib.crypto as crypto

LOG_FILE_NAME = 'log.pcap'

# ----------------------------------------------------------------------

if __name__ == '__main__':

    log_fn = LOG_FILE_NAME
    if len(sys.argv) > 1:
        log_fn = sys.argv[1]

    print("Welcome to SneakerNet\n")
    print(f"** dumping log '{log_fn}', only showing body of events" + '\n')
    pp = pprint.PrettyPrinter(indent=2)

    lg = log.PCAP()
    lg.open(log_fn, 'r')
    n = 1
    t = gg.TRANSFER()
    for block in lg:
        t.from_cbor(block)
        c = t.event.content
        if c != None:
            print(f"** {n}:")
            # print(str(c, 'utf8'))
            m = json.loads(c)
            pp.pprint(m)
            # print(m)
            print()
        else:
            print(f"** {n}: no content")
        n += 1
    lg.close()

# eof
