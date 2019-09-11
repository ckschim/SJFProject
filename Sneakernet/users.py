#!/usr/bin/env python3

# Sneakernet/users.py

"""
  if no my_feed.json exists:
    create? n -> exit
    create
  if no log dir exists:
    create dir
  if no log file 0 exists:
    create pcap file
  read pcap file
  if unequal to feedID:
    abort

  if 'display_name' option:
    ask for name
    append about event
  else:
    loop over all logs
      scan log, record latest 'about'
      display feed and display_name
"""

import base64
import json
import os
import platform
import sys
import time

import lib.crypto as crypto
import lib.gg     as gg
import lib.pcap   as log

MY_SECRET_FILE = 'MyFeedID.json'
LOGS_DIR = 'logs'
MY_LOG_FILE = '1.pcap' # inside logs dir

# ----------------------------------------------------------------------

def my_log_append(log_fn, body):
    lg = log.PCAP()
    lg.open(log_fn, 'r')
    prev = None
    feed = None
    seq = 0
    t = gg.TRANSFER()
    # find last event
    for block in lg:
        t.from_cbor(block)
        prev = t.event.prev
        feed = t.event.feed
        seq = t.event.seq
    lg.close()

    lg.open(log_fn, 'a')
    e = gg.EVENT(
        prev=prev,
        feed=keypair.public,
        seq=seq+1,
        time=int(time.time()),
        content=bytes(json.dumps(body), 'utf-8'),
        content_enc=gg.GG_CONTENT_ENCODING_JSON
    )
    e.signature = keypair.sign(e.event_to_cbor())
    t = gg.TRANSFER(e)
    lg.write(t.to_cbor())
    lg.close()

def feed_get_display_name(log_fn):
    # returns a <feedID,display_name> tuple
    feed = None
    name = None
    lg = log.PCAP()
    lg.open(log_fn, 'r')
    t = gg.TRANSFER()
    for block in lg:
        t.from_cbor(block)
        if not feed:
            feed = t.event.feed
        c = t.event.content
        if not c:
            continue
        m = json.loads(c)
        if 'app' in m and m['app'] == 'feed/about' and 'display_name' in m:
            name = m['display_name']
    lg.close()
    return (feed,name)


def write_message():
    message = input("\nPlease insert your message: ")
    body = {"app": "feed/message",
            "feed": my_secret['public_key'],
            "text": message}
    print("\n** successfuly created body")
    my_log_append(os.path.join(LOGS_DIR, MY_LOG_FILE), body)
    print("** successfuly appended to", os.path.join(LOGS_DIR, MY_LOG_FILE),"\n")

def output_chat():
    t = gg.TRANSFER()
    lg = log.PCAP()
    for file in os.listdir(LOGS_DIR):
        lg.open(os.path.join(LOGS_DIR, file), "r")
        for block in lg:
            t.from_cbor(block)
            c = t.event.content
            if c != None:
                #print(f"** {base64.b64encode(t.event.feed).decode('utf8')}/{t.event.seq}")
                # print(str(c, 'utf8'))
                m = json.loads(c)
                if m['app'] == "feed/message":
                    print(m['text'])
                # print(m)
                print()
            else:
                print(f"** {n}: no content")
        lg.close()










# ----------------------------------------------------------------------
if __name__ == '__main__':

    if len(sys.argv) == 2:
        set_new_name = sys.argv[1] == '-new_name'
        message_mode = sys.argv[1] == '-new_message'
        output_mode = sys.argv[1] == '-output_chat'
    
    print("Welcome to SneakerNet\n")
    #print("** starting the user directory app")

    keypair = crypto.ED25519()
    if not os.path.isfile(MY_SECRET_FILE):
        yn = input('>> create personal feed ID? (y/N) ')
        if yn != 'y':
            print("** aborted")
            sys.exit()
        keypair.create()
        my_secret = {'public_key':
                       base64.b64encode(keypair.public).decode('utf8'),
                     'private_key':
                       base64.b64encode(keypair.private).decode('utf8'),
                     'create_context': platform.uname(),
                     'create_time': time.ctime()
        }
        with open(MY_SECRET_FILE, 'w') as f:
            f.write(json.dumps(my_secret, indent=2))
    else:
        with open(MY_SECRET_FILE, 'r') as f:
            my_secret = json.loads(f.read())
        keypair.public = base64.b64decode(my_secret['public_key'])
        keypair.private = base64.b64decode(my_secret['private_key'])
        # print(keypair.public, keypair.private)
        print(f"** loaded my feed ID: @{base64.b64encode(keypair.public).decode('utf8')}")

    if not os.path.isdir(LOGS_DIR):
        os.mkdir(LOGS_DIR)
        print(f"** created {LOGS_DIR} directory")

    log_fn = os.path.join(LOGS_DIR, MY_LOG_FILE)
    if not os.path.isfile(log_fn):
        lg = log.PCAP()
        lg.open(log_fn, 'w')
        lg.close()
        print(f"** created my log at {log_fn}")

    # find my name
    feed, name = feed_get_display_name(log_fn)
    if feed and feed != keypair.public:
        print(f"** {log_fn} does not match feed ID (MyFeedID.json), aborting")
        sys.exit()
    if set_new_name or not feed or not name:
        if not feed or not name:
            print("** no name for this feed found")
        name = input(">> enter a display name for yourself: ")
        about = { 'app' : 'feed/about',
                  'feed' : my_secret['public_key'],
                  'display_name' : name }
        my_log_append(log_fn, about)
        print(f"** defined display name '{name}'")
    else:
        print(f"** loaded my name: '{name}'")

    print("\n** list of known users:")
    feeds = {}
    for fn in os.listdir(LOGS_DIR):
        log_fn = os.path.join(LOGS_DIR, fn)
        feed, name = feed_get_display_name(log_fn)
        feeds[feed] = name
    for feed,name in sorted(feeds.items(), key=lambda x: x[1]): 
        print(f"- @{base64.b64encode(feed).decode('utf8')}   {name}")

    if message_mode:
        write_message()
    if output_mode:
        output_chat()

# eof
