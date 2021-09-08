# https://docs.python.org/3/library/sys.html#sys.platform
# https://docs.python.org/3/library/subprocess.html?highlight=subprocess#module-subprocess
# https://rich.readthedocs.io/en/latest/index.html
import time
from inspect import Arguments
import sys 
import subprocess
from rich import columns
from rich.columns import Columns
from rich import color, print, style, text 
from rich import pretty
from rich import inspect #display methods linked to any object
from rich import progress_bar
from rich import layout
from rich import tree
from rich import align
from rich import panel
from rich import padding
from rich.align import Align
from rich.padding import Padding
from rich.tree import Tree
from rich.text import Text
from rich.live import Live
from rich.layout import Layout
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
from rich import box
import pyfiglet

console = Console()
layout = Layout()
text = Text()

print('\n')

logo = pyfiglet.figlet_format("D i a T o o l", font = "3-d") #just a nice logo
console.print(logo, justify="center")

def welcome_message():
    if sys.platform.startswith('linux'):
        msg = ("We found ourselves in a [bold #ffa726]Linux-based[/bold #ffa726] system, a wild penguin appears! :penguin:\n")
        keep_alive = True
        return(msg, keep_alive)
    elif sys.platform.startswith('win32'):
        msg = ("We found ourselves in a [bold #004d90]Windows-based[/bold #02a9f4] system, it's chilly outside, better open the windows. \U0001fa9f \n")
        keep_alive = True
        return(msg, keep_alive)
    else:
        msg = (" Unfortunately [bold #e91e63]i can't detect[/bold #e91e63] the os we are in, so i'm basically useless....\U0001f480")
        keep_alive = False
        return(msg, keep_alive)
results = welcome_message()
welcome = results[0]

console.print("[bold yellow]Welcome[/bold yellow], this is a simple terminal tool to diagnose a pc and play with the network. If the script it's not displayed properly, maybe you should consider to increase the terminal size a little.\n\n" + welcome)

keep_alive = results[1]

