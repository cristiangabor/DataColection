#!/usr/bin/python
import socket
import sys, os
from _thread import *
import xml.etree.ElementTree as ET # API for xml parsing
from simplecrypt import decrypt
import xml.etree.ElementTree as ET
import pysftp # this is API for ssh connection
import paramiko # API for remote script execution
from subprocess import call  # for executing the python client script



def decrypt_data(data, addr):
    f = open("mydata.txt",'a+')
    if data:
        print("Decrypting the information")
        decrypted_data = decrypt('cris', data).decode('utf-8')
        print(decrypted_data)
        CLIENT_IP,CLIENT_PORT=addr[0],addr[1]
        aditional_info="\n" +"CLIENT_IP: " + str(CLIENT_IP) + " " + "CLIENT_PORT: " + str(CLIENT_PORT) + " "
        aditional_info +=str(decrypted_data)
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


def parsing( HOST, PORT):
    filename="data.xml"

    pathname = os.path.dirname(sys.argv[0])
    full_pathname=os.path.abspath(pathname)
    ssh = paramiko.SSHClient()

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
            print(user_name,ip,port,password,user_mail)
            number_of_alerts=len(child)

            # Connect to the client through ssh

            cinfo = {'host':ip, 'username':user_name, 'password':password, 'port':int(port) } # dict configuration for pyftp

            try:
                with pysftp.Connection(**cinfo) as sftp:

                    # Check to see if there is a temp directory already

                    main_directory=sftp.listdir()
                    if not "temp" in main_directory:
                        sftp.mkdir('temp', mode=777) # Create directory
                        sftp.put_r(send_script,'temp', preserve_mtime=True) # Copy the script
                    else:
                        sftp.put_r(send_script,'temp', preserve_mtime=True) # Copy the script

                try: # Execute the script with paramiko
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(ip, username=user_name, password=password)
                    command="python temp/monitor.py" + " " + HOST + " " + PORT
                    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command, get_pty=True)
                except Exception:
                    print("Could not execute the script")

                # CHECK IF THERE ARE ALERTS
                if number_of_alerts > 0:

                    print("There are {0} alerts!".format(number_of_alerts))
                    for second_child in child:
                        second_child_attrib=second_child.attrib
                        check_type=second_child_attrib.get("type")
                        if check_type=="memory":
                            memory_limit=second_child_attrib.get("limit")
                            print("The memory limit is:",memory_limit)
                        elif check_type=="cpu":
                            cpu_limit=second_child_attrib.get("limit")
                            print("The cpu limit is:",cpu_limit)
                        else:
                            print("There are no tests to be done!")
                else:
                    print("There are no alerts to take into consideration!")

            except Exception:
                print("ERROR! Could not connect to host. Bad credentials!")

        else:
            print("One of the attributes is missing!")

        counter +=1


def main():


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

    start_new_thread(parsing, (HOST, PORT,))
    while True:
        conn ,addr = s.accept()
        print("Connected to :"+  addr[0] + ":" + str(addr[1]))

        start_new_thread(threded_clinet, (conn,addr,))

main()
