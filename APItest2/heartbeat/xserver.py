#coding:utf8
import socket
import time
import os
import threading
import argparse

MAX_BYTES = 1024
is_alive = 0

def server(host,port,delay):
    if not isinstance(host,str):
        raise KeyError("The host must be a string like \'127.0.0.1\'")
    if not isinstance(port,int):
        raise KeyError('The port must be a integer')
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((host,port))

    def recv():
        global is_alive
        while True:
            #print('test')
            data,addr = sock.recvfrom(MAX_BYTES)
            print(data.decode())
            print(addr)

            is_alive += 1
            if is_alive >= 10000:
                is_alive = 0
    client = threading.Thread(target=recv)
    client.setDaemon(True)
    client.start()
    IS_ALIVE = True
    while IS_ALIVE:
        before = is_alive
        time.sleep(delay)
        if before is is_alive:
            result = os.popen('python test.py')
            print(result)
            IS_ALIVE = False
    sock.close()

def main():
    #server('0.0.0.0', 5000, 5)
    parse = argparse.ArgumentParser(description='Listen to a port and excute a file')
    parse.add_argument('-H',nargs='?',default='127.0.0.1',const='127.0.0.1')
    parse.add_argument('-P',nargs='?',default=58080,const=58080,type=int)
    parse.add_argument('-D',nargs='?',default=15,const=15)
    result = parse.parse_args()
    print(result.H,result.P,result.D)
    server(result.H,result.P,result.D)


print(int('15.00'.split('.')[0]))

# if __name__=='__main__':
#     main()
# for i in os.listdir('/home/win/project/data/test_data/open'):
#     os.remove('/home/win/project/data/test_data/open' + '/' + i)
    # for i,line in enumerate(f):
    #     if i == 0:param1 = line.strip()
    #     if i == 1:param2 = line.strip()
    #     if i == 2:fid = line.strip()
    #     if i == 3: rid = line.strip()
    #     if i == 4: lid = line.strip()
    #     if i == 5: eid = line.strip()
    #
    #
    # print('param1 = ',param1.rstrip())
    # print('param2 = ',param2)
    # print(fid,rid,lid,eid)
    # param = f.readline()
    # print('len(param)=', len(param))
    # print('param = ', param[0])
    # param2 = f.readline(2)
    # print('param = ', param)
