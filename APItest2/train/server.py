from flask import Flask, request, Response
import json
from flask import jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/json', methods=['POST'])
def my_json():
    #print(request.headers)
    print(request.json)
    #rt = {'info': 'hello ' + request.json['name']}
    #print('name=',rt)
    result = {'code':10000}
    return Response(json.dumps(result),  mimetype='application/json')

@app.route('/iss/heartbeat/traininfo', methods=['POST'])
def _json():
    data = request.json
    flag = data['flag']
    print('flag=',flag)
    if (flag == '0'):
        step = data['step']
        loss = data['loss']
        print('step:', step)
        print('loss:', loss)
        predict_time = data['predict_time']
        print('predict_time:'+str(predict_time)+'s')
        spend_time = data['spend_time']
        train_accuracy = data['train_accuracy']
        print('spend_time:',spend_time)
        print('train_accuracy',train_accuracy)
    else:
        accuracy = data['accuracy']
        print('accuracy:', accuracy)
        train_time = data['train_time']
        print('train_time',train_time)


    result = {'code':10000}
    return Response(json.dumps(result),  mimetype='application/json')

@app.route('/iss/heartbeat/pcinfo', methods=['POST'])
def son():
    data = request.json
    id = data['id']
    print('id=',id)
    print("json=",data)
    result = {'code':10000,'model_path':'C:\project\data\models','input_data':'C:/project/data/flower_photos','flag':2}
    return Response(json.dumps(result),  mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True,port=8080,host='0.0.0.0')
    #app.run(debug=True)
