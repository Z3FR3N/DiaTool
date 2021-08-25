from os import name
import time
from inspect import Arguments
import sys # https://docs.python.org/3/library/sys.html#sys.platform
import subprocess # https://docs.python.org/3/library/subprocess.html?highlight=subprocess#module-subprocess
# https://rich.readthedocs.io/en/latest/index.html
from rich import color, print, style, text 
from rich import pretty
from rich import inspect #display methods linked to any object
from rich import progress_bar
from rich import layout
from rich import tree
from rich import align
from rich import panel
from rich.align import Align
from rich.tree import Tree
from rich.text import Text
from rich.live import Live
from rich.layout import Layout
from rich.console import Console
from rich.panel import Panel
from rich import box
import pyfiglet

console = Console()
layout = Layout()

keep_alive = True

def welcome_message():
    if sys.platform.startswith('linux'):
        msg = ("We found ourselves in a [bold #ffa726]Linux-based[/bold #ffa726] system :penguin:\n")
        keep_alive = True
        return(msg, keep_alive)
    if sys.platform.startswith('win32'):
        msg = ("We found ourselves in a [bold #004d90]Windows-based[/bold #02a9f4] system \U0001fa9f \n\nHere's the details:\n")
        keep_alive = True
        return(msg, keep_alive)
    else:
        msg = (" Unfortunately [bold #e91e63]i can't detect[/bold #e91e63] the os we are in, so i'm basically useless....press Ctr+C to abort\U0001f480")
        keep_alive = False
        return(msg, keep_alive)

print('\n')

logo = pyfiglet.figlet_format("D i a T o o l", font = "3-d") #just a nice logo
console.print(logo, justify="center")

welcome = welcome_message()

console.print("[bold yellow]Welcome[/bold yellow], this is a simple terminal tool to diagnose this machine and play with the network. If you are not displaying it right, maybe you should consider to increase the terminal size a little, anyway...", welcome[0])

current_os = sys.platform

layout.split(
        Layout(name="header", size=3),
        Layout(name="cpu"),
        Layout(name="ram"),
        Layout(name="network"),
        Layout(name="Other info"),
        Layout(name="interactive")
    )

