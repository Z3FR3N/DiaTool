import platform
import subprocess
from rich import print
from rich import pretty
from rich import inspect #display methods linked to any object
from rich import progress_bar
from rich.tree import Tree

##################################################

def cmd_to_list(grep_param, cmd):
    if (type(grep_param) == str) and (type(cmd) == str):
        command = subprocess.run(cmd, capture_output=True)  #run the command and capture the output
        cmd_list = subprocess.run(['grep', grep_param], input=command.stdout, capture_output=True).stdout.decode().split() #decode output into a list to improve data visualization
        return list(cmd_list)
    else:
        print('input non valido') #debug reason

def cmd_to_string(cmd):
    command = subprocess.run(cmd, capture_output=True).stdout.decode() #decode the output of cmd into a string
    return str(command)

def run(cmd):
    command = subprocess.run(cmd) #cmd 

##################################################

print(sys.platform)

#   Vecchio codice
#
#   #user name
#   print("user:")
#   user_name = subprocess.run('whoami', capture_output=True).stdout.decode() #recover & convert string
#   user_name = user_name[0:-1] #string cleaning, more readable
#   print(user_name + "\n")
#   
#   #hostname
#   print("hostname:")
#   hostname  = socket.gethostname() #method from socket
#   print(hostname + "\n")
#   
#   #CPU info
#   lscpu = subprocess.run('lscpu', capture_output=True) #lscpu command
#   cpu_model = subprocess.run(['grep', 'Model name:*'], input=lscpu.stdout, capture_output=True).stdout.decode().split() #grep command for model name & convert to list
#   threads = subprocess.run(['grep', 'CPU(s)*'], input=lscpu.stdout, capture_output=True).stdout.decode().split()[1] #grep threads number
#   cpus = subprocess.run(['grep', 'Core(s) per socket:*'], input=lscpu.stdout, capture_output=True).stdout.decode().split()[3] #grep cpus number
#   arch = subprocess.run(['grep', 'Architecture:*'], input=lscpu.stdout, capture_output=True).stdout.decode().split()[1] #grep architecture
#   freq_max = subprocess.run(['grep', 'CPU max MHz:*'], input=lscpu.stdout, capture_output=True).stdout.decode().split()[3] #grep max freq
#   freq_min = subprocess.run(['grep', 'CPU min MHz:*'], input=lscpu.stdout, capture_output=True).stdout.decode().split()[3] #grep min freq
#   
#   del cpu_model[0:2] #cleaning 1
#   del cpu_model[-3:-1], cpu_model[-1] #cleaning 2
#   cpu_name = " ".join(cpu_model) #conversion list to string, ready to output
#   
#   print("CPU info:\n" + freq_min + "\n" + freq_max + "\n" + arch + "\n" + cpus + "\n" + threads + "\n" + cpu_name + "\n")
#   
#   #RAM info
#   free = subprocess.run(['free', '-m'], capture_output=True) #free command, RAM in MB
#   ram_info = subprocess.run(['grep', 'Mem:*'], input=free.stdout, capture_output=True).stdout.decode().split() #grep command to list [RAM info]
#   
#   total_ram = ram_info[1]
#   used_ram = ram_info[2]
#   free_ram = ram_info[3]
#   available_ram = ram_info[6]
#   
#   print("RAM info\n" + total_ram + "\n" + used_ram + "\n" + free_ram + "\n" + available_ram + "\n")
#   
#   #Swap info
#   swap_details = subprocess.run(['grep', 'Swap:*'], input=free.stdout, capture_output=True).stdout.decode().split() #grep command to list [swap info]
#   total_swap = swap_details[1]
#   used_swap = swap_details[2]
#   free_swap = swap_details[3]
#   
#   print("swap info\n" + total_swap + "\n" + used_swap + "\n" + free_swap + "\n")
#   
#   #On linux we can check the value of swappiness
#   swappiness = subprocess.run(['cat', '/proc/sys/vm/swappiness'], capture_output=True).stdout.decode()
#   swappiness = swappiness[0:-1] #string cleaning
#   print("swappiness:" + swappiness + "\n")
#   
#   #Disk info
#   lsblk = subprocess.run('lsblk', capture_output=True) #lsblk command
#   disk_nvme = subprocess.run(['grep', 'nvme'], input=lsblk.stdout, capture_output=True).stdout.decode()
#   disk_sd = subprocess.run(['grep', 'sd'], input=lsblk.stdout, capture_output=True).stdout.decode()
#   
#   print("Disk tree:\n" + disk_nvme + "\n" + disk_sd) #cleaning needed
#   
#   #GPU info
#   lspci = subprocess.run(['lspci'], capture_output=True)#general info for GPUs
#   int_gpu = subprocess.run(['grep', 'VGA compatible controller:'], capture_output=True, input=lspci.stdout).stdout.decode()
#   ded_gpu_nvidia = subprocess.run(['grep', '3D controller'], capture_output=True, input=lspci.stdout).stdout.decode()
#   ded_gpu_amd = subprocess.run(['grep', 'Display controller'], capture_output=True, input=lspci.stdout).stdout.decode()
#   
#   print(int_gpu + "\n" + ded_gpu_nvidia + "\n" + ded_gpu_amd) #cleaning needed
#   
#   #Uptime
#   uptime = subprocess.run(['uptime', '-p'], capture_output=True).stdout.decode()
#   print(uptime)
#   
#   #distro Linux info
#   os_info = subprocess.run(['cat', '/etc/lsb-release'], capture_output=True)#releases info
#   distro_info = subprocess.run(['grep', 'DISTRIB_DESCRIPTION'], capture_output=True, input=os_info.stdout).stdout.decode() 
#   distro_ver =  subprocess.run(['grep', 'DISTRIB_RELEASE'], capture_output=True, input=os_info.stdout).stdout.decode()
#   print(distro_info + "\n" + distro_ver)#cleaning needed
#   
#   #Network info
#   wifi_adapter = subprocess.run(['grep', 'Network controller:'], capture_output=True, input=lspci.stdout).stdout.decode()
#   ip_address = subprocess.run(['ip', 'address'], capture_output=True)
#   ip_string = subprocess.run(['grep', 'inet'], capture_output=True, input=ip_address.stdout).stdout.decode().split()
#   print("Network info: \nWifi adapter:\n" + wifi_adapter)#cleaning needed
#   print(ip_string)#need a better way to print the output, info are in the list generated, we can found ipv4, ipv6 and gateway