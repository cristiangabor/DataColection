import socket
import sys
from _thread import *

# 1.Gets the local ip/ip over LAN.
HOST =socket.gethostbyname(socket.gethostname())
# 2.Use port no. above 1800 so it does not interfere with ports already in use.
PORT =input ("Enter the PORT number (1 - 10,000)")
BUFFER_SIZE = 1024

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print(str(msg))

s.listen(100)
print("Waiting for a connection....")

def threded_clinet(conn):
    conn.send(str.encode("Welcome user!\n"))
    data = conn.recv(20)
    print(data)
    if data:
        reply = "Server output: Data was received by the server!"
        conn.sendall(str.encode(reply))
    else:
        reply = "Server output: Data was not received by the server!"
        conn.sendall(str.endcode(reply))
    conn.close()

while True:
    conn ,addr = s.accept()
    print("Connected to :" + addr[0] + ":" + str(addr[1]))

    #start_new_thread(threded_clinet, (conn,))
