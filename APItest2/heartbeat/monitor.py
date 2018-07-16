#!/usr/bin/env python3
#-*- coding:utf-8 -*-


'''
pc信息(ubuntu)
'''

import sys
import os
import time     
import psutil    
import socket
import uuid
import re
from collections import OrderedDict


def gethost():
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    mac_addr = ":".join(re.findall(r".{2}",uuid.uuid1().hex[-12:].upper()))#uuid.uuid1().hex
    if not hostname:
        hostname = 'tegra-ubuntu'
    if not ip_addr:
        ip_addr = "127.0.1.1"
    if not mac_addr:
        mac_addr = "00:04:4B:8D:28:43'"
    return hostname, ip_addr, mac_addr



def sys_info():
    with open('/etc/issue') as fd:
        for line in fd:
            os_version = line.strip().split('\\')[0]
            break
    number_processes = 50
    if not os_version:
            os_version = "Ubuntu 16.04 LTS "
    if not number_processes:
            number_processes = "1"
    return os_version,number_processes



def CPUinfo():
    CPUinfo=OrderedDict()
    procinfo=OrderedDict()

    nprocs = 0
    with open('/proc/cpuinfo') as f:
        for line in f:
            if not line.strip():
                #end of one processor
                CPUinfo['proc%s' % nprocs]=procinfo
                nprocs = nprocs+1
                #Reset
                procinfo=OrderedDict()
            else:
                if len(line.split(':')) == 2:
                    procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
                else:
                    procinfo[line.split(':')[0].strip()] = ''
    cpu_name = CPUinfo[list(CPUinfo.keys())[0]]['model name']
    if not cpu_name:
        cpu_name = 'ARMv8 Processor rev 3 (v8l)'
    return cpu_name



#function of Get CPU State;    
def getCPUstate(interval=1):    
    #return (" CPU: " + str(psutil.cpu_percent(interval)) + "%") 
    return(str(psutil.cpu_percent(interval)))   





def getMemorystate():
    phymem = psutil.virtual_memory()
    memory_percent = "%5s" % (# %6s/%s
        phymem.percent
        #,
        #str(int(phymem.used / 1024 / 1024)) + "M",
        #str(int(phymem.total / 1024 / 1024)) + "M"
    )
    #print(memory_percent)
    return memory_percent




def disk():      
    total = 0  
    used = 0  
    disk_partitions = psutil.disk_partitions(all=False)  
    for i in range(0,len(disk_partitions)):  
        partition = disk_partitions[i][1]  
        total_each = psutil.disk_usage(partition)[0]  
        total = total + total_each  
        used_each = psutil.disk_usage(partition)[1]  
        used = used + used_each  
    disk_u = used/float(total)*100  
    return "%.2f"%disk_u

if __name__=='__main__':
    print("Welcome,current system is",os.name," start to get data...")
    print(gethost())
    print(sys_info())
    print(CPUinfo())
    print(getCPUstate())
    print(getMemorystate())
    print(disk())






       


          

