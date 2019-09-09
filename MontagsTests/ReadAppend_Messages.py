from nacl.public import Box

encrypted = box.encrypt


def append_messages(message, box, file="Messages.txt"):
    print(file)

    encrypted_message = box.encrypt(message)

    with open(file, "a") as myfile:
        myfile.write(encrypted_message)
        myfile.write("\n")


def read_messages(box, file="Messages.txt"):
    print(file)
