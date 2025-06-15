import random
import re
import socket
import json
from atomicwrites import atomic_write
import threading

TCP_IP = "0.0.0.0"
TCP_RECEIVER_PORT = 5175
BUFF_SIZE = 1024

feed_statistics = {}
pet_statistics = {}

def handle_client(conn, addr):
    print('Connected by', addr)
    msg = ''
    cat_ran_away = False
    with conn:
        while True:
            cat_reactions = ''
            data = conn.recv(BUFF_SIZE)
            if not data:
                break
            data = data.decode('utf-8')
            msg += data
            print(data)
            if len(msg) == 0:
                break
            if msg[-1] != '~':
                continue

            with threading.Lock():
                with open("feed_stat.txt", "r") as f:
                    feed_statistics = json.load(f)

                usernames = re.split('@|~', msg[1:-1])
                for username in usernames:
                    if username != '':
                        if username in pet_statistics and pet_statistics[username] >= 3:
                            cat_reactions = "The cat got tired of you and ran away."
                            pet_statistics[username] = pet_statistics[username] - random.randrange(0, pet_statistics[username])
                            cat_ran_away = True
                            break
                        elif username in feed_statistics and feed_statistics[username]:
                            cat_reactions += 'Tolerated by the cat'
                            pet_statistics[username] = pet_statistics[username] + 1 if username in pet_statistics else 1
                        else:
                            cat_reactions += 'Scratched by the cat'
                            pet_statistics[username] = pet_statistics[username] if username in pet_statistics else 0

                with atomic_write("pet_stat.txt", overwrite=True) as f:
                    f.write(json.dumps(pet_statistics))

            print("Cat reactions:", cat_reactions)
            conn.sendall(cat_reactions.encode('utf-8'))
            if cat_ran_away:
                break
            msg = ''

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((TCP_IP, TCP_RECEIVER_PORT))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.daemon = True
        client_thread.start()