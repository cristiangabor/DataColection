#!/usr/bin/python

import sys
import psutil
import platform
from uptime import uptime
from simplecrypt import encrypt


# PASSWORD

PASSWORD = "cristian"

# for ip purpouse
print("Number of arguments:", len(sys.argv), "arguments.")
print("Argument List:", str(sys.argv))

# Memory usage

mem = psutil.virtual_memory()

MEMORY = { "MEMORY_USED": mem.used,"MEMORY_TOTAL" : mem.total, "MEMORY_AVAILABLE": mem.available, "MEMORY_FREE" : mem.free, "MEMORY_PERCENT":
mem.percent }



# CPU usage
"""Returns a list of floats representing the utilization as a percentage for each CPU. First element of the list refers to first CPU, second
element to second CPU and so on. The order of the list is consistent across calls. """

CPU=psutil.cpu_percent(interval=1, percpu=True)


# UPTIME
""" Returns the uptime in seconds, or None if it can’t figure it out. """

UPTIME = uptime()


# DETECT PLATFORM

current_platform = platform.system()

LOGS = None

if current_platform == "Windows":
	print("The current platform is:",current_platform, " ATENTION! There will be Windows security event logs")
	# The LOGS variable for windows will be implemented in the future
else:
	print("The current platform is:",current_platform, " ATENTION! There will not be any Windows security event logs")


def transform_data(memory,cpu,uptime,logs=None):
	encrypted_text = ''
	keys_list=memory.keys()
	length = len(memory)


	for i in keys_list:
		encrypted_text += str(i) + " " + str(memory.get(i)) + " "


	encrypted_text += " " + "CPU"

	for i in cpu:
		encrypted_text += " " + str(i)

	encrypted_text += " " + "UPTIME" + " " + str(UPTIME)

	if logs:
		encrypted_text +=" " + "LOGS" + " "
		for i in logs:
			encrypted_text += i + " "

	return(encrypted_text)

def encrypt_data(password, message):

	ciphertext =encrypt(password, message)

	print("SUCCES!")
	return(ciphertext)


MESSAGE=transform_data(MEMORY, CPU, UPTIME, logs=LOGS)
encrypt_data(PASSWORD,MESSAGE)
