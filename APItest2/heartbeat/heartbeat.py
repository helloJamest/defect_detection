#-*- coding:utf-8-*-

import argparse
import requests
import socket
import time
#import computer_info
import json
import orderparam
import ast
import monitor

def main():

    n = 0
    m = 1
    while True:
        n += 1
        print('n=',n)
        time.sleep(1)
        # user_info = {'name': '11111'}
        #print('httptools....')
        headers = {'content-type': 'application/json'}
        hostname, ip_addr, mac_addr = monitor.gethost()
        os_version,number_processes = monitor.sys_info() 
        cpu_name = monitor.CPUinfo()
        cpu_percent = monitor.getCPUstate()
        memory_percent = monitor.getMemorystate()
        disk_percent = monitor.disk()

        com_info = {
                    'id': hostname, 'ip_address': ip_addr, 'mac_address': mac_addr,
                    'os_version': os_version, 'number_processes': number_processes, 'cpu_name': cpu_name,
                    'cpu_percent': cpu_percent, 'memory_percent': memory_percent, 'disk_percent': disk_percent,
                    'pc_state': 'normal', 'temper': '22', 'humidity': '50','light_num':'1',
                    'lights':[{'light_no':'1','light_state':'on'}],'camera_num':'1',
                    'cams':[{'camera_no':'1','camera_state':'normal'}]
                    }

        r = requests.post(r"http://59.110.166.55:8080/iss/heartbeat/pcinfo", data=json.dumps(com_info), headers=headers)#10.108.65.176
        #print('r=',r)
        result = r.json()['result']
        print('result=',result)
        if m==1:

            orderparam.orderparame(result)


if __name__=='__main__':
    main()   
