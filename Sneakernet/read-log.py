#!/usr/bin/env python3

# Sneakernet/read-log.py

import binascii
import json
import logging
import os

import lib.gg     as event
import lib.pcap   as log
import lib.crypto as crypto

LOG_FILE_NAME = 'log.pcap'

# ----------------------------------------------------------------------

if __name__ == '__main__':

    print("Welcome to SneakerNet\n")
    print(f"reading out log '{LOG_FILE_NAME}'" + '\n')

    lg = log.PCAP()
    lg.open(LOG_FILE_NAME, 'r')
    n = 1
    while True:
        block = lg.read()
        if block == None:
            break
        # print(f"pcap block {n}:\n", block, '\n')
        t = event.TRANSFER()
        t.from_cbor(block)
        c = t.event.content
        if c != None:
            print(f"** {n}:")
            # print(str(c, 'utf8'))
            m = json.loads(c)
            print(m)
            print()
        else:
            print(f"** {n}: no content")
        n += 1
    lg.close()

# eof
