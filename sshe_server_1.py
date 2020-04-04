import socket
import os
import pam
from pathlib import Path
import subprocess
import multiprocessing
import time



home = str(Path.home())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
p = pam.pam()
port = 2222


s.bind(('',port))

s.listen(10)

client, addr = s.accept()

p1 = subprocess.Popen(['python3','pty_1.py'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)

f = open('typescript','rb')

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


def input_send(client,p1):
    while True:
            x = client.recv(1024)
            y = x.decode()
            #print(y)
            if y == '\x03':
                print('^C')
                client.close()
                exit()

               
            p1.stdin.write(x)
            p1.stdin.flush()


def output_send(client,f):
    try:
        lines = follow(f)
        for line in lines:
            print(line.decode(),end = "",flush = True)
            client.send(line)
    except KeyboardInterrupt:
        #client.close()
        return        

t1 = multiprocessing.Process(target = input_send,args = (client,p1))
t2 = multiprocessing.Process(target = output_send,args = (client,f))

t1.start()
t2.start()

t1.join()
t2.join()

	
