from nacl.public import Box
import nacl.encoding


def append_messages(message, box, file="Messages.txt"):
    encrypted_message = box.encrypt(bytes(message, 'utf-8'), encoder=nacl.encoding.Base64Encoder)

    with open(file, "a") as f:
        f.write("%s" % encrypted_message)
        f.write("\n")


def read_messages(box, file="Messages.txt"):
    with open(file, "r") as f:
        line = f.readline()
        while line:
            line = f.readline()
            try:
                print(box.decrypt(line))
            except:
                pass
