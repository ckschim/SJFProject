import nacl.utils
import base64
import os.path
import base64
from nacl.public import PrivateKey
from nacl.encoding import Base64Encoder

if not os.path.exists("keys.txt"):
    secretkey = PrivateKey.generate()
    publickey = secretkey.public_key


    publickey64 = publickey.encode(Base64Encoder).decode("utf8")
    secretkey64 = secretkey.encode(Base64Encoder).decode("utf8")

    print(publickey64)
    print(secretkey64)

    with open("keys.txt", "w") as myfile:
        myfile.write(publickey64)
        myfile.write("\n")
        myfile.write(secretkey64)
else:
    with open("keys.txt", "r") as myfile:
        publickey64 = myfile.readline()
        secretkey64 = myfile.readline()

    print(publickey64)
    print(secretkey64)

    publickey = base64.b64decode(publickey64.encode("utf8"))
    secretkey = base64.b64decode(secretkey64.encode("utf8"))

    print(publickey, secretkey)


