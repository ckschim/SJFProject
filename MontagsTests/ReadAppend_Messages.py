from nacl.public import Box


def append_messages(message, box, file="Messages.txt"):
    print(file)

    encrypted_message = box.encrypt(bytes(message, 'utf-8'))

    with open(file, "a") as f:
        f.write(encrypted_message.ciphertext.decode('utf-8'))
        f.write("\n")



def read_messages(box, file="Messages.txt"):
    print(file)

    box = Box(skalice, pkbob)
    plaintext = box.decrypt(encrypted)
    print(plaintext.decode('utf-8'))



