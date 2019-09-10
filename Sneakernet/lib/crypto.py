# sn/lib/crypto.py

import nacl.signing
import nacl.encoding

class ED25519:

    def __init__(self):
        self.seed = 0
        self.public = b'...'
        self.private = b'...'

    def create(self, seed):
        self.private = bytes(PrivateKey.generate())
        self.public = bytes(self.private.public_key)



    def sign(self, blob, signing_key):
        signing_key = nacl.signing.SigningKey(self.private, encoder=nacl.encoding.HexEncoder)
        # TODO: sign blob
        signed = signing_key.sign(blob)
        # TODO: return signed blob
        return signed
        # blob = Binary Large OBject


    def validate(self, public, blob, signature):
        # TODO: compare signature/blob and public key to validate author

        return FaLSE

# eof

