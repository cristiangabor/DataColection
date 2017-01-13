

1. Instructions to install and configure dependencies.

   To run the scripts - Use Python3

   Dependencies:

   To install the following dependencies - Use the PIP pakage installer

   FOR CLIENT:

   a) psutil [Description: psutil is a cross-platform library for retrieving information onrunning processes and system utilization.]

	To install : pip install psutil


   b) simple-crypt [Description: Simple Crypt encrypts and decrypts data. It has two functions, encrypt and decrypt. Is a wrapper of pycrypto.]
	
	To install : pip install simple-crypt


   FOR SERVER:

   a) simple-crypt [Description: Simple Crypt encrypts and decrypts data. It has two functions, encrypt and decrypt. Is a wrapper of pycrypto.]
	
	To install : pip install simple-crypt
   
   b) pysftp [Description: A simple interface to SFTP, used for ssh comunication. Is is based on paramiko]
	
	To install : pip install pysftp

2. Instructions to create and initialize the database. 

     The server script will automaticaly create the database if is not already created. Also the script will automatically insert the data received
   from the client and after that will decrypt it. After the decryption process is over the data will automatically inserted into the database.
   If something happens with the data integrity the server script will not include it and will show a message error.
 
3. Assumptions made.

      The client part was pretty clear. The script had to gather system information and send the information through a socket to server. 
    The connection had to be based on the server IP and PORT, so I wanted to design the client script to take 2 arguments when is executed from
    terminal. I was reading the pycrypto documentation and I had some problems when I tried to encrypt the data with AES, The password had byte 
    restriction. Luckily, I found the simple-crypt which, was doing the password conversion automatically and I did not had to worry about any other
    details. It was a decision based on the time I had to develop the future script. 
       For the server script I had to make it parse the xml and based on the ip and username to connect it to a client in the LAN. I wanted to make a 
    xml error check in case the ssh conncetion data was wrong. After the connection is enstablished I had a problem. I could not make the server       
    script to execute the client script. It was copying correctly the script, but when was executing it, I had no data comming. 
    After many, many attempts, I discovered that my linux had some internet connectivity problems. I think I made some changes to the firewall in my 
    previous hacks. Anyway, I checked the scripts on my laptop and rasberry and was connectiong, it was sending the client script to the raspberry, 
    but was not executing it. After I tought a bit I had the ideea to make a bash script to execute the client script. I thought that this will 
    eliminate any permission errors in linux to make it listen all the time for incomming connections.
       I decided to continue with the script developing even there was still a problem on the executing part. I assumed that the problem was on my
    system and will work on your system. So I made the server script to decrypt data recevied. From the string it had to find the key words
    (like: CLIENT_PORT:) and extract the value. I made pretty simple with a for loop. Next, I build the data integration into database and linked it
    with the data parse.
       In order to make the server script accept many connections, I made new threads for each connection. Also for decrypting part I integrated new
    threads. And for the email part it was simple, but I had some problems with sending the email from the Gmail client. 

4. Requirements that you have not covered in your submission. 

     I build the program on my linux system. I had no Windows computer so I did not implemented the windows event logs. I only made a system check, 
   to see what system is running. So the server will know.

5. Issue you have faced while completing the assignment.

     I encountered problems pretty much on every dependencies I installed with pip. Most of the problems were caused by my lack of experience with 
   the dependencies, but after some trial and error and a few hours, I succeded. 
     The big problem I am still having is with the ssh. I could not succeded to make the server script to execute the client script. I hope it is a 
    problem with my system and not with the script. 
     Second I encountered some problems on stmp part. Google e-mail client was not letting me to send the e-mail. After some research I found out 
    that I had to dezactivate their security check.  [ https://www.google.com/settings/security/lesssecureapps ]

6. Constructive feedback for improving the assignment. 
    
    The assignment was difficult but not impossible to be done in this period of time. I liked that it was challenging and it succeded to keep my
   interest up all the time. 

    Two things I will add/modify in the assignment:

       1. I think it would be really cool to make mail system dynamic, so for example when the cpu is at the 90% capacity, the script will send an  
       alert e-mail.
       2. Second I would like to make the system more automated. I would make implement a system that at a specific hour in a day it will gather this
       information(something similar with crontab in linux).
  

