import re
import socket
import textwrap

MESSAGE_REGEX = re.compile('@[A-Za-z0-9]+ - [A-Za-z0-9]+~')

UDP_IP = '127.0.0.1'
UDP_SENDER_PORT = 7070
UDP_REVEIVER_PORT = 5174

BUFF_SIZE = 8

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_SENDER_PORT))

try:
    while True:
        MESSAGE = input('Enter the message in format \"@Name - Food~\": ')
        if not MESSAGE_REGEX.match(MESSAGE):
            print('Invalid message. Please, try again.')
            continue
        if len(MESSAGE) > BUFF_SIZE:
            split_list = textwrap.wrap(MESSAGE, BUFF_SIZE)
            split_list = [split_list[i] + '~' + str(i + 1) if i != len(split_list) - 1 else split_list[i] for i in
                          range(len(split_list))]
            for part in split_list:
                print(part)
                part = bytes(part, 'utf-8')
                sock.sendto(part, (UDP_IP, UDP_REVEIVER_PORT))
                data, addr = sock.recvfrom(1024)
                print("cat answer: %s" % data)
        else:
            MESSAGE = bytes(MESSAGE, 'utf-8')
            sock.sendto(MESSAGE, (UDP_IP, UDP_REVEIVER_PORT))
            data, addr = sock.recvfrom(BUFF_SIZE)
            print("cat answer: %s" % data)
except KeyboardInterrupt:
    sock.close()