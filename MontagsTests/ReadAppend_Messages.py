from nacl.public import Box


def append_messages(message, box, file="Messages.txt"):
    print(file)

    encrypted_message = box.encrypt(message)

    with open(file, "a") as f:
        f.write(encrypted_message)
        f.write("\n")



def read_messages(box, file="Messages.txt"):
    print(file)




    with open(file, "r" ) as f:
        line = f.readline()
        while line:
                line = f.readline()
                try:
                    box.decrypt(line)
                except:
                    pass




