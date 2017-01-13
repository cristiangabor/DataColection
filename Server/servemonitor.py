#!/usr/bin/python
import socket
import sqlite3
import sys, os
import getpass # for the password input
import smtplib # For email
from _thread import *
import xml.etree.ElementTree as ET # API for xml parsing
from simplecrypt import decrypt
import xml.etree.ElementTree as ET
import pysftp # this is API for ssh connection
from subprocess import call  # for executing the python client script


# CREATE THE DATABASE

def create_table(db_name,table_name,sql):
	with sqlite3.connect(db_name) as db:
		cursor=db.cursor()
		cursor.execute('PRAGMA foreign_keys=ON')
		cursor.execute("select name from sqlite_master where name=?",(table_name,))
		result=cursor.fetchall()
		kepp_table=True
		if len(result) == 1:
			response = input("The table {0} alerady exists, do yoy wish to recreate it (y/n):".format(table_name))
			if response== "y":
				kepp_table=False
				print('The {0} table will be recreated- all existing data will be lost'.format(table_name))
				cursor.execute('drop table if exists {0}'.format(table_name))
				db.commit()
			else:
				print("The existing table was kept")
		else:
			kepp_table=False
		if not kepp_table:
			cursor.execute(sql)
			db.commit()


# CREATE DATABASE - BUILD THE COLLONS

def create_table_for_doc(db_name):

	sql="""CREATE TABLE IF NOT exists INFORMATION(
			ID INTEGER,
			CLIENT_IP text,
			CLIENT_PORT text,
			MEMORY_FREE text,
			MEMORY_PERCENT text,
			MEMORY_AVAILABLE text,
			MEMORY_TOTAL text,
			MEMORY_USED text,
			CPU text,
			UPTIME text,
			primary key(ID))"""

	create_table(db_name,'INFORMATION',sql)

# CREATE DATABASE - POPULATE THE DATABASE

def insert_text(CLIENT_IP, CLIENT_PORT, MEMORY_FREE, MEMORY_PERCENT, MEMORY_AVAILABLE, MEMORY_TOTAL,MEMORY_USED,CPU,UPTIME):

		with sqlite3.connect('poze.db') as db:
			cursor=db.cursor()
			data=(popular.title(),stiintific,importanta,descriere,sqlite3.Binary(poza))
			sql="INSERT INTO INFORMATION(Popular,Stiintific,Importanta,Descriere,Poza) values (?,?,?,?,?)"
			cursor.execute(sql,data)
			db.commit()

# START THE DECRYPTION PROCESS

def decrypt_data(data, addr):

    f = open("mydata.txt",'a+')
    if data:
        print("Decrypting the information")
        decrypted_data = decrypt('cris', data).decode('utf-8')
        print(decrypted_data)
        CLIENT_IP,CLIENT_PORT=addr[0],addr[1]
        aditional_info="\n" +"CLIENT_IP: " + str(CLIENT_IP) + " " + "CLIENT_PORT: " + str(CLIENT_PORT) + " "
        aditional_info +=str(decrypted_data)
        aditional_info = aditional_info.split()
        for i in aditional_info:
            print(i)
        f.write(str(aditional_info))
        f.close()
        return(decrypted_data)
    else:
	    print("There is no data to decrypt")



def threded_clinet(conn, addr):
    conn.send(str.encode("Data received by the server!\n"))
    data = conn.recv(1024)

    start_new_thread(decrypt_data, (data,addr,))

    if data:
        reply = "Server output: Data was received by the server!"
        conn.sendall(str.encode(reply))
    else:
        reply = "Server output: Data was not received by the server!"
        conn.sendall(str.endcode(reply))
    conn.close()

# SENT MAIL TO THE SERVER OWNER

def send_email_function(fromaddr,memory_limit,cpu_limit, gmail_password):

    toaddrs = fromaddr

    # Gmail Login
    username = fromaddr
    msg = """
    This a automated email received from a script. The alert is:
    \n Memory limit: %s
    \n CPU limit: %s """ % (str(memory_limit),str(cpu_limit))

    # Sending the mail

    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(username,gmail_password)
        server.sendmail(fromaddr, toaddrs, msg, "")
        server.quit()
        print('successfully sent the mail')
    except:
        print("Failed to send mail. Check if the Gmail password is correct.")


