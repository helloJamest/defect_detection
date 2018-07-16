import requests, json

def tools(info):
    print('info =',info)
    print('httptools....')
    headers = {'content-type': 'application/json'}
    r = requests.post("http://59.110.166.55:8080/iss/heartbeat/traininfo", data=json.dumps(info), headers=headers)#10.108.65.176
    # r = requests.post("http://60.208.116.146:58080/heartbeat/traindata", data=json.dumps(info), headers=headers)
    try:
        print('result:',r.json())
    except:
        print('未连接')
