'''
检测配置
'''
import os
import evaluate
import urllib3
import flask
from flask import request
from flask import jsonify
import evaluate_apis

server = flask.Flask(__name__)

qualified_samples_upload ='no'
degraded_samples_upload = 'yes'
model_path = '../../data/models'
input_data = '../../data/test_data'

@server.route('/alarmoutput',methods=['GET','POST'])
def alarm_outputPost():
    #判断接口的请求方式是GET还是POST
    if request.method == 'POST':
        try:
            id = request.form['id']
            light = request.form['light']
            light_colour = request.form['light_colour']
            sound = request.form['sound']
            sound_voice = request.form['sound_voice']
            print('id:',id)
            print('light:',light)
            print('light_colour',light_colour)
            print('sound:',sound)
            print('sound_voice',sound_voice)
            return jsonify({'success':'true','code':'10000','msg':'ok','result':''})

        except:
            #pass
            return jsonify({'success':'false','code':'10005','msg':'server error','result':''})

@server.route('/camera', methods=['GET', 'POST'])
def cameraPost():
    # 判断接口的请求方式是GET还是POST
    if request.method == 'POST':
        try:
            id = request.form['id']
            camera_frame_rate = request.form['camera_frame_rate']
            camera_resolution = request.form['camera_resolution']
            camera_exposure_time = request.form['camera_exposure_time']
            camera_offset_x = request.form['camera_offset_x']
            camera_offset_y = request.form['camera_offset_y']
            print('id:',id)
            print('camera_frame_rate:',camera_frame_rate)
            print('camera_resolution:',camera_resolution)
            print('camera_exposure_time:',camera_exposure_time)
            print('camera_offset_x:',camera_offset_x)
            print('camera_offset_y:',camera_offset_y)
            return jsonify({'success':'true','code':'10000','msg':'ok','result':''})

        except:
            # pass
            return jsonify({'success':'false','code':'10005','msg':'server error','result':''})

@server.route('/light', methods=['GET', 'POST'])
def lightPost():
    # 判断接口的请求方式是GET还是POST
    if request.method == 'POST':
        try:
            id = request.form['id']
            No = request.form['no']
            light_value = request.form['light_value']
            light = request.form['light']
            print('id:',id)
            print('No:',No)
            print('light_value:',light_value)
            print('light:',light)
            return jsonify({'success':'true','code':'10000','msg':'ok','result':''})
        except:
            return jsonify({'success':'false','code':'10005','msg':'server error','result':''})

@server.route('/environmentalalarm', methods=['GET', 'POST'])
def environmental_alarmPost():
    # 判断接口的请求方式是GET还是POST
    if request.method == 'POST':
        try:
            id = request.form['id']
            temperature_threshold = request.form['temperature_threshold']
            humidity_threshold = request.form['humidity_threshold']
            light = request.form['light']
            light_colour = request.form['light_colour']
            sound = request.form['sound']
            sound_voice = request.form['sound_voice']
            return jsonify({'success':'true','code':'10000','msg':'ok','result':''})

        except:
            # pass
            return jsonify({'success':'false','code':'10005','msg':'server error','result':''})

@server.route('/evaluate',methods=['GET','POST'])
def registerPost():
    #判断接口的请求方式是GET还是POST
    if request.method == 'POST':
        try:

            global model_path

            model_path = request.form['model_path']
            print('qualified_samples_upload=',qualified_samples_upload)
            print('degraded_samples_upload=',degraded_samples_upload)

            return jsonify({'success':'true','code':'10000','msg':'ok','result':''})

        except:
            #pass
            return jsonify({'success':'false','code':'10005','msg':'server error','result':''})

@server.route('/upload',methods=['GET','POST'])
def registeruploadPost():
    #判断接口的请求方式是GET还是POST
    if request.method == 'POST':
        try:
            global qualified_samples_upload
            global degraded_samples_upload
            qualified_samples_upload = request.form['qualified_samples_upload']
            degraded_samples_upload =  request.form['degraded_samples_upload']

            return jsonify({'success':'true','code':'10000','msg':'ok','result':''})

        except:
            #pass
            return jsonify({'success':'false','code':'10005','msg':'server error','result':''})

@server.route('/path',methods=['GET','POST'])
def pathPost():
    #判断接口的请求方式是GET还是POST
    if request.method == 'POST':
        try:
            global input_data

            input_data = request.form['input_data']
            if not (os.path.isdir(input_data)):
                os.makedirs(input_data)


            return jsonify({'success':'true','code':'10000','msg':'ok','result':''})

        except:
            #pass
            return jsonify({'success':'false','code':'10005','msg':'server error','result':''})

@server.route('/work', methods=['GET', 'POST'])
def workPost():
    # 判断接口的请求方式是GET还是POST
    if request.method == 'POST':
        try:
            id = request.form['id']
            start = request.form['start']
            pause = request.form['pause']
            stop = request.form['stop']
            start_testing_time = request.form['start_testing_time']
            stop_testing_time = request.form['stop_testing_time']
            evaluate_apis.evaluate_apisimpl(input_data, model_path, qualified_samples_upload, degraded_samples_upload)
            return jsonify({'success':'true','code':'10000','msg':'ok','result':''})

        except:
            # pass
            return jsonify({'success':'false','code':'10005','msg':'server error','result':''})

@server.route('/screen', methods=['GET', 'POST'])
def screenPost():
    # 判断接口的请求方式是GET还是POST
    if request.method == 'POST':
        try:
            id = request.form['id']
            sleep = request.form['sleep']
            brightness = request.form['brightness']
            password = request.form['password']
            print('id:', id)
            print('sleep:', sleep)
            print('brightness:',brightness)
            print('password:',password)
            return jsonify({'success':'true','code':'10000','msg':'ok','result':''})

        except:
            # pass
            return jsonify({'success':'false','code':'10005','msg':'server error','result':''})

if __name__ == '__main__':
    server.run(debug=True,port=8080,host='0.0.0.0')


