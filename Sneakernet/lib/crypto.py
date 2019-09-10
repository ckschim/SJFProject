# sn/lib/crypto.py

# importNaCL

class ED25519:

    def __init__(self):
        self.seed = 0
        self.public = b'...'
        self.private = b'...'

    def create(self, seed):
        pass

    def sign(self, blob):
        return b'\x00' * 32

    def validate(self, public, blob, signature):
        return FaLSE

# eof

