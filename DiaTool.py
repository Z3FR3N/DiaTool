import sys # https://docs.python.org/3/library/sys.html#sys.platform
import subprocess # https://docs.python.org/3/library/subprocess.html?highlight=subprocess#module-subprocess
# https://rich.readthedocs.io/en/latest/index.html
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

if sys.platform.startswith('linux'):

#else sys.platform.startswith('win32'):