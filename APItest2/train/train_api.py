#coding=utf-8
import urllib3
import flask
from flask import request
from flask import jsonify
import train_apis
import CNNMain

server = flask.Flask(__name__)
@server.route('/train',methods=['GET','POST'])
def registerPost():
    #判断接口的请求方式是GET还是POST
    if request.method == 'POST':
        try:
            # 获取请求参数是json格式，返回结果是字典
            # username = request.form.get('username')
            # 目前知道两种获取参数方法
            # pwd = request.form['pwd']
            # confirmpwd = request.form['pwd']

            model_path = request.form['model_path']
            print('model_path:',model_path)
            input_data = request.form['input_data']
            TEST_PERCENTAGE = int(request.form['test_percentage'])
            LEARNING_RATE = float(request.form['learning_rate'])
            STEPS = int(request.form['steps'])
            VALIDATION_PERCENTAGE = int(request.form['validation_percentage'])
            BATCH = int(request.form['batch'])
            Optimizer = request.form['optimizer']
            print('开始训练...')
            #test_accuracy = CNNMain.traincNN(input_data, LEARNING_RATE, STEPS, model_path, VALIDATION_PERCENTAGE,
            #                                 TEST_PERCENTAGE)
            train_apis.train_apisimpl(input_data, LEARNING_RATE, STEPS, model_path, VALIDATION_PERCENTAGE,
                                           TEST_PERCENTAGE,BATCH,Optimizer)
            return jsonify({'success':'true','code': 10000, 'msg': 'ok','result':'train over'})

        except:
            #pass
            return jsonify({'success':'false',"code":10005,"meg":"服务器异常",'result':''})




if __name__ == '__main__':
    server.run(debug=True,port=8080,host='0.0.0.0')