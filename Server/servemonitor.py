import socket
import sys
from _thread import *
from simplecrypt import decrypt

# 1.Gets the local ip/ip over LAN.

HOST =socket.gethostbyname(socket.gethostname())

# 2.Use port no. above 1800 so it does not interfere with ports already in use.

PORT =input ("Enter the PORT number (1 - 10,000)")


s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((HOST, int(PORT)))
except socket.error as msg:
    print(str(msg))

s.listen(100)
print("Waiting for a connection....")

def decrypt_data(data):
    f = open("mydata.txt",'w')
    if data:
	    print("Decrypting the information")
	    decrypted_data = decrypt('cristian', data).decode('utf-8')
        print(decrypted_data)
        f.write(decrypted_data)
        f.close()
        return(decrypted_data)
    else:
	    print("There is no data to decrypt")



def threded_clinet(conn):
    conn.send(str.encode("Data received by the server!\n"))
    data = conn.recv(1024)

    start_new_thread(decrypted_data, (data,))
    if data:
        reply = "Server output: Data was received by the server!"
        conn.sendall(str.encode(reply))
    else:
        reply = "Server output: Data was not received by the server!"
        conn.sendall(str.endcode(reply))
    conn.close()

while True:
    conn ,addr = s.accept()
    print("Connected to :"+  addr[0] + ":" + str(addr[1]))

    start_new_thread(threded_clinet, (conn,))
