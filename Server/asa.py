import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy())
ssh.connect('192.168.0.104', username='cristian', password='k3blinuxmint')
ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("python check.py",get_pty=True)

for line in ssh_stdout.read().splitlines():
    print(line)
