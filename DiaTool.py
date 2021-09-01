# https://docs.python.org/3/library/sys.html#sys.platform
# https://docs.python.org/3/library/subprocess.html?highlight=subprocess#module-subprocess
# https://rich.readthedocs.io/en/latest/index.html
from os import name
import time
from inspect import Arguments
import sys 
import subprocess
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
from rich.progress import Progress
from rich import box
import pyfiglet

console = Console()
layout = Layout()
text = Text()

keep_alive = True

def welcome_message():
    if sys.platform.startswith('linux'):
        msg = ("We found ourselves in a [bold #ffa726]Linux-based[/bold #ffa726] system :penguin:\n")
        keep_alive = True
        return(msg, keep_alive)
    elif sys.platform.startswith('win32'):
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

while keep_alive == True:
    if current_os == 'linux':

        #°°°°°°°°°° USEFUL FUNCTIONS °°°°°°°°°°°#

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
        
        def take_substring(end_char, string, ib): #input: the end character, the string to analyze and the index to begin with
            end_char = str(end_char)
            string = str(string)
            ib = int(ib)
            list =[]
            while string[ib] != end_char:
                list.append(string[ib])
                ib = ib + 1
            sep = ''
            substring = sep.join(list)
            return(substring)

        #°°°°°°°°°° FUNCTIONS TO RETRIEVE INFORMATIONS °°°°°°°°°°°#

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
        print(cpu_details())

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
        print(ram_details())

        def disk_info(): #disk space informations, if there are parallel interface(like SATA) we can retrieve the disk model
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
            n = len(disk_info_model1)
            if n > 1:
                disk_info_model1.pop(0)
                disk_info_model1.pop(-1)
            for i in range(len(disk_info_model)):
                disk_info_string1 = disk_info_model[i]
                disk_info_string2 = disk_info_string1[-4:]
                disk_info_interface.append(disk_info_string2)
            n = len(disk_info_interface)
            if n > 1:
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
        print(disk_info())

        def other_info(): #gpu integrated/dedicated, chipset version, usb/audio/sata controller with lscpi
            other_info_final = []
            other_info_list = []
            other_info_det =["VGA compatible controller:", "Display controller:", "ISA bridge:", "USB controller:", "Audio device:", "SATA controller:","Non-Volatile memory controller:", "Network controller:", "3D controller:"]
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
            while("" in other_info_final):
                other_info_final.remove("")
            return(other_info_final)
        print(other_info())

        def network_details():
            ip_det = cmd_to_string(['ip', 'address'])
            network_info = []
            name_list = []
            mtu_list = []
            mac_list = []
            inet_list = []
            inet6_list = []
            bit_list = []
            bit6_list = []
            brd_list = []
            state_list = []
            qlen_list = []
            network_info = ip_det.split('\n')
            for i in range(len(network_info)):
                network_info[i] = network_info[i].lstrip()
                if network_info[i].find('mtu') != -1:
                    n = 3
                    name_list.append(take_substring(' ', network_info[i], n))
                    n = network_info[i].index('mtu') + 4
                    mtu_list.append(take_substring(' ', network_info[i], n))
                    n = network_info[i].index('state') + len('state') + 1
                    state_list.append(take_substring(' ', network_info[i], n))
                    n = network_info[i].index('qlen') + len('qlen') + 1
                    qlen_list.append(network_info[i][n:])
                elif network_info[i].find('link/loopback') != -1:
                    n = network_info[i].index('link/loopback')
                    n = n + len('link/loopback') + 1
                    mac_list.append(take_substring(' ', network_info[i], n))
                elif network_info[i].find('link/ether') != -1:
                    n = network_info[i].index('link/ether')
                    n = n + len('link/ether') + 1
                    mac_list.append(take_substring(' ', network_info[i], n))
                elif network_info[i].find('inet ') != -1:
                    n = len('inet ')
                    inet_list.append(take_substring('/', network_info[i], n))
                    n = network_info[i].index('/') + 1
                    bit_list.append(take_substring(' ', network_info[i], n))
                    if network_info[i].find('brd') != -1:
                        n = network_info[i].index('brd') + len('brd') + 1
                        brd_list.append(take_substring(' ', network_info[i], n))
                elif network_info[i].find('inet6') != -1:
                    n = len('inet6') + 1
                    inet6_list.append(take_substring('/', network_info[i], n))
                    n = network_info[i].index('/') + 1
                    bit6_list.append(take_substring(' ', network_info[i], n))
            for i in range(0, len(state_list)):
                if state_list[i] == 'DOWN':
                    inet_list.insert(i, 'not found')
                    bit_list.insert(i, 'not found')
                    brd_list.insert(i, 'not found')
                    bit6_list.insert(i, 'not found')
                    inet6_list.insert(i, 'not found')
                if state_list[i] == 'UNKNOWN':
                    brd_list.insert(i, 'not found')
            return(network_info, name_list, mac_list, state_list, qlen_list, mtu_list, inet_list, bit_list, brd_list, inet6_list, bit6_list)
        print(network_details())

        #°°°°°°°°°° INTERFACE °°°°°°°°°°°#
        
        layout.split(
            Layout(name="header", size=3),
            Layout(name="cpu"),
            Layout(name="ram"),
            Layout(name="disk"),
            Layout(name="network"),
            Layout(name="Other info"),
        )

        layout["header"].split(
            Align.center(
                Panel.fit(cmd_to_string('hostname')[:-1], style="bold #ffa726", box = box.ROUNDED), 
            )
        )
        layout["cpu"].split_column(
            Align.center(
                Panel('prova')
            )
        )
        console.print(layout)
        keep_alive = False

    if current_os == 'win32':
        console.print("I'm still developing this part sorry. \n")
        
        with Progress() as progress:

            task1 = progress.add_task("[red]Playing video-games...", total=1000)
            task2 = progress.add_task("[green]Cooking...", total=1000)
            task3 = progress.add_task("[orchid]Eating pasta...", total=1000)
            task4 = progress.add_task("[cyan1]Sleeping...", total=1000)
            task5 = progress.add_task("[magenta]Eating pizza...", total=1000)
            task6 = progress.add_task("[dark_orange3]Playing chitarra...", total=1000)
            task7 = progress.add_task("[yellow]Studying (oh, cmon really?)...", total=1000)
            task8 = progress.add_task("[violet]Cooking the pizza i ate before (whaat?)...", total=1000)
            task9 = progress.add_task("[white]Browsing the Guatemala page in wikipedia...", total=1000)

            while not progress.finished:
                progress.update(task1, advance=1.5)
                progress.update(task2, advance=0.3)
                progress.update(task3, advance=0.7)
                progress.update(task4, advance=0.9)
                progress.update(task5, advance=1)
                progress.update(task6, advance=0.5)
                progress.update(task7, advance=0.1)
                progress.update(task8, advance=0.6)
                progress.update(task9, advance=0.8)
                time.sleep(0.02)
        valore = input("Inserire il valore: ")
        keep_alive = valore
else:
    exit()