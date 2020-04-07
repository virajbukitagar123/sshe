import crypt 
f = open('/etc/shadow','r')

a = f.readlines()

username = "root"
password = "qwer"	

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


print(encoded)
print(e == encoded)




