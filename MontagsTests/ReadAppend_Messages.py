from nacl.public import Box
import nacl.encoding


def append_messages(message, box, file="Messages.txt"):
    encrypted_message = box.encrypt(bytes(message, 'utf-8'), encoder=nacl.encoding.Base64Encoder)

    with open(file, "a") as f:
        f.write(str(nacl.encoding.Base64Encoder.encode(encrypted_message), 'utf-8'))
        f.write("\n")


def read_messages(box, file="Messages.txt"):
    print(box)
    print(file)
    with open(file, "r") as f:
        while True:
            line = f.readline()
            print(line)
            if line is None:
                print("All Messages read")
                break
            print(box.decrypt(line, encoder=nacl.encoding.Base64Encoder))
            try:
                print(box.decrypt(line, encoder=nacl.encoding.Base64Encoder))
            except:
                print("pass")
