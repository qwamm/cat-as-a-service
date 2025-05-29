import re
import socket
import textwrap

MESSAGE_REGEX = re.compile('(@[A-Za-z0-9]+~)+')

TCP_IP = "127.0.0.1"
TCP_RECIEIVER_PORT = 5175
TCP_SENDER_PORT = 8080

BUFF_SIZE = 8

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((TCP_IP, TCP_RECIEIVER_PORT))
    while True:
        MESSAGE = input('Enter nicknames of users, who want to pet the cat, in one raw and without spaces: ')
        if not MESSAGE_REGEX.match(MESSAGE):
            print('Invalid message. Please, try again.')
            continue
        if len(MESSAGE) > BUFF_SIZE:
            split_list = textwrap.wrap(MESSAGE, BUFF_SIZE)
            for part in split_list:
                part = bytes(part, 'utf-8')
                s.sendall(part)
            data = s.recv(1024)
            print('Received', repr(data))
        else:
            MESSAGE = bytes(MESSAGE, 'utf-8')
            s.sendall(MESSAGE)
            data = s.recv(BUFF_SIZE)
            print('Received', repr(data))