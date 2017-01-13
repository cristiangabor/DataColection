import sys, os
import xml.etree.ElementTree as ET # API for xml parsing
import pysftp # this is API for ssh connection
import paramiko # API for remote script execution
from subprocess import call  # for executing the python client script


filename="data.xml"
pathname = os.path.dirname(sys.argv[0])
full_pathname=os.path.abspath(pathname)
ssh = paramiko.SSHClient()


try:
    send_script=os.path.join(full_pathname,"Send")
except Exception:
    print("Somenting went wrong with the script that will be sent!")

tree = ET.parse('data.xml')
root = tree.getroot()

number_of_clients=len(root)
print("The number of total clients are:", number_of_clients)
counter=1

for child in root:
    print("Client number {0}:".format(counter))
    child_attributes=child.attrib

    # Check for errors in the xml

    if "usernme" in child_attributes and "ip" in child_attributes and "port" in child_attributes and "password" in child_attributes and "mail"  in child_attributes:
        user_name=child_attributes.get("username")
        ip=child_attributes.get("ip")
        port=child_attributes.get("port")
        password=child_attributes.get("password")
        user_mail=child_attributes.get("mail")
        number_of_alerts=len(child)


        # Connect to the client through ssh

        cinfo = {'host':ip, 'username':user_name, 'password':password, 'port':int(port) }
        try:
            print("TEST")
            with pysftp.Connection(**cinfo) as sftp:
                print("TEST")
                # Check to see if there is a temp directory already

                main_directory=sftp.listdir()
                if not "temp" in main_directory:
                    sftp.mkdir('temp', mode=777) # Create directory
                    print("TEST")
                    sftp.put_r(send_script,'temp', preserve_mtime=True) # Copy the script

                else:
                    sftp.put_r(send_script,'temp', preserve_mtime=True) # Copy the script

            try: # Execute the script with paramiko
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, username=user_name, password=password)
                command="python temp/monitor.py " + HOST + " " + PORT
                print("Executing the external script.........\")
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("temp/monitor.py",get_pty=True)

            except Exception:
                print("Could not execute the script")

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
            print("ERROR!.Could not connect to host. Bad credentials!")


    else:
        print("One of the attributes is missing!")

    counter +=1



#for i in