if sys.platform.startswith('linux'):

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

    def disks_info(): #disk space informations, if there are parallel interface(like SATA) we can retrieve the disk model
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
        if len(disk_info_model1) == 1:
            disk_info_model1[0] = str(disk_info_model1)
            if disk_info_model1[0].find('[') != -1:
                disk_info_model1.insert(0, 'not found')
                disk_info_model1.pop(1)
        if len(disk_info_interface) == 1:
            disk_info_interface[0] = str(disk_info_interface)
            if disk_info_interface[0].find('[') != -1:
                disk_info_interface.insert(0, 'not found')
                disk_info_interface.pop(1)
        return(disk_info_model1, disk_info_interface, disk_info_sd1)

    def other_info(): #gpu integrated/dedicated, chipset version, usb/audio/sata controller with lscpi
        other_info_final = []
        other_info_list = []
        other_info_det =["VGA compatible controller:", "Display controller:", "ISA bridge:","Host bridge:", "USB controller:", "Audio device:", "SATA controller:","Non-Volatile memory controller:", "Network controller:", "3D controller:"]
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
        net_interface = []
        net_interface1 = []
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
        for j in range(len(state_list)):
            net_interface.clear()
            net_interface.append(name_list[j])
            net_interface.append(mac_list[j])
            net_interface.append(state_list[j])
            net_interface.append(qlen_list[j])
            net_interface.append(mtu_list[j])
            net_interface.append(inet_list[j])
            net_interface.append(bit_list[j])
            net_interface.append(brd_list[j])
            net_interface.append(inet6_list[j])
            net_interface.append(bit6_list[j])
            net_interface1.append(net_interface.copy())
        return(net_interface1)

    #°°°°°°°°°° INTERFACE °°°°°°°°°°°#

    cpu = cpu_details()
    ram = ram_details()
    disks = disks_info()
    disks_tree = ''
    disks_tree = '\n'.join(disks[2])
    info = other_info()
    controllers = ''
    controllers = '\n\n'.join(info)
    network = network_details()
        
    # quick way to calculate how many cores the CPU has
    n_threads = int(cpu[3])
    threads_per_core = int(cpu[5])
    n_core = n_threads / threads_per_core
    n_core = int(n_core)
    n_core = str(n_core)

    ## CPU AND RAM TABLE ##
    
    table = Table(title=cmd_to_string('hostname')[:-1], title_style="bold #ffa726", title_justify="center", expand=True, box=box.HEAVY_HEAD)
    
    table.add_column("CPU info", justify="right",   style="bold cyan")
    table.add_column("CPU data", justify="left"),
    table.add_column("RAM info", justify="right", style=" bold magenta")
    table.add_column("RAM Data", justify="left"),

    table.add_row("Architecture:", cpu[1])
    table.add_row("Core(s):", cpu[3], "Total:", ram[1])
    table.add_row("Thread(s):", cpu[7], "Used:", ram[3])
    table.add_row("Socket(s):", cpu[9][:-14], "Free:", ram[5])
    table.add_row("Model:", cpu[11], "Shared:", ram[7])
    table.add_row("CPU max freq:", cpu[13], "Buffered:", ram[9])
    table.add_row("CPU min freq:", cpu[15], "Available:", ram[11])
    table.add_row("L1d cache:", cpu[17], "Total Swap:", ram[13])
    table.add_row("L1i cache:", cpu[19], "Used Swap:", ram[15])
    table.add_row("L2 cache:", cpu[21], "Free Swap:", ram[17])
    table.add_row("L3 cache:", cpu[23])

    ## DISKS TABLE ##

    table2 = Table(expand = True, box=box.HEAVY_HEAD)

    table2.add_column("Legend", justify="center")
    table2.add_column("Disks tree", justify="left")

    table2.add_row("[bold red]MAJ:MIN[/bold red]\nmajor:minor device number\n\n[bold red]RM[/bold red]\nremovable device\n\n[bold red]RO[/bold red]\nread only device\n\n[bold red]MOUNTPOINT[/bold red]\nwhere the device is mounted", "[bold green1]NAME      MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINT[/bold green1]\n\n" + disks_tree)

    ## CONTROLLERS TABLE ##

    table3 = Table(expand = True, box=box.HEAVY_HEAD, show_footer=True, footer_style="bold white")

    table3.add_column("Controllers", justify="center", footer="Here you can find some useful informations like USB controllers, Integrated/dedicated GPU, audio controller etc...")
    
    table3.add_row(controllers)

    renderable = []
    renderable.append(table)
    renderable.append(table2)
    renderable.append(table3)

    ## NETWORK TABLE https://www.networkworld.com/article/3262045/checking-your-network-connections-on-linux.html##
    renderable.append(
        Panel(
            Text(
                "Network interfaces",
                style="bold", justify="center"
            ), box=box.HEAVY
        )
    )

    loopback_list = []
    wireless_list = []
    ethernet_list = []
    lis1 = []
    lis2 = []
    lis3 = []

    table4 = Table(expand = True, box = box.HEAVY_HEAD)
    
    for i in range(len(network)):
            for j in range(len(network[i])):
                string = str(network[i][j])
                if string.find("lo:") != -1:
                    lis1.append("\n[bold yellow1]Mac Address:[/bold yellow1] " + network[i][j+1] + '\n')
                    lis1.append("[bold yellow1]State:[/bold yellow1] " + network[i][j+2] + '\n')
                    lis1.append("[bold yellow1]Qlen:[/bold yellow1] " + network[i][j+3] + '\n')
                    lis1.append("[bold yellow1]MTU:[/bold yellow1] " + network[i][j+4] + '\n')
                    lis1.append("[bold yellow1]IPv4:[/bold yellow1] " + network[i][j+5] + " (bit: " + network[i][j+6] + ')\n')
                    lis1.append("[bold yellow1]IPv4 brd:[/bold yellow1] " + network[i][j+7] + '\n')
                    lis1.append("[bold yellow1]IPv6:[/bold yellow1] " + network[i][j+8] + " (bit: " + network[i][j+9] + ')\n')
                    string1 = ''.join(lis1)
                    loopback_list.append(string1)
                    string1 = ''
                if string.find("wlp") != -1:
                    lis2.append("\n[bold yellow1]Name:[/bold yellow1] " + network[i][j][:-1] + '\n')
                    lis2.append("[bold yellow1]Mac Address:[/bold yellow1] " + network[i][j+1] + '\n')
                    lis2.append("[bold yellow1]State:[/bold yellow1] " + network[i][j+2] + '\n')
                    lis2.append("[bold yellow1]Qlen:[/bold yellow1] " + network[i][j+3] + '\n')
                    lis2.append("[bold yellow1]MTU:[/bold yellow1] " + network[i][j+4] + '\n')
                    lis2.append("[bold yellow1]IPv4:[/bold yellow1] " + network[i][j+5] + " (bit: " + network[i][j+6] + ')\n')
                    lis2.append("[bold yellow1]IPv4 brd:[/bold yellow1] " + network[i][j+7] + '\n')
                    lis2.append("[bold yellow1]IPv6:[/bold yellow1] " + network[i][j+8] + " (bit: " + network[i][j+9] + ')\n')
                    string1 = ''.join(lis2)
                    wireless_list.append(string1)
                    string1 = ''
                if string.find("eth") != -1:
                    lis3.append("[yellow1]Name:[/yellow1] " + network[i][j][:-1] + '\n')
                    lis3.append("Mac Address:[/red] " + network[i][j+1] + '\n')
                    lis3.append("[red]State:[/red] " + network[i][j+2] + '\n')
                    lis3.append("[red]Qlen:[/red] " + network[i][j+3] + '\n')
                    lis3.append("[red]MTU:[/red] " + network[i][j+4] + '\n')
                    lis3.append("[red]IPv4:[/red] " + network[i][j+5] + " (bit: " + network[i][j+6] + ')\n')
                    lis3.append("[red]IPv4 brd:[/red] " + network[i][j+7] + '\n')
                    lis3.append("[red]IPv6:[/red] " + network[i][j+8] + " (bit: " + network[i][j+9] + ')')
                    string1 = ''.join(lis3)
                    ethernet_list.append(string1)
                    string1 = ''

    for i in range(len(loopback_list)):
        renderable.append(
            Panel.fit(
                loopback_list[i],
                 box=box.DOUBLE_EDGE, title="[bold]Localhost[/bold]"
            )
        )

    for i in range(len(wireless_list)):
        renderable.append(
            Panel.fit(
                wireless_list[i],
                box=box.DOUBLE_EDGE, title="[bold]Wireless Interfaces[/bold]"
            )
        )
    
    for i in range(len(ethernet_list)):
        renderable.append(
            Panel.fit(
                ethernet_list[i],
                box=box.DOUBLE_EDGE, title="[bold]Ethernet[/bold]"
            )
        )
    
    col = Columns(renderable)
    print(col)

if sys.platform.startswith('win32'):
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