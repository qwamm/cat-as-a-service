import re
import socket
import textwrap
import dns.resolver

MESSAGE_REGEX = re.compile('(@[A-Za-z0-9]+~)+')

TCP_IP = "10.129.0.3"
TCP_RECEIVER_PORT = 0
TCP_SENDER_PORT = 8080

INPUT_BUFF_SIZE = 8


def split_str_by_usernames(s, BUFF_SIZE):
    if len(s) <= BUFF_SIZE:
        return [s]
    else:
        res = []
        split_list = s.split('~')
        print(split_list)
        for i in range(len(split_list)):
            if split_list[i] != '':
                if i == len(split_list) - 2:
                    split_list[i] = '~' + split_list[i] + '~'
                elif i > 0:
                    split_list[i] = '~' + split_list[i]
                res += textwrap.wrap(split_list[i], BUFF_SIZE)
        print(res)
        return res


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


srv_name = '_pet-the-cat._tcp.cat-service.org.'
ports = get_srv_port(srv_name)

if ports:
    print(f"Ports for {srv_name}: {ports}")
    TCP_RECEIVER_PORT = ports[0]
else:
    print(f"No SRV record found for {srv_name}")
    raise Exception('Can\'t get SRV record with service port number')


while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TCP_IP, TCP_RECEIVER_PORT))
        print(f'Connected to {TCP_IP}:{TCP_RECEIVER_PORT}')
        while True:
            MESSAGE = input('Enter nicknames of users, who want to pet the cat, in one raw and without spaces: ')
            if not MESSAGE_REGEX.match(MESSAGE) or MESSAGE[-1] != '~':
                print('Invalid message. Please, try again.')
                continue
            data = ''
            if len(MESSAGE) > INPUT_BUFF_SIZE:
                split_list = split_str_by_usernames(MESSAGE, INPUT_BUFF_SIZE)
                for part in split_list:
                    part = bytes(part, 'utf-8')
                    s.sendall(part)
                data = s.recv(1024).decode("utf-8")
                print('Received:', data)
            else:
                MESSAGE = bytes(MESSAGE, 'utf-8')
                s.sendall(MESSAGE)
                data = s.recv(1024).decode("utf-8")
                print('Received:', data)
            if data == 'The cat got tired of you and ran away.':
                break