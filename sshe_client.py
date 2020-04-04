import socket
import readchar

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 2222
host_ip = '127.0.0.1'

s.connect((host_ip,port))

def send_username():
    while True:
        c = readchar.readchar()
        x = c.encode()
        s.send(x)
        if c == '\r':
            print()
            return 

        print(c,end="",flush=True)
        
        if c == '\x03':
            print('^C')
            s.close()
            exit()

def send_password():
    while True:
        c = readchar.readchar()
        x = c.encode()
        s.send(x)
        if c == '\r':
            print()
            return 

        #print(c,end="",flush=True)
        
        if c == '\x03':
            print('^C')
            s.close()
            exit()


def auth_user():
    server_output = s.recv(4096).decode()
    print(server_output,end="",flush=True)
    send_username()
    server_output = s.recv(4096).decode()
    print(server_output,end="",flush=True)
    send_password()

a = "0"

while a == "0":
    auth_user()
    a = s.recv(1).decode()
    print(a)
    print()


while True:
        c = readchar.readchar()
        x = c.encode()
        s.send(x)
        