if keep_alive == True:
    if current_os == 'linux':

        def grep_to_string(grep_param, cmd): #useful to change and manipolate the output
            if (type(grep_param) == str) and (type(cmd) == str):
                command = subprocess.run(cmd, capture_output=True)  
                cmd_string = subprocess.run(['grep', grep_param], input=command.stdout, capture_output=True)    .stdout.decode().strip()
                return str(cmd_string)

        def grep_to_list(grep_param, cmd): #useful to change and manipolate the output
            if (type(grep_param) == str) and (type(cmd) == str):
                command = subprocess.run(cmd, capture_output=True)  
                cmd_list = subprocess.run(['grep', grep_param], input=command.stdout, capture_output=True). stdout.decode().split()
                return list(cmd_list)

        def cmd_to_string(cmd): #useful to immediately print the output onto a string
                command = subprocess.run(cmd, capture_output=True).stdout.decode()
                return str(command)

        def cmd_to_list(cmd): #useful to immediately print the output onto a list
            command = subprocess.run(cmd, capture_output=True).stdout.decode().split()
            return list(command)

        def cpu_details():
            cpu_final =[] #final list
            specs_list = [] #support list
            string_cpu2_to_list = [] #support list
            cpu_det_name = [ "Architecture:", "CPU(s): ", "Thread(s) per core:", "Socket(s):", "Model name:", "CPU max MHz:", "CPU min MHz:", "Virtualization:", "L1d cache:", "L1i cache:", "L2 cache:", "L3 cache:" ] #specs we're interested in, taken from lscpu
            for i in range(0, len(cpu_det_name)): 
                grep_param = cpu_det_name[i]
                string_cpu = (grep_to_string(grep_param, 'lscpu'))
                string_cpu1 = string_cpu.lstrip(grep_param)
                string_cpu2 = string_cpu1.strip(" ")
                if string_cpu2.find('node0') >= 2: #grep is taking too much,
                    string_cpu2_to_list = string_cpu2.rsplit('\n')#better trim it down
                    string_cpu2 = string_cpu2_to_list[0]
                specs_list.append(string_cpu2)#re-integrate the string into the list
            for i in range (0, len(cpu_det_name)):#assemble the final list with right specs
                cpu_final.append(cpu_det_name[i])
                cpu_final.append(specs_list[i])
            return(cpu_final)
        cpu_final = cpu_details()
        print(cpu_final)

        def ram_details():
            ram_final =[] #final list
            ram_details = [] #support list
            ram_details = cmd_to_list(['free', '--mega'])
            ram_det_name = [ "total_ram", "used_ram", "free_ram", "shared_ram", "buff_ram", "available_ram", "swap_total", "swap_used", "swap_free" ]
            for i in range (7):#some cleaning
                ram_details.pop(0)
            ram_details.pop(6)#some cleaning
            for i in range(0, len(ram_det_name)):#assemble the final list with right specs
                ram_final.append(ram_det_name[i])
                ram_final.append(ram_details[i])
            return(ram_final)
        ram_final = ram_details()
        print(ram_final)

        def disk_info(): #aggiungere lo stampaggio dei dischi con lsblk -S, usandolo anche per la dimensione dei dischi
            disk_info_model = []
            disk_info_model1 = []
            disk_info_interface = []
            disk_info_sd = []
            disk_info_sd1 = []
            disk_info_string = cmd_to_string(['lsblk', '-S'])
            disk_info_model = disk_info_string.split('\n')
            for i in range(len(disk_info_model)):
                disk_info_string1 = disk_info_model[i]
                disk_info_string2 = disk_info_string1[24:-26].strip()
                disk_info_model1.append(disk_info_string2)
            disk_info_model1.pop(0)
            disk_info_model1.pop(-1)
            for i in range(len(disk_info_model)):
                disk_info_string1 = disk_info_model[i]
                disk_info_string2 = disk_info_string1[-4:].strip()
                disk_info_interface.append(disk_info_string2)
            disk_info_interface.pop(0)
            disk_info_interface.pop(-1)
            disk_info_sd_string = cmd_to_string(['lsblk', '-l'])
            disk_info_sd = disk_info_sd_string.split('\n')
            for i in range(len(disk_info_sd)):
                disk_info_sd[i] = disk_info_sd[i].strip()
                if disk_info_sd[i].find('loop') != -1:
                    n = i
            for i in range(n+1, len(disk_info_sd)):
                disk_info_sd1.append(disk_info_sd[i])
            disk_info_sd1.pop(-1)
            return(disk_info_model1, disk_info_interface, disk_info_sd1)
        disk_info_final = disk_info()
        print(disk_info_final)

        def other_info(): #gpu integrated/dedicated, chipset version, usb/audio/sata controller with lscpi
            other_info_final = []
            other_info_list = []
            other_info_det =["VGA compatible controller:", "Display controller:", "ISA bridge:", "USB controller:", "Audio device:", "SATA controller:", "Network controller:"]
            for i in range(len(other_info_det)):
                grep_param = other_info_det[i]
                s = 8 + len(grep_param) + 1
                other_info_string =grep_to_string(grep_param, 'lspci')
                if other_info_string.find('\n') != -1:
                    other_info_list = other_info_string.split('\n')
                    for i in range(len(other_info_list)):
                        other_info_string1 = (other_info_list[i])
                        other_info_final.append(other_info_string1[s:])
                else:
                    other_info_final.append(other_info_string[s:])#usa lo slicing a 9 caratteri + il parametro grep
            return(other_info_final)
        other_info_final = other_info()
        print(other_info_final)

        def network_details():
            ip_det = cmd_to_string(['ip', 'address'])
            network_info = []
            network_info = ip_det.split('\n')
            network_info.pop(-1)
            for i in range(len(network_info)):
                network_info[i] = network_info[i].lstrip()
            return(network_info)
        network_info = network_details()
        print(network_info)
    if current_os == 'win32':
        print("[TODO]")
else:
    exit()