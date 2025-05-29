import re
import socket
import json

TCP_IP = "127.0.0.1"
TCP_RECIEIVER_PORT = 5175
TCP_SENDER_PORT = 8080

BUFF_SIZE = 1024

usernames_dict= {}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((TCP_IP, TCP_RECIEIVER_PORT))
    s.listen(1)
    while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                msg = ''
                cat_reactions = ''
                data = conn.recv(BUFF_SIZE)
                data = data.decode('utf-8')
                msg += data
                print(msg)
                print(len(msg))
                if len(msg) == 0 or msg[-1] != '~':
                    continue
                with open("feed_stat.txt", "r") as f:
                    usernames_dict = json.load(f)
                usernames = re.split('@|~', msg[1:-1])
                for username in usernames:
                    if username != '':
                        if username in usernames_dict and usernames_dict[username]:
                            cat_reactions += 'Tolerated by the cat'
                        else:
                            cat_reactions += 'Scratched by the cat'
                cat_reactions = bytes(cat_reactions, 'utf-8')
                conn.sendall(cat_reactions)
                msg = ''
                conn.close()