# PARSE THE XML DATA

def parsing( HOST, PORT, GMAIL_PASSWORD):

    filename="data.xml"

    pathname = os.path.dirname(sys.argv[0])
    full_pathname=os.path.abspath(pathname)


    try:
        send_script=os.path.join(full_pathname,"Send")
    except Exception:
        print("Somenting went wrong with the script location!")

    tree = ET.parse('data.xml')   # PARSING
    root = tree.getroot()

    number_of_clients=len(root)
    print("The number of total clients are:", number_of_clients)
    counter=1

    # START THE XML ANALYZATION
    for child in root:
        print("Client number {0}:".format(counter))
        child_attributes=child.attrib

        # Check for errors in the xml

        if "username" in child_attributes and "ip" in child_attributes and "port" in child_attributes and "password" in child_attributes and "mail"  in child_attributes:
            user_name=child_attributes.get("username")
            ip=child_attributes.get("ip")
            port=child_attributes.get("port")
            password=child_attributes.get("password")
            user_mail=child_attributes.get("mail")
            number_of_alerts=len(child)

            # Connect to the client through ssh

            cinfo = {'host':ip, 'username':user_name, 'password':password, 'port':int(port) } # dict configuration for pyftp
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            try:

                with pysftp.Connection(**cinfo) as sftp:

                    # Check to see if there is a temp directory already

                    main_directory=sftp.listdir()
                    if not "temp" in main_directory:
                        sftp.mkdir('temp', mode=777) # Create directory
                        sftp.put_r(send_script,'temp', preserve_mtime=True) # Copy the script

                    else:
                        sftp.put_r(send_script,'temp', preserve_mtime=True) # Copy the script

                    with sftp.cd('temp'):    # CHANGE into temp directory
                        command = "./startscript.sh" + " " + HOST + " " + PORT
                        sftp.chmod('startscript.sh', 777)   # set privileges
                        #err=sftp.excute(command) # Execute the bash script

                # CHECK IF THERE ARE ALERTS
                if number_of_alerts > 0:

                    print("There are {0} alerts!".format(number_of_alerts))
                    for second_child in child:
                        second_child_attrib=second_child.attrib
                        check_type=second_child_attrib.get("type")
                        if check_type=="memory":
                            memory_limit=second_child_attrib.get("limit")
                        elif check_type=="cpu":
                            cpu_limit=second_child_attrib.get("limit")
                        else:
                            print("There are no tests to be done!")

                    # SEND MAIL

                    send_email_function(user_mail, memory_limit, cpu_limit, GMAIL_PASSWORD)
                else:
                    print("There are no alerts to take into consideration!")

            except Exception:
                print("ERROR! Could not connect to host. Bad credentials!")

        else:
            print("One of the attributes is missing!")

        counter +=1

# MAIN

def main():


    # 1.Gets the local ip/ip over LAN.

    #HOST =socket.gethostbyname(socket.gethostname())
    HOST="192.168.0.102"
    # 2.Use port no. above 1800 so it does not interfere with ports already in use.

    PORT =input ("Enter the PORT number (1 - 10,000)")

    #GMAIL_PASSWORD =input ("Enter your gmail password:")

    GMAIL_PASSWORD=getpass.getpass("Insert your gamil password: ")    #password input

    create="none"
    while create != "y" and create !="n":
        create = input("Do you want to create the database for the future data [y/n]:")
        if create == "y":
            create_table_for_doc('client_data.db')
        elif create =="n":
            print("ATTENTION! Program can not run without a database. ")


    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((HOST, int(PORT)))
    except socket.error as msg:
        print(str(msg))

    s.listen(100)
    print("Waiting for a connection....")

#    start_new_thread(parsing, (HOST, PORT,GMAIL_PASSWORD))

    while True:
        conn ,addr = s.accept()
        print("Connected to :"+  addr[0] + ":" + str(addr[1]))

        start_new_thread(threded_clinet, (conn,addr,))

main()
