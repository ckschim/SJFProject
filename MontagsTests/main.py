import nacl.utils
import os.path
import MontagsTests.ReadAppend_Messages as ra
from nacl.public import PrivateKey
from nacl.public import Box
from nacl.encoding import Base64Encoder


def start():
    if not os.path.exists("keys.txt"):
        secretkey = PrivateKey.generate()
        publickey = secretkey.public_key

        publickey64 = publickey.encode(Base64Encoder).decode("utf8")
        secretkey64 = secretkey.encode(Base64Encoder).decode("utf8")

        with open("keys.txt", "w") as myfile:
            myfile.write(publickey64)
            myfile.write("\n")
            myfile.write(secretkey64)
    else:
        with open("keys.txt", "r") as myfile:
            publickey64 = myfile.readline()
            secretkey64 = myfile.readline()

        publickey = nacl.public.PublicKey(publickey64, nacl.encoding.Base64Encoder)
        secretkey = nacl.public.PrivateKey(secretkey64, nacl.encoding.Base64Encoder)
        print(secretkey)
    return secretkey


PrivateKey = start()
print(PrivateKey)
PublicKey = nacl.public.PublicKey(input("Please insert your friends public key: "), nacl.encoding.Base64Encoder)
box = Box(PrivateKey, PublicKey)
select = input("Press\n1 to read\n2 to append\n")
try:
    select = int(select)
except:
    select = input("Please try it again. Press\n1 to read\n2 to append\n")
if select == 1:
    print("Cool. We're looking for your messages.\n")
    ra.read_messages(box)
elif select == 2:
    message = input("Please insert a message: ")
    ra.append_messages(message, box)
