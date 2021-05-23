import os
import platform
import subprocess
import socket
 
#user name
print("user:")
user_name = subprocess.run('whoami', capture_output=True).stdout.decode() #recover & convert string
user_name = user_name[0:-1] #string cleaning, more readable

print(user_name + "\n")

#hostname
print("hostname:")
hostname  = socket.gethostname() #method from socket

print(hostname + "\n")

#CPU info
print("CPU info:")
lscpu = subprocess.run('lscpu', capture_output=True) #lscpu command
cpu_model = subprocess.run(['grep', 'Model name:*'], input=lscpu.stdout, capture_output=True).stdout.decode().split() #grep command for model name & convert to list
del cpu_model[0:2] #cleaning 1
del cpu_model[-3:-1], cpu_model[-1] #cleaning 2
cpu_name = " ".join(cpu_model) #conversion list to string, ready to output
threads = subprocess.run(['grep', 'CPU(s)*'], input=lscpu.stdout, capture_output=True).stdout.decode().split()[1] #grep threads number

cpus = subprocess.run(['grep', 'Core(s) per socket:*'], input=lscpu.stdout, capture_output=True).stdout.decode().split()[3] #grep cpus number

arch = subprocess.run(['grep', 'Architecture:*'], input=lscpu.stdout, capture_output=True).stdout.decode().split()[1] #grep architecture

freq_max = subprocess.run(['grep', 'CPU max MHz:*'], input=lscpu.stdout, capture_output=True).stdout.decode().split()[3] #grep max freq

freq_min = subprocess.run(['grep', 'CPU min MHz:*'], input=lscpu.stdout, capture_output=True).stdout.decode().split()[3] #grep min freq

print(freq_min)
print(freq_max)
print(arch)
print(cpus)
print(threads)
print(cpu_name + "\n")

#RAM info
print("RAM info")
free = subprocess.run(['free', '-m'], capture_output=True) #free command, RAM in MB
ram_info = subprocess.run(['grep', 'Mem:*'], input=free.stdout, capture_output=True).stdout.decode().split() #grep command to list [RAM info]
total_ram = ram_info[1]
used_ram = ram_info[2]
free_ram = ram_info[3]
available_ram = ram_info[6]

print(total_ram)
print(used_ram)
print(free_ram)
print(available_ram + "\n")

#Swap info
print("swap info")
swap_details = subprocess.run(['grep', 'Swap:*'], input=free.stdout, capture_output=True).stdout.decode().split() #grep command to list [swap info]
total_swap = swap_details[1]
used_swap = swap_details[2]
free_swap = swap_details[3]

print(total_swap)
print(used_swap)
print(free_swap + "\n")

#On linux we can check the value of swappiness
print("swappiness:")
swappiness = subprocess.run(['cat', '/proc/sys/vm/swappiness'], capture_output=True).stdout.decode()
swappiness = swappiness[0:-1] #string cleaning
print(swappiness + "\n")

#Disk info
print("Disks tree:")
lsblk = subprocess.run('lsblk', capture_output=True) #lsblk command
disk_nvme = subprocess.run(['grep', 'nvme'], input=lsblk.stdout, capture_output=True).stdout.decode()
disk_sd = subprocess.run(['grep', 'sd'], input=lsblk.stdout, capture_output=True).stdout.decode()

print(disk_nvme)
print(disk_sd)

#Todo

#GPU info

#Todo

#Uptime

#OS info

#Network info

