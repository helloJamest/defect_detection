from flask import Flask, request, Response
import json
from flask import jsonify
import base64
import os

app = Flask(__name__)

@app.route('/iss/heartbeat/pcinfo', methods=['POST'])
def _json():
    data = request.json
    print(data)

    # qcount = data['qcount']
    # print('qcount:', qcount)
    #
    # count = data['count']
    # spend_time = data['spend_time']
    # print('count:', count)
    # print('spend_time:', spend_time)

    result = {'code':10000}
    return Response(json.dumps(result),  mimetype='application/json')


@app.route('/iss/heartbeat/addpc', methods=['POST'])
def my_test_json():
    #print(request.headers)
    data = request.json
    name = data['name']
    print('name:',name)


    result = {'code':10000}
    return Response(json.dumps(result),  mimetype='application/json')









@app.route('/imagedata', methods=['POST'])
def my_json():
    #print(request.headers)
    data = request.json
    name = data['name']
    flag = data['flag']
    print('name:',name)
    print('flag:',flag)
    base_name = os.path.basename(name)
    print('base_name=',base_name)
    img_data = data['image_base64_string']
    imgdata = base64.b64decode(img_data)
    file = open((os.path.join('C:\project\image_save',base_name)),'wb')
    file.write(imgdata)

    result = {'code':10000}
    return Response(json.dumps(result),  mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True,port=8080,host='0.0.0.0')
    #app.run(debug=True)