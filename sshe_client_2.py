import socket
import sys
import readchar
import multiprocessing
from diffiehellman import *
import pickle
import getpass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

port = 2223
host_ip = '127.0.0.1'

hash_table = {}

s.connect((host_ip,port))

def send_password(password):
	password += chr(10)
	print(password)
	for c in password:
		c = ord(c)*sharedSecret
		x = (str(c.x.n)+";"+str(c.y.n)+"|").encode()
		s.send(x)
	
def receive_ack():
	msg = s.recv(1024).decode()
	points = msg.split(";")
	x,y = points[0],points[1]
	x = int(x)
	y = int(y)
	count = 1
	temp = Point(curve,F(x),F(y))	
	while(not temp == sharedSecret):
		temp = temp - sharedSecret
		count += 1
	d = chr(count)
	if(d == "y"):
		return 1
	else:
		return 0

def sendFunction(sharedKey):
    msg = (str(sharedKey.x.n)+";"+str(sharedKey.y.n)).encode()
    s.send(msg)

def recvFunction():
    msg = s.recv(1024).decode()
    #msg = s.recv(9).decode()
    x,y = msg.split(";")
    x = int(x)
    y = int(y)
    return Point(curve,F(x),F(y))

def input_send(s):
    sys.stdin = open(0)
    global sharedSecret
    while True:
        c = readchar.readchar()
        c = ord(c)*sharedSecret
        x = (str(c.x.n)+";"+str(c.y.n)+"|").encode()
        s.send(x)
        #print(x)
        if x == '\x03':
            s.close()
        #print(c)


def get_output(s):
    global sharedSecret
    while True:
        msg = s.recv(1024).decode()
        messages = msg.split("|")
        for msg in messages:
            if msg == "":
                continue
            points = msg.split(";")
            if(len(points) < 2 or points[0] == "" or points[1] == ""):
                continue
            x,y = points[0],points[1]
            x = int(x)
            y = int(y)
            if((x,y) in hash_table.keys()):
                 d = hash_table[(x,y)]
            else:
                 count = 1
                 try :
                      temp = Point(curve,F(x),F(y))
                 except :
                      continue
                 while(not temp == sharedSecret):
                     temp = temp - sharedSecret
                     count += 1
                 d = chr(count)
                 hash_table[(x,y)] = d 
            print(d,end = "",flush=True)

F = FiniteField(3851, 1)

# Totally insecure curve: y^2 = x^3 + 324x + 1287
curve = EllipticCurve(a=F(324), b=F(1287))

# order is 1964
basePoint = Point(curve, F(920), F(303))

aliceSecretKey = generateSecretKey(8)#Client

alicePublicKey = sendDH(aliceSecretKey, basePoint, sendFunction)#Client

sharedSecret = receiveDH(aliceSecretKey,recvFunction)#Client

print('Shared secret is %s' % (sharedSecret))

print('extracing x-coordinate to get an integer shared secret: %d' % (sharedSecret.x.n))

ack = 0
count = 0
while(ack != 1 and count < 3):		
	password = getpass.getpass("Password : ")
	send_password(password)
	ack = receive_ack()
	count += 1
	if(ack == 0):
		print("Wrong Password Try again.....")

if(count == 3 and ack == 0):
	s.close()
	exit()

t1 = multiprocessing.Process(target = input_send,args = (s,))
t2 = multiprocessing.Process(target = get_output,args = (s,))

t1.start()
t2.start()

t1.join()
t2.join()




        
