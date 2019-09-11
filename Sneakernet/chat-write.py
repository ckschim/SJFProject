"""

message input                          | x
create event                           |
    create content json                | x
        add feed (public key)          | x
        add message                    | x
    add cool stuff                     |
append to log                          | x

"""

import users

# ------------------------------------------

if __name__ == '__main__':
    print("Welcome to SneakerNet\n")
    message = input("Please insert your message: ")
    body = {'app': 'feed/message',
             'feed': users.my_secret['public_key'],
             'text': message}
    users.my_log_append(users.MY_LOG_FILE, body)