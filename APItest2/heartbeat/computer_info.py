# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
pc信息(windows)
'''

import wmi
import platform
import time
import psutil
import socket
import uuid

def get_host():
    hostname = socket.getfqdn(socket.gethostname())#获取本机电脑名
    ip_addr = socket.gethostbyname(hostname)#获取本机ip
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    mac_addr =  (":".join([mac[e:e + 2] for e in range(0, 11, 2)]))

    #print(hostname)
    #print(ip_addr)
    #print(mac_addr)
    if not hostname:
        hostname = '2013-20171028SW'
    if not ip_addr:
        ip_addr = "192.168.1.8"
    if not mac_addr:
        mac_addr = "00:19:0f:30:7f:e7"
    return hostname,ip_addr,mac_addr

def sys_version():
    c = wmi.WMI()
    # 获取操作系统版本
    for sys in c.Win32_OperatingSystem():
        #print("Version:%s" % sys.Caption)

        # print(sys.OSArchitecture.encode("UTF8"))  # 系统是32位还是64位的
        #print(sys.NumberOfProcesses)  # 当前系统运行的进程总数
        os_version, number_processes = sys.Caption,sys.NumberOfProcesses
        if not os_version:
            os_version = "MicrosoftWindows7旗舰版"
        if not number_processes:
            number_processes = "1"
        return os_version, number_processes



def cpu_mem():
    c = wmi.WMI()
    # CPU类型和内存
    for processor in c.Win32_Processor():
        pass
           #print("Process Name: %s" % processor.Name.strip())
    # for Memory in c.Win32_PhysicalMemory():
    #     print("Memory Capacity: %.fMB" % (int(Memory.Capacity) / 1048576))
    cpu_name = processor.Name.strip()
    if not cpu_name:
        cpu_name = "Intel(R)Core(TM)i7-4770CPU@3.40GHz"
    return cpu_name


def cpu_use():
    # 5s取一次CPU的使用率
    c = wmi.WMI()
    while True:
        for cpu in c.Win32_Processor():
            timestamp = time.strftime('%a, %d %b %Y %H:%M:%S', time.localtime())
            #print('%s | Utilization: %s: %d %%' % (timestamp, cpu.DeviceID, cpu.LoadPercentage))
            return cpu.LoadPercentage
            time.sleep(5)


#获取内存使用率
def getMemorystate():
    phymem = psutil.virtual_memory()
    memory_percent = "%5s" % (# %6s/%s
        phymem.percent
        #,
        #str(int(phymem.used / 1024 / 1024)) + "M",
        #str(int(phymem.total / 1024 / 1024)) + "M"
    )
    #print(memory_percent)
    return  memory_percent


def disk():
    c = wmi.WMI()
    '''
    # 获取硬盘分区
    for physical_disk in c.Win32_DiskDrive():
        for partition in physical_disk.associators("Win32_DiskDriveToDiskPartition"):
            for logical_disk in partition.associators("Win32_LogicalDiskToPartition"):
                print(physical_disk.Caption.encode("UTF8"), partition.Caption.encode("UTF8"), logical_disk.Caption)
'''
                # 获取硬盘使用百分情况
    for disk in c.Win32_LogicalDisk(DriveType=3):
        #print(disk.Caption, "%0.2f%% free" % (100.0 * (float)(disk.FreeSpace) / (float)(disk.Size)))
        return 100.0 * (float)(disk.FreeSpace) / (float)(disk.Size)



def main():
    get_host()
    sys_version()
    cpu_mem()
    getMemorystate()
    disk()
    cpu_use()


if __name__ == '__main__':
    main()
    # print(platform.system())
    # print(platform.release())
    # print(platform.version())
    # print(platform.platform())
    # print(platform.machine())