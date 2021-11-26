# https://docs.python.org/3/library/sys.html#sys.platform
# https://docs.python.org/3/library/subprocess.html?highlight=subprocess#module-subprocess
# https://rich.readthedocs.io/en/latest/index.html

from os import name
import time
import sys 
import subprocess
from rich.columns import Columns
from rich import print
from rich.align import Align
from rich.padding import Padding
from rich.tree import Tree
from rich.text import Text
from rich.live import Live
from rich.layout import Layout
from rich.console import Console
from rich.emoji import Emoji
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress
from rich import box
import pyfiglet

console = Console(width=80)

print('\n')

logo = pyfiglet.figlet_format("D i a T o o l", font = "3-d") #just a nice logo
console.print(logo, justify="center")

def welcome_message():
    if sys.platform.startswith('linux'):
        msg = ("This is [bold #ffa726]Linux-based[/bold #ffa726] system, a wild penguin appears! :penguin:\n")
        keep_alive = True
        return(msg, keep_alive)
    elif sys.platform.startswith('win32'):
        msg = ("This is a [bold #004d90]Windows-based[/bold #004d90] system, it's quite hot here, better open the windows. \U0001fa9f \n")
        keep_alive = True
        return(msg, keep_alive)
    else:
        msg = (" Unfortunately [bold #e91e63]i can't detect[/bold #e91e63] the os we are in, so i'm basically useless....\U0001f480")
        keep_alive = False
        return(msg, keep_alive)
results = welcome_message()
welcome = results[0]

console.print("[bold yellow]Welcome[/bold yellow], this is a simple script to diagnose this machine and play with the network. If it's not displayed properly, just increase the terminal size. " + welcome)

keep_alive = results[1]

