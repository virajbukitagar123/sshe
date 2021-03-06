import socket
import os
from pathlib import Path
import subprocess
import multiprocessing
import time
from diffiehellman import *
import pickle
import crypt

def receive_password():
	password = ""
	y = 0
	while(y != 10):
		t = ""
		message = ""
		while(t != "|"):
			t = client.recv(1).decode()
			message += t
		message = message[:len(message)-1]
		points = message.split(";") 
		x,y = points[0],points[1]
		x = int(x)
		y = int(y)
		count = 1
		print("X",x,"Y",y)
		temp = Point(curve,F(x),F(y))
		while(not temp == sharedSecret):
		   temp = temp - sharedSecret
		   count += 1
		y = count
		password += chr(count)
	return password[:len(password)-1]

def receive_username():
	username = ""
	y = 0
	while(y != 10):
		t = ""
		message = ""
		while(t != "|"):
			t = client.recv(1).decode()
			message += t
		message = message[:len(message)-1]
		points = message.split(";") 
		x,y = points[0],points[1]
		x = int(x)
		y = int(y)
		count = 1
		print("X",x,"Y",y)
		temp = Point(curve,F(x),F(y))
		while(not temp == sharedSecret):
		   temp = temp - sharedSecret
		   count += 1
		y = count
		username += chr(count)
	return username[:len(username)-1]
	

def authorize(username,password):
	try:
		f = open('/etc/shadow','r')

		a = f.readlines()

		print(password)
		#username = "root"	

		for i in a:
			if username in i:
				line = i
				break
		#print(line)
		e = line.split(":")[1]
		print(e)
		k = e.rfind('$')
		#print(k)
		salt = e[:k]
		#print(salt)
		encoded  = crypt.crypt(password,salt)

		if(e == encoded):
			print("Password is correct")
		return e == encoded
	except Exception as e:
		return False

def send_ack(ack):
	if(ack == 0):
		c = ord("n")*sharedSecret
		x = (str(c.x.n)+";"+str(c.y.n)).encode()
		client.send(x)
	else:
		c = ord("y")*sharedSecret
		x = (str(c.x.n)+";"+str(c.y.n)).encode()
		client.send(x)

home = str(Path.home())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
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
            msg = client.recv(1024).decode()
            #msg = client.recv(9).decode()
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
                count = 1
                try:
                    temp = Point(curve,F(x),F(y))
                except:
                    continue
                while(not temp == sharedSecret):
                   temp = temp - sharedSecret
                   count += 1
                y = chr(count).encode()
                #y = y.decode()
                #print("Character ",y.decode())
                if y == '\x03':
                    print('^C')
                    client.close()
                    exit()

               
                p1.stdin.write(y)
                p1.stdin.flush()


def output_send(client,f):
    try:
        lines = follow(f)
        for line in lines:
            print(line.decode(),end = "",flush = True)
            line = list(line.decode())
            for i in line:
                c = ord(i)*sharedSecret
                x = (str(c.x.n)+";"+str(c.y.n)+"|").encode()
                client.send(x)
            #client.send(line)
    except KeyboardInterrupt:
        #client.close()
        return 

def sendFunction(sharedKey):
    global client
    msg = (str(sharedKey.x.n)+";"+str(sharedKey.y.n)).encode()
    client.send(msg)

def recvFunction():
    global client
    msg = client.recv(1024).decode()
    x,y = msg.split(";")
    x = int(x)
    y = int(y)
    return Point(curve,F(x),F(y))

F = FiniteField(3851, 1)

# Totally insecure curve: y^2 = x^3 + 324x + 1287
curve = EllipticCurve(a=F(324), b=F(1287))

# order is 1964
basePoint = Point(curve, F(920), F(303))

bobSecretKey = generateSecretKey(8)#Server

bobPublicKey = sendDH(bobSecretKey, basePoint, sendFunction)#Server

sharedSecret = receiveDH(bobSecretKey,recvFunction)#Server
print('Shared secret %s' % (sharedSecret))

print('extracing x-coordinate to get an integer shared secret: %d' % (sharedSecret.x.n))  

ack = 0
count = 0

while(ack != 1 and count < 3):
	username = receive_username()
	password = receive_password()
	ack = authorize(username,password)
	send_ack(ack)
	count+=1

if(count == 3 and ack != 1):
	client.close()
	exit()

t1 = multiprocessing.Process(target = input_send,args = (client,p1))
t2 = multiprocessing.Process(target = output_send,args = (client,f))

t1.start()
t2.start()

t1.join()
t2.join()

	
