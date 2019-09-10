# sn/lib/crypto.py

import nacl.signing
import nacl.encoding
import nacl.public

class ED25519:

    def __init__(self):
        self.seed = 0
        self.public = b'...'
        self.private = b'...'

    def create(self, seed):
        self.private = nacl.public.PrivateKey.generate()
        self.public = bytes(self.private.public_key)
        self.private = bytes(self.private)



    def sign(self, blob):
        # TODO: sign blob
        # TODO: return signed blob
        # blob = Binary Large OBject

        return b'\x00' * 32

    def validate(self, public, blob, signature):
        # TODO: compare signature/blob and public key to validate author

        return FaLSE

# eof

