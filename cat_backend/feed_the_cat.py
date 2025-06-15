import socket
import json
from atomicwrites import atomic_write

UDP_IP = "0.0.0.0"
UDP_RECIEVER_PORT = 5174
UDP_SENDER_PORT = 7071

BUFF_SIZE = 1024

REPLY = ''
prefered_food = ['Fish', 'Meat', 'Flash', 'Coffee', 'Donut']

feeding_stat = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_RECIEVER_PORT))

try:
    msg = ''
    while True:
        data, addr = sock.recvfrom(BUFF_SIZE)
        print("received message: %s" % data)
        UDP_IP, UDP_SENDER_PORT = addr[0], addr[1]
        data = data.decode('utf-8')
        if data[-1] != '~':
            msg += data[:-2]
            part_received_msg = 'The Cat is amused by #%s' % data[-1]
            sock.sendto(bytes(part_received_msg, 'utf-8'), (UDP_IP, UDP_SENDER_PORT))
        else:
            msg = data if msg == '' else msg + data
            if msg.find(' ') != -1 and msg[msg.find(' ') + 1] == '-':
                username = msg[msg.find('@') + 1:msg.find(' ')]
            else:
                username = msg[msg.find('@') + 1:msg.find('-')]
            print(msg)
            if any([food in msg for food in prefered_food]):
                REPLY = b'Eaten by the cat'
                feeding_stat[username] = 1
            else:
                REPLY = b'Ignored by the cat'
                feeding_stat[username] = 0
            msg = ''
            print("FEEDING STATISTICS:")
            print(feeding_stat)
            with atomic_write("feed_stat.txt", overwrite=True) as f:
                f.write(json.dumps(feeding_stat))
            sock.sendto(REPLY, (UDP_IP, UDP_SENDER_PORT))
except KeyboardInterrupt:
    sock.close()