import re
import socket
import textwrap

import dns.resolver

MESSAGE_REGEX = re.compile('@[A-Za-z0-9]+ - [A-Za-z0-9]+~')

UDP_IP = '10.129.0.3'
UDP_SENDER_PORT = 7071
UDP_RECEIVER_PORT = 0

INPUT_BUFF_SIZE = 8


def get_srv_port(srv_name):
    try:
        answers = dns.resolver.resolve(srv_name, 'SRV')
        ports = [record.port for record in answers]
        return ports
    except dns.resolver.NoAnswer:
        return None
    except dns.resolver.NXDOMAIN:
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


srv_name = '_feed-the-cat._udp.cat-service.org.'
ports = get_srv_port(srv_name)

if ports:
    print(f"Ports for {srv_name}: {ports}")
    UDP_RECEIVER_PORT = ports[0]
else:
    print(f"No SRV record found for {srv_name}")
    raise Exception('Can\'t get SRV record with service port number')

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    while True:
        MESSAGE = input('Enter the message in format \"@Name - Food~\": ')
        if not MESSAGE_REGEX.match(MESSAGE) or MESSAGE[-1] != '~':
            print('Invalid message. Please, try again.')
            continue
        if len(MESSAGE) > INPUT_BUFF_SIZE:
            split_list = textwrap.wrap(MESSAGE, INPUT_BUFF_SIZE)
            split_list = [split_list[i] + '~' + str(i + 1) if i != len(split_list) - 1 else split_list[i] for i in
                          range(len(split_list))]
            for part in split_list:
                print(part)
                part = bytes(part, 'utf-8')
                sock.sendto(part, (UDP_IP, UDP_RECEIVER_PORT))
                data, addr = sock.recvfrom(1024)
                print("cat answer: %s" % data)
        else:
            MESSAGE = bytes(MESSAGE, 'utf-8')
            sock.sendto(MESSAGE, (UDP_IP, UDP_RECEIVER_PORT))
            data, addr = sock.recvfrom(1024)
            print("cat answer: %s" % data)
except KeyboardInterrupt:
    sock.close()
