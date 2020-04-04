import socket
import sys
import readchar
import multiprocessing

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 2222
host_ip = '127.0.0.1'

s.connect((host_ip,port))



def input_send(s):
    sys.stdin = open(0)
    while True:
        c = readchar.readchar()
        x = c.encode()
        s.send(x)
        #print(x)
        if x == '\x03':
            s.close()
        #print(c)


def get_output(s):
    while True:
        d = s.recv(1024)
        print(d.decode(),end = "",flush=True)


t1 = multiprocessing.Process(target = input_send,args = (s,))
t2 = multiprocessing.Process(target = get_output,args = (s,))

t1.start()
t2.start()

t1.join()
t2.join()


        
