import nacl.utils
from nacl.public import PrivateKey
from nacl.encoding import Base64Encoder

secretkey = PrivateKey.generate()
publickey = secretkey.public_key

print(publickey.encode(Base64Encoder).decode())
print(secretkey.encode(Base64Encoder).decode())

