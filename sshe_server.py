import socket
import os
import pam
from pathlib import Path
import subprocess

home = str(Path.home())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
p = pam.pam()
port = 2222

p1 = subprocess.Popen(['python3','pty_1.py'],stdin=subprocess.PIPE,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

s.bind(('',port))

s.listen(10)

client, addr = s.accept()

def receive_str():
    buffer_str = ""
    try:   
        while True:
            x = client.recv(1024)
            y = x.decode()
            if y == '\x03':
                print('^C')
                client.close()
                exit()

            if y == '\r':
                print()
                return buffer_str     
            print(y,end = "",flush=True)
            buffer_str += y

    except KeyboardInterrupt:
        client.close()
        exit()


def auth_user():
    user_str = "Username:"
    client.send(user_str.encode())
    user = receive_str()
    print(user_str,user)
    pass_str = "Password:"
    client.send(pass_str.encode())
    password = receive_str()
    print(pass_str,password)
    return ((user,password))


user , password = auth_user()

while(not(p.authenticate(user, password))):
	user , password = auth_user()


while True:
        x = client.recv(1024)
        y = x.decode()
        if y == '\x03':
            print('^C')
            client.close()
            exit()

           
        p1.stdin.write(x)


	
