#!/usr/bin/python
import sys
import socket
import psutil
import platform
from uptime import uptime
from simplecrypt import encrypt


def detect_uptime():
	""" Returns the uptime in seconds, or None if it can’t figure it out. """

	UPTIME = uptime()

	return(UPTIME)

def detect_platform():

	# DETECT PLATFORM
	current_platform = platform.system()
	if current_platform == "Windows":
		print("The current platform is:",current_platform, " ATENTION! There will be Windows security event logs")
		# The LOGS variable for windows will be implemented in the future
	else:
		print("The current platform is:",current_platform, " ATENTION! There will not be any Windows security event logs")
	return(True)


def get_cpu():
	# CPU usage
	"""Returns a list of floats representing the utilization as a percentage for each CPU. First element of the list refers to first CPU, second
	element to second CPU and so on. The order of the list is consistent across calls. """
	CPU_LIST=psutil.cpu_percent(interval=1, percpu=True)
	CPU=""
	for i in CPU_LIST:
		CPU += str(int(i)) + "/"
		CPU=str(CPU)
	return(CPU)

def get_memory_usage():
	mem = psutil.virtual_memory()
	MEMORY = { "MEMORY_USED": mem.used,"MEMORY_TOTAL" : mem.total, "MEMORY_AVAILABLE": mem.available, "MEMORY_FREE" : mem.free, "MEMORY_PERCENT":mem.percent}

	return(MEMORY)

def check_for_args(hostname):
	if len(sys.argv) < 3:
		print("Not enough arguments!")
		sys.exit()
	else:
		HOST_IP=str(sys.argv[1])
		PORT = int(sys.argv[2])
		print(hostname," ",HOST_IP,":",PORT)
		return(HOST_IP,PORT)

def transform_data(memory,cpu,uptime,logs=None):

	data_transformed = ''
	keys_list=memory.keys()
	length = len(memory)

	for i in keys_list:
		data_transformed += str(i) + " " + str(memory.get(i)) + " "

	data_transformed += " " + "CPU"

	for i in cpu:
		data_transformed += " " + str(i)

	data_transformed += " " + "UPTIME" + " " + str(uptime)

	if logs:
		data_transformed +=" " + "LOGS" + " "
		for i in logs:
			data_transformed += i + " "

	return(data_transformed)

def encrypt_data(password, message):

	ciphertext =encrypt(password, message)
	return(ciphertext)


def make_connection(client_socket,host, port):
	# Enstablish the connection to the central server

	client_socket.connect((host,port))

def send_encrypted_data(client_socket,data):


	client_socket.sendall(data)
	reply = client_socket.recv(1024)
	reply = reply.decode('utf-8')
	print(reply)
	return(reply)

def main(password):

	# GET CLIENT HOSTNAME
	HOSTNAME = socket.gethostname()

	# check if there are sufficient args*
	HOST_IP, PORT = check_for_args(HOSTNAME)

	# CLIENT SOCKET - OPEN
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Socket created...")

	# CPU
	CPU = get_cpu()

	# MEMORY
	MEMORY = get_memory_usage()

	# UPTIME
	UPTIME = detect_uptime()

	# LOGS
	LOGS = detect_platform()
	LOGS = str(LOGS)

	# PASSWORD
	PASSWORD = password

    # Tranform data
	data = transform_data(MEMORY, CPU, UPTIME, logs=LOGS)

	if data: # Check to see if the data exists
		make_connection(client_socket,HOST_IP,PORT)               # Enstablish the connection with the main server
		print("Encrypting data...")
		data_encrypted=encrypt_data(PASSWORD,data) 				  # Encrypt the data
		if data_encrypted:
			print("Sending data...")
			send_encrypted_data(client_socket,data_encrypted)  # Send the encrpyted data over TCP
		else:
			print("Data not sent!")
	else:
		print("There is no data!")



main('cris')
