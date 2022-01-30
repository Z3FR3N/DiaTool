<div style="text-align: center;">
<img src="icon.png" alt="alt text" title="image Title" width="300"/>
</div>

# DiaTool

The aim of this script is to display in a compact way all the information regarding the machine. It's meant to be a tool to "diagnose" (hence the name) the hardware and the network. If you have git installed in your system, you can obtain this script by simply running:

```bash
git clone  https://github.com/Z3FR3N/DiaTool 
```
To run the script simply type from the terminal (from the folder):

```bash
python3 DiaTool.py
```

# The Code

To enable **all** the features, make sure to install the "Arping" package from Ubuntu repositories (it's a fairly small package to make ARP requests). You can use the package manager and the terminal of your choice, I daily drive Pop_OS (Ubuntu based) so for me it's:

```bash
sudo apt-get install arping
```
If not installed, Python3:

```bash
sudo apt-get install python3
```

Written in Python (v3.9), makes use of the following **modules**:

- subprocess (pass commands to the CLI)
- concurrent.futures (parallellization for I/O bound operation)
- sys
- rich (framework to display all the info in a nice way)

Almost all are standard python modules, the only one needed is rich:

```bash
sudo pip install rich
```

Feel free to go on the [python download page](https://www.python.org/downloads/) and [rich documentation](https://rich.readthedocs.io/en/stable/introduction.html#installation) for more information.

# Features

This script is capable of displying:

- CPU(s), RAM, disks usage and volume mounting point.
- Print network interfaces, process which are using the network, public IP
- Make an ICMP/ARP scan of the subnet.
- Ping one or more (up to 10) IP addresses.
- Changing DNS of the current session (using **systemd-resolve**) with a faster one.