while keep_alive == True:
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

        def cmd_to_list(cmd, sep): #useful to immediately print the output onto a list
            command = subprocess.run(cmd, capture_output=True).stdout.decode().split(sep)
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
            ram_details = cmd_to_list(['free', '--mega'], None)
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
            ip_a = cmd_to_string(['ip', 'a'])
            net_list = []
            net_list = ip_a.split(': ')
            wireless_list = []
            ethernet_list = []
            localhost = []
            for i in range(len(net_list)):
                if net_list[i][:2] == 'wl':
                    s = i +1
                    wireless_list.append(net_list[i])
                    net_list[s] = net_list[s].replace('\n', ' ')
                    net_list[s] = net_list[s].replace('        ', ' ')
                    net_list[s] = net_list[s].replace('     ', ' ')
                    if net_list[s].find(' ', -2) == len(net_list[s])-2:
                        wireless_list.append(net_list[s][:-2])
                    else:
                        wireless_list.append(net_list[s][:-1])
                if net_list[i][:2] == 'en':
                    s = i + 1
                    ethernet_list.append(net_list[i])
                    net_list[s] = net_list[s].replace('\n', ' ')
                    net_list[s] = net_list[s].replace('        ', ' ')
                    net_list[s] = net_list[s].replace('     ', ' ')
                    if net_list[s].find(' ', -2) == len(net_list[s])-2:
                        ethernet_list.append(net_list[s][:-2])
                    else:
                        ethernet_list.append(net_list[s][:-1])
                if net_list[i][:2] == 'lo':
                    s = i + 1
                    localhost.append(net_list[i])
                    net_list[s] = net_list[s].replace('\n', ' ')
                    net_list[s] = net_list[s].replace('        ', ' ')
                    net_list[s] = net_list[s].replace('     ', ' ')
                    localhost.append(net_list[s][:-2])
            return(wireless_list, localhost, ethernet_list)

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

        ## CPU AND RAM ##

        hostname = Align.center(Panel.fit(Text(cmd_to_string('hostname')[:-1], style = "bold #ffa726", justify="center"), style="#ffa726"))
        
        table = Table(border_style="pale_turquoise1", expand=True, box=box.HEAVY_HEAD)
        
        table.add_column(Text('CPU info', style='bold green1', justify='center'), justify="right",   style="bold yellow")
        table.add_column(Text('CPU data', style='bold green1', justify='center'), justify="left"),
        table.add_column(Text('RAM info', style='bold green1', justify='center'), justify="right", style= "bold yellow")
        table.add_column(Text('RAM data', style='bold green1', justify='center'), justify="left"),

        table.add_row("Architecture:", cpu[1])
        table.add_row("Core(s):", cpu[3], "Total:", ram[1])
        table.add_row("Thread(s) per core:", cpu[5], "Used:", ram[3])
        table.add_row("Socket(s):", cpu[7], "Free:", ram[5])
        table.add_row("Model:", cpu[9][:-14], "Shared:", ram[7])
        table.add_row("CPU max freq:", cpu[11], "Buffered:", ram[9])
        table.add_row("CPU min freq:", cpu[13], "Available:", ram[11])
        table.add_row("L1d cache:", cpu[17], "Total Swap:", ram[13])
        table.add_row("L1i cache:", cpu[19], "Used Swap:", ram[15])
        table.add_row("L2 cache:", cpu[21], "Free Swap:", ram[17])
        table.add_row("L3 cache:", cpu[23])

        ## DISKS ##

        table2 = Table(border_style="pale_turquoise1", expand = True, box=box.HEAVY_HEAD)

        table2.add_column("[bold green1]Legend[/bold green1]", justify="center")
        table2.add_column(Text('Disk Tree', style='bold green1', justify='center'))

        table2.add_row()
        table2.add_row("[bold yellow]MAJ:MIN[/bold yellow]\nmajor:minor device number\n\n[bold yellow]RM[/bold yellow]\nremovable device\n\n[bold yellow]RO[/bold yellow]\nread only device\n\n[bold yellow]MOUNTPOINT[/bold yellow]\nwhere the device is mounted", "[bold yellow]NAME     MAJ:MIN  RM   SIZE RO TYPE MOUNTPOINT[/bold yellow]\n\n" + disks_tree)
        table2.add_row()

        ## CONTROLLERS ## note: nvme disks models shows up here

        table3 = Table(expand = True, box=box.HEAVY_HEAD, show_footer=True, footer_style="bold white", show_lines = True, border_style="pale_turquoise1")

        table3.add_column("[bold green1]Controllers[/bold green1]", justify="center", footer="Here you can find some useful informations like USB controllers, Integrated/dedicated GPU, audio controller etc...")
        
        controllers = controllers.split('\n\n')
        for i in range(len(controllers)):
            table3.add_row(controllers[i])

        tables = []
        tables.append(hostname)
        tables.append(table)
        tables.append('\n')
        tables.append(table2)
        tables.append('\n')
        tables.append(table3)
        tables.append('\n')
        console.print(Columns(tables))
        tables.clear()
        
        ## NETWORK https://www.networkworld.com/article/3262045/checking-your-network-connections-on-linux.html##
        
        console.print(Panel(Text('Network interfaces', justify='center', style='bold green1'), box=box.HEAVY, border_style='pale_turquoise1'))

        def net_specs(list1):
            result = []
            string = str(list1)
            if string.find("LOWER_UP") != -1:
                result.append("[green1]Connected to the network[/green1] :link:")
            if string.find('BROADCAST') != -1:
                result.append('Broadcasting is supported :thumbs_up:')
            if string.find('MULTICAST') != -1:
                result.append('Multicasting is supported :thumbs_up:')
            if string.find('lo', 0, 5) != -1:
                result.append('[bold yellow]Type:[/bold yellow] Localhost :desktop_computer:')
            if string.find('wl', 0, 5) != -1:
                b = string.find('wl')
                e = string.find(',') -1
                result.append('[bold yellow]Type:[/bold yellow] Wireless :satellite:')
            if string.find('en', 0, 5) != -1:
                result.append('[bold yellow]Type:[/bold yellow] Ethernet :electric_plug:')
            if string.find('UP') != -1:
                result.append('[bold yellow]State:[/bold yellow] Enabled 	:white_check_mark:')
            elif string.find('DOWN')!= -1:
                result.append('[bold yellow]State:[/bold yellow] Disabled :x:')
            if string.find('mtu') != -1:
                b = string.find('mtu') + 4
                e = string.find('qdisc') - 1
                result.append("[bold yellow]MTU:[/bold yellow] " + string[b:e])
            if string.find("qdisc") != -1:
                b = string.find("qdisc") + 6
                e = string.find("state") - 1
                result.append("[bold yellow]Queuing:[/bold yellow] " + string[b:e])
            if string.find("group") != -1:
                b = string.find("group") + 6
                e = string.find("qlen") - 1
                result.append("[bold yellow]Group:[/bold yellow] " + string[b:e])
            if string.find("link/ether") != -1:
                b = string.find("link/ether") + 11
                e = string.find("brd") - 1
                result.append("[bold yellow]MAC:[/bold yellow] " + string[b:e])
            if string.find("brd") != -1:
                b = string.find("brd ") + len("brd") + 1
                if string.find("altname") != -1:
                    e = string.find("altname") -1
                else:
                    e = string.find("inet") - 1
                result.append("[bold yellow]Brd MAC:[/bold yellow] " + string[b:e])
            if string.find("inet") != -1:
                b = string.find("inet") + len("inet") + 1
                e = string.find("/", b)
                result.append("[bold yellow]IPv4:[/bold yellow] " + string[b:e])
                b = e + 1
                e = string.find(" ", b)
                result.append("[bold yellow]Bit IPv4:[/bold yellow] " + string[b:e])
                if string.find("brd", e) != -1:
                    b = string.find("brd", e) + len("brd") + 1
                    e = string.find("scope", b) - 1
                    result.append("[bold yellow]Brd IPv4:[/bold yellow] " + string[b:e])
            if string.find("scope") != -1:
                b = string.find("scope") + len("scope") + 1
                e = string.find(" ", b)
                result.append("[bold yellow]Scope:[/bold yellow] " + string[b:e])
                b = e + 1
                e = string.find(" ", b)
                result.append("[bold yellow]Addr type:[/bold yellow] " + string[b:e])
            if string.find("valid_lft") != -1:
                b = string.find("valid_lft") + len("valid_lft") + 1
                e = string.find(" ", b)
                result.append("[bold yellow]Lifetime (lft):[/bold yellow] " + string[b:e])
            if string.find("preferred_lft") != -1:
                b = string.find("preferred_lft") + len("preferred_lft") + 1
                e = string.find(" ", b)
                result.append("[bold yellow]Preferred lft:[/bold yellow] " + string[b:e])
            if string.find("inet6") != -1:
                b = string.find("inet6") + len("inet6") + 1
                e = string.find("/", b)
                result.append("[bold yellow]IPv6:[/bold yellow] " + string[b:e])
                result.append("[bold yellow]Bit IPv6:[/bold yellow] " + string[e+1:e+3])
            if string.rfind("valid_lft") != -1:
                b = string.rfind("valid_lft") + len("valid_lft") + 1
                e = string.find(" ", b)
                result.append("[bold yellow]Lifetime:[/bold yellow] " + string[b:e])
            if string.rfind("preferred_lft") != -1:
                b = string.rfind("preferred_lft") + len("preferred_lft") + 1
                e = string.find("'", b)
                result.append("[bold yellow]Preferred lft:[/bold yellow] " + string[b:e])
            return(result)

        localhost = net_specs(network[1])
        wireless_list = net_specs(network[0])
        ethernet_list = net_specs(network[2])
        
        if len(network[2])>=1 and len(ethernet_list)>=1:
            ethernet_table = Table(border_style="pale_turquoise1", width=40,  expand = True, box=box.HEAVY_HEAD)

            for i in range(0, len(network[2]), 2):
                ethernet_table.add_column(Text(network[2][i], justify="center", style="bold #ffa726"))

            for i in range(len(ethernet_list)):
                ethernet_table.add_row(ethernet_list[i])
            tables.append(ethernet_table)
        
        if len(network[0])>=1 and len(wireless_list)>=1:
            wireless_table = Table(border_style="pale_turquoise1",width=40, expand = True, box=box.HEAVY_HEAD)
            
            for i in range(0, len(network[0]), 2):
                wireless_table.add_column(Text(network[0][i], justify="center", style="bold #ffa726"))

            for i in range(len(wireless_list)):
                wireless_table.add_row(wireless_list[i])
            tables.append(wireless_table)

        if len(network[1])>=1 and len(localhost)>=1:
            localhost_table = Table(border_style="pale_turquoise1", width=40, expand = True, box=box.HEAVY_HEAD)

            for i in range(0, len(network[1]), 2):
                localhost_table.add_column(Text(network[1][i], justify="center", style="bold #ffa726"))

            for i in range(len(localhost)):
                localhost_table.add_row(localhost[i])

        if len(tables) > 1:
            console.print(Align(localhost_table, align="center"))
        else:
            tables.append(localhost_table)

        console.print(Columns(tables, padding=(0, 0)))

        ## PROCESSES AND PORTS ##
        pr_list = cmd_to_list(['lsof', '-i', '-P', '-n'], '\n')
        pr_list.pop(0)
        pr_list.pop(-1)
        pr_list2 = [[]]
        for i in range(len(pr_list)):
            pr_list2.append(pr_list[i].split())
        for i in range(len(pr_list2)):
            if pr_list2 == '':
                pr_list2.pop(i)
        pr_list2.pop(0)
        pr_name = []
        for i in range(len(pr_list2)):
            n = pr_name.count(pr_list2[i][0])
            if n == 0:
                pr_name.append(pr_list2[i][0])
            else:
                i =+ 1
        pr_tables = []
        for i in range(len(pr_name)):
            pr_table = Table(title=Text(pr_name[i], style="bold #ffa726"), border_style="pale_turquoise1", expand = True, box=box.HEAVY_HEAD)
            pr_table.add_column("[bold yellow]PID[/bold yellow]", justify="center")
            pr_table.add_column("[bold yellow]USER[/bold yellow]", justify="center")
            pr_table.add_column("[bold yellow]FD[/bold yellow]", justify="center")
            pr_table.add_column("[bold yellow]NODE[/bold yellow]", justify="center")
            pr_table.add_column("[bold yellow]IP IN:PORT -> IP OUT:PORT[/bold yellow]", justify="left")
            for n in range(len(pr_list2)):
                if pr_list2[n][0] == pr_name[i]:
                    pr_table.add_row(Text(pr_list2[n][1]), Text(pr_list2[n][2]), Text(pr_list2[n][5]), Text(pr_list2[n][7]), Text(pr_list2[n][8]))
            pr_tables.append(pr_table)
        console.print(Panel(Columns(pr_tables), title="[bold green1]Pocesses and Ports[/bold green1]", padding= (1,0), box=box.HEAVY))
        #console.print(subprocess.run(['curl', 'https://ipinfo.io/ip']))
        #SUBNET MASK -> dai bit dell'ipv4
        #TEMPO DI LEASE -> sempre con ip
        #CALCOLO PING MEDIO -> ping
        #JITTER -> ping
        #SCAN DELLA RETE LOCALE -> ping + analisi del TTL
        #LISTA DI SERVER DNS -> da fare: Cloudflare, Google public DNS, OpenDNS
        #DNS UTILIZZATO -> systemd-resolve

    if sys.platform.startswith('win32'):
        console.print("I'm still developing this part sorry. \n")
        
        with Progress() as progress:
            task1 = progress.add_task("[red]Playing league of legends...", total=1000)
            task2 = progress.add_task("[green]Cooking a panda...", total=1000)
            task3 = progress.add_task("[orchid]Eating pasta...", total=1000)
            task4 = progress.add_task("[cyan1]Sleeping(like, a lot)...", total=1000)
            task5 = progress.add_task("[magenta]Eating pizza(frozen? Cmon dude)...", total=1000)
            task6 = progress.add_task("[dark_orange3]Playing sea of thieves...", total=1000)
            task7 = progress.add_task("[yellow]Studying (oh, cmon really?)...", total=1000)
            task8 = progress.add_task("[violet]Cooking the pizza i ate before (that's better)...", total=1000)
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