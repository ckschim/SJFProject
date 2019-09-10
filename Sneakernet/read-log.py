import lib.pcap as log
import lib.gg as event
import json
import nacl.public
import nacl.encoding
import glob

if __name__ == '__main__':

    for file in glob.glob("*.pcap"):
        lg = log.PCAP()
        lg.open(file, 'r')
        n = 0
        while True:
            block = lg.read()
            if block is None:
                break
            t = event.TRANSFER()
            t.from_cbor(block)

            feed = nacl.public.PublicKey(t.event.feed).encode(nacl.encoding.Base64Encoder).decode("utf-8")

            print(feed + " : " + json.loads(t.event.content.decode('utf-8'))['message'])
            n += 1
        lg.close()




