# sn/lib/crypto.py

# importNaCL

class ED25519:

    def __init__(self):
        self.seed = 0
        self.public = b'...'
        self.private = b'...'

    def create(self, seed):
        # TODO: generate keys (SigningKey, PublicKey)
        # signing key is kind of a PrivateKey

        pass

    def sign(self, blob):
        # TODO: sign blob
        # TODO: return signed blob
        # blob = Binary Large OBject

        return b'\x00' * 32

    def validate(self, public, blob, signature):
        # TODO: compare signature/blob and public key to validate author

        return FaLSE

# eof

