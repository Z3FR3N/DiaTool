import sys # https://docs.python.org/3/library/sys.html#sys.platform
import subprocess # https://docs.python.org/3/library/subprocess.html?highlight=subprocess#module-subprocess
# https://rich.readthedocs.io/en/latest/index.html
from rich import color, print 
from rich import pretty
from rich import inspect #display methods linked to any object
from rich import progress_bar
from rich.tree import Tree
from rich.console import Console
import pyfiglet

console = Console()

def cmd_to_list(grep_param, cmd): #useful to change and manipolate the output
    if (type(grep_param) == str) and (type(cmd) == str):
        command = subprocess.run(cmd, capture_output=True)  
        cmd_list = subprocess.run(['grep', grep_param], inpSut=command.stdout, capture_output=True).stdout.decode().split()
        return list(cmd_list)
    else:
        print('input non valido') #debug reason

def cmd_to_string(cmd): #useful to immediately print the output onto a string to display it
    command = subprocess.run(cmd, capture_output=True).stdout.decode()
    return str(command)

def run(cmd): #useful for running a single command, with no interest of the output
    command = subprocess.run(cmd)

def retrieve_os(): #retrieve information about the platform we are in
    if sys.platform.startswith('linux'):
        os = "We found ourselves in a Linux-based system :penguin: \n\nHere the details:\n"
        return (os)
    if sys.platform.startswith('win32'):
        os = "We found ourselves in a Windows-based system \U0001fa9f \n\nHere the details:\n"
        return (os)
    else:
        os = (" but i can't detect the os we are in, so i'm basically useless....\U0001f480")
        return (os)
print("\n")

logo = pyfiglet.figlet_format("D i a T o o l", font = "3-d") #just a nice logo
print(logo)

console.print("\n[bold yellow]Welcome[/bold yellow], this is a simple script to retrieve information and do simple stuff with the network.", retrieve_os())