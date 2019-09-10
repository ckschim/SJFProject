"""
write the log
    #create identity                        | True
    #input loop (interruptable)             |
        #create event                       |
            #seq counter +1                 |
            #timestamp                      |
            #content                        |
            #feed (public_key)
            #previous (previous hash)
            #signature
        #save to pcap
    #finisch
"""

import lib.crypto as crypto


def msg_input():

def create_event():

def save_pcap():


if __name__ == '__main__':
    keypair = crypto.ED25519()
    keypair.create()
    while True:
        content = input("msg: ")

