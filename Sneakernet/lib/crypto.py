# sn/lib/crypto.py

import nacl.encoding
import nacl.exceptions
import nacl.signing


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

    @staticmethod
    def validate(public, blob, signature):
        """
        :param public: public Key as Hex
        :param blob: Binary Large Object
        :param signature: The signature of the blob to verify against. If the value of blob is the concated signature and blob, this parameter can be None.
        :return: True when the Blob is sucessfully verified
        """

        verify_key = nacl.signing.VerifyKey(public,
                                            encoder=nacl.encoding.HexEncoder)
        try:
            verify_key.verify(blob, signature)
        except nacl.exceptions.BadSignatureError:
            return False
        else:
            return True
