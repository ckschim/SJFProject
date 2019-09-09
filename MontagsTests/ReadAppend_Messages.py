from nacl.public import Box


def append_messages(message, box, file="Messages.txt"):
    print(file)

    encrypted_message = box.encrypt(bytes(message, 'utf-8'))

    with open(file, "a") as f:
        f.write(encrypted_message)
        f.write("\n")


def read_messages(box, file="Messages.txt"):
    print(file)




with open(filepath) as fp:
   line = fp.readline()
   while line:
       line = fp.readline()