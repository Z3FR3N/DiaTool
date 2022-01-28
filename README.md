<div style="text-align: center;">
<img src="icon.png" alt="alt text" title="image Title" width="300"/>
</div>

# DiaTool

The aim of this terminal script is to visualize in a compact way all the information regarding the machine in which it's running, to "diagnose" (hence, the name) the hardware. If you have git installed in your system, you can obtain this script simply running:

```bash
git clone  https://github.com/Z3FR3N/DiaTool 
```
To run the script simply type from the terminal:

```bash
python3 DiaTool.py
```

# The Code

To enable **all** the features, make sure to install the "Arping" package from Ubuntu repositories (it's a fairly small package to make ARP requests), you can use the package manager and the terminal of your choice, i daily drive Pop_OS (Ubuntu based) so for me it's:

```bash
sudo apt-get install arping
```
If not installed, Python3:

```bash
sudo apt-get install python3
```
Running from zsh.

Feel free to go [on the python download page](https://www.python.org/downloads/) and [rich documentation](https://rich.readthedocs.io/en/stable/introduction.html#installation) for more informations.

Written in Python (v3.9), makes use of the following **modules**:

- subprocess (pass commands to the CLI)
- concurrent.futures (parallellization for I/O bound operation)
- sys
- rich (framework to display all the infos in a nice way)

On debian based distros:

```bash
sudo pip install rich
```

# Features

This script is capable to display:

- Machine details like CPU(s), RAM, disks usage and volume mounting point
- Print network interfaces, process which are using the network, the public IP of the machine
- Make an ICMP/ARP scan of the subnet
- Ping one or more IP addresses
- Changing DNS of the current session (using **systemd-resolve**)

