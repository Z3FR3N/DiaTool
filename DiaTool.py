import os
import platform
import subprocess
import socket
 
#user name
user_name = subprocess.run('whoami', capture_output=True).stdout.decode() #recover & convert string
user_name = user_name[0:-1] #more readable

print(user_name)

#hostname
hostname  = socket.gethostname() #hostname

print(hostname)

#CPU details
lscpu = subprocess.run('lscpu', capture_output=True) #lscpu process
cpu_model = subprocess.run(['grep', 'Model name:*'], input=lscpu.stdout, capture_output=True).stdout.decode().split() #grep process for model name & convert to string
del cpu_model[0:2] #cleaning 1
del cpu_model[-3], cpu_model[-2], cpu_model[-1] #cleaning 2
cpu_name = " ".join(cpu_model) #cpu model
threads = subprocess.run(['grep', 'CPU(s)*'], input=lscpu.stdout, capture_output=True).stdout.decode().split()[1]

cpus = subprocess.run(['grep', 'Core(s) per socket:*'], input=lscpu.stdout, capture_output=True).stdout.decode().split()[3]

arch = subprocess.run(['grep', 'Architecture:*'], input=lscpu.stdout, capture_output=True).stdout.decode().split()[1]

freq_max = subprocess.run(['grep', 'CPU max MHz:*'], input=lscpu.stdout, capture_output=True).stdout.decode().split()[3]

freq_min = subprocess.run(['grep', 'CPU min MHz:*'], input=lscpu.stdout, capture_output=True).stdout.decode().split()[3]

print(freq_min)
print(freq_max)
print(arch)
print(cpus)
print(threads)
print(cpu_name)

#Network informations


