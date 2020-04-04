import os
import subprocess

os.system('rm typescript')
os.system('touch typescript')

p1 = subprocess.Popen(['tail','-F','typescript'],stdout = subprocess.PIPE)

while True:
	print(p1.stdout.read().decode())
