#-*- coding:utf-8-*-
import requests, json
import base64
from base64 import b64encode
import time
import socket

hostname = socket.gethostname()

def tools(info):
    #user_info = {'name': '11111'}
    print('info=',info)
    headers = {'content-type': 'application/json'}
    r = requests.post("http://59.110.166.55:8080/iss/heartbeat/evaluateinfo", data=json.dumps(info), headers=headers)#10.108.65.176
    print('result=',r.json())
    print('上传信息')
'''
while True:
     info = {'id':'2013-20171028SW','qcount': str(10000),'count':str(11000),'spend_time':str(10000.0)}
     tools(info)
     time.sleep(4)
'''


def image_tools(path,name,category):
    print('tools_path=',path)
    ENCODING = 'utf-8'  # 指定编码形式
    # SCRIPT_NAME, IMAGE_NAME, JSON_NAME = argv    # 获得文件名参数

    # 读取二进制图片，获得原始字节码，注意 'rb'
    with open(path, 'rb') as jpg_file:
        byte_content = jpg_file.read()
    # 把原始字节码编码成 base64 字节码
    base64_bytes = b64encode(byte_content)
    # 将 base64 字节码解码成 utf-8 格式的字符串
    base64_string = base64_bytes.decode(ENCODING)
    # 用字典的形式保存数据
    raw_data = {}
    raw_data['id'] = hostname
    raw_data['category'] = category
    raw_data["name"] = name
    #raw_data['path'] = path
    raw_data["image_base64_string"] = base64_string
    #print('data=',json.dumps(raw_data))

    headers = {'content-type': 'application/json'}
    r = requests.post("http://59.110.166.55:8080/iss/heartbeat/imgupload", data=json.dumps(raw_data), headers=headers)
    print('r=',r)
    try:
        print('result=',r.json())
        print('上传图片')
    except:
        print('服务器错误')

def image_tools0(info):
    path = info['path']
    num = info['num']
    flag = str(info['flag'])
    collect_id = info['collect_id']
    name = info['name']
    print('tools_path=',path)
    ENCODING = 'utf-8'  # 指定编码形式
    # SCRIPT_NAME, IMAGE_NAME, JSON_NAME = argv    # 获得文件名参数

    # 读取二进制图片，获得原始字节码，注意 'rb'
    with open(path, 'rb') as jpg_file:
        byte_content = jpg_file.read()
    # 把原始字节码编码成 base64 字节码
    base64_bytes = b64encode(byte_content)
    # 将 base64 字节码解码成 utf-8 格式的字符串
    base64_string = base64_bytes.decode(ENCODING)
    # 用字典的形式保存数据
    raw_data = {'name':name,'flag':flag,'id':collect_id}
    raw_data["image_base64_string"] = base64_string
    # print('12345456')
    #print('data=',json.dumps(raw_data))

    headers = {'content-type': 'application/json'}
    r = requests.post("http://59.110.166.55:8080/iss/heartbeat/rawimgupload", data=json.dumps(raw_data), headers=headers)
    print('r=',r)
    try:
        print('result=',r.json())
        print('上传图片')
    except:
        print('服务器错误')






def addpc(info):
    print('addpc....')
    headers = {'content-type': 'application/json'}
    r = requests.post("http://59.110.166.55:8080/iss/heartbeat/addpc", data=json.dumps(info), headers=headers)
    try:
        print('result1=',r.json())
        print('增加设备')
    except:
        print('服务器错误...')

#com_info = {'mac':'2013-20171028SW1','lightnum':1,'cameranum':1}
#addpc(com_info)


#headers = {'content-type': 'application/json'}
     # "path": "C:/project/data/test_data/daisy/fac1_workshop1_line1_point1_2013-20171028SW2_1515723777210.jpg",



'''
r = requests.post("http://59.110.166.55:8080/iss/heartbeat/imgupload", data=json.dumps(raw_data), headers=headers)
print('r=',r)
try:
    print('result=', r.json())
except:
    print('服务器错误')
    time.sleep(4)

'''


