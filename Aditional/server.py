import socket

host=''
port = 5560

storedValue = "Yo, what's up?"

def setupServer():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Socket created.")

	try:	
		s.bind((host, port))
	except socket.error as msg:
		print(msg)
	print("Socked bind complete.")
	
	return  s 


def setupConnection():
	s.listen(1) # Allows one connection at a time.
	conn, address = s.accept()
	print("Connected to: " + address[0] + ":" + str(address[1]))
	return conn

def GET():
        reply = storedValue
        return reply

def REPEAT(dataMessage):
        reply = dataMessage[1]
        return reply


s = setupServer()

while True:
	try: 
		conn = setupConnection()
		dataTransfer(conn)
	except:	
		break


def dataTransfer(conn):
	# a big loop that 
	while True:
		data = conn.recv(1024)
		data = data.decode('utf-8')
		dataMessage = data.split(" ", 1)
		command = dataMessage[0]
		if command == "GET":			reply = GET()
		elif command == "REPEAT":
			reply = REPEAT(dataMessage)
		elif command == "EXIT":
			print("Our client has left us:( ")
			break
		elif command == "KILL":
			print("Our server is shutting down.")
			s.close()
			break
		else:
			reply = "Unknown command"

		conn.sendall(str.encode(reply))
		print("Data has ben sent!")
	conn.close()

