"""
write the log
    #create identity                        | True
    #input loop (interruptable)             |
        #create event                       |
            #seq counter +1                 |
            #timestamp                      |
            #content                        |
            #feed (public_key)              |
            #previous (previous hash)
            #signature
        #save to pcap
    #finisch
"""

import lib.crypto as crypto
import lib.gg as gg
import time
import lib.pcap as log


def create_event(content, seq, prev, public_key):
    return gg.EVENT(
        prev=prev,
        feed=public_key,
        seq=seq,
        time=time.time(),
        content=bytes("{\n \"message\": \"%s\"\n}\n" % content, 'utf-8'),
        content_enc=gg.GG_CONTENT_ENCODING_JSON
    )


if __name__ == '__main__':
    keypair = crypto.ED25519()
    keypair.create()
    seq = 0
    prev = None
    lg = log.PCAP()
    lg.open("log" + str(time.time()) + ".pcap", 'w')
    while True:
        content = input("Please type in your message: ")
        event = create_event(content, seq, prev, keypair.public)
        event.signature = keypair.sign(event.event_to_cbor())
        t = gg.TRANSFER(event)
        lg.write(t.to_cbor())
        print(event.pretty_print())
        seq += 1
        prev = event.get_sha256()
        loop = input("Do you want to write another message: (y/n) ")
        if loop == "n":
            break

    lg.close()