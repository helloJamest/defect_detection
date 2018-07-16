#code=utf-8
import sys
sys.path.append('../evaluate')
sys.path.append('../train')

import re
import multiprocessing

import train_apis
# from train import train_apis
import httptools#evaluate
import evaluate_apis
import evaluates

import Demo3
import os
import time
import ast
import glob
import socket

hostname = socket.gethostname()

model_path = '../../data/models'
input_data = '../../data/test_data'
imgupload = '../../data/imgupload'
train_data = '../../data/train_data'
TEST_PERCENTAGE = 10
LEARNING_RATE = 0.001
STEPS = 2000
VALIDATION_PERCENTAGE = 10
BATCH = 32
Optimizer = 'GradientDescentOptimizer'

qualified_samples_upload = 'no'
degraded_samples_upload = 'yes'

camera_frame_rate = '10'
camera_exposure_time = 1000

fid,rid,lid,eid = '00000003','00000006','00000010',hostname


#
def splitresult(result):
    resultlist = []
    stack = []
    dict = {"]": "[", "}": "{"}
    splitindex = -1
    if result[-1]!='}':result+='}'  #{"flag":4,"fid":"factory1","rid":"room1","lid":"line1","eid":"win-desktop"
    for i,char in enumerate(result):
        if char in dict.values():
            stack.append(char)
        elif char in dict.keys():
            stack.pop()
        if stack == [] and char != ',':
            resultlist.append(result[splitindex+1:i+1])
            splitindex = i + 1
    return resultlist

# result= {"flag":0,"config_info":2,"camera_frame_rate":10,"camera_resolution":"1920*1080","camera_exposure_time":1000,"camera_offset_x":400,"camera_offset_y":200,"camera_id":"2013-20171028SW"},{"flag":0,"config_info":4,"environmentalalarm_id":"2013-20171028SW","temperature_threshold":"0-50","humidity_threshold":"30%-60%","environmentalalarm_light":"on","environmentalalarm_light_colour":"Y","environmentalalarm_sound":"off","environmentalalarm_sound_voice":"1"}


def orderparame(result):
    if not result:
        return
    resultlist = splitresult(result)
    for config_list in resultlist:
        print('config_list=',config_list)
        config(config_list)


def config(config_dic1):
    if not config_dic1:
        return
    #print('asd',config_dic1)
    config_dic = ast.literal_eval(config_dic1)
    flag = config_dic['flag']
    if flag == 0:
        config_info = config_dic['config_info']
        if config_info == 1:
            alarmoutput_id = config_dic['alarmoutput_id']
            alarm_light = config_dic['alarm_light']
            alarm_light_colour = config_dic['alarm_light_colour']
            alarm_sound = config_dic['alarm_sound']
            alarm_sound_voice = config_dic['alarm_sound_voice']

            print('alarmoutput_id',alarmoutput_id)
            print('light:',alarm_light)
            print('light_colour',alarm_light_colour)
            print('sound:',alarm_sound)
            print('sound_voice',alarm_sound_voice)

        if config_info == 2:
            camera_id = config_dic['camera_id']
            global camera_frame_rate
            global camera_exposure_time
            camera_frame_rate = config_dic['camera_frame_rate']#
            camera_resolution = config_dic['camera_resolution']#
            camera_exposure_time = config_dic['camera_exposure_time']#
            camera_offset_x = config_dic['camera_offset_x']
            camera_offset_y = config_dic['camera_offset_y']
            print('camera_id:',camera_id)
            print('camera_frame_rate:',camera_frame_rate)
            print('camera_resolution:',camera_resolution)
            print('camera_exposure_time:',camera_exposure_time)
            print('camera_offset_x:',camera_offset_x)
            print('camera_offset_y:',camera_offset_y)


        if config_info == 3:
            light_id = config_dic['light_id']
            list = config_dic['list']
            for config_dic in list:
                light_id = config_dic['light_id']
                No_of_light = config_dic['no_of_light']
                light_value = config_dic['light_value']
                light = config_dic['light']
                print('light_id:',light_id)
                print('No_of_light:',No_of_light)
                print('light_value:',light_value)
                print('light:',light)

        if config_info == 4:
            environmentalalarm_id = config_dic['environmentalalarm_id']
            temperature_threshold = config_dic['temperature_threshold']
            humidity_threshold = config_dic['humidity_threshold']
            environmentalalarm_light = config_dic['environmentalalarm_light']
            environmentalalarm_light_colour = config_dic['environmentalalarm_light_colour']
            environmentalalarm_sound = config_dic['environmentalalarm_sound']
            environmentalalarm_sound_voice = config_dic['environmentalalarm_sound_voice']
            print('environmentalalarm_id:',environmentalalarm_id)
            print('temperature_threshold',temperature_threshold)
            print('humidity_threshold',humidity_threshold)
            print('environmentalalarm_light',environmentalalarm_light)
            print('environmentalalarm_light_colour',environmentalalarm_light_colour)
            print('environmentalalarm_sound',environmentalalarm_sound)
            print('environmentalalarm_sound_voice',environmentalalarm_sound_voice)


        if config_info == 5:
            global input_data
            #input_data = config_dic['input_data']
            if not (os.path.isdir(input_data)):
                os.makedirs(input_data)
            path_id = config_dic['path_id']
            classification_sample_path = config_dic['classification_sample_path']
            feature_vector_path = config_dic['feature_vector_path']
            print('path_id',path_id)
            print('classification_sample_path',classification_sample_path)
            print('feature_vector_path',feature_vector_path)


        if config_info == 6:
            global qualified_samples_upload
            global degraded_samples_upload

            upload_id = config_dic['upload_id']
            qualified_samples_upload = config_dic['qualified_samples_upload']
            degraded_samples_upload = config_dic['degraded_samples_upload']
            print('upload_id',upload_id)
            print('qualified_samples_upload',qualified_samples_upload)
            print('degraded_samples_upload',degraded_samples_upload)



        if config_info == 7:

            global  model_path
            evaluate_id = config_dic['evaluate_id']
            product_type = config_dic['product_type']
            model_path = config_dic['model_path']
            image_deny_noise = config_dic['image_deny_noise']
            image_segmentation = config_dic['image_segmentation']
            image_enhanced = config_dic['image_enhanced']
            image_size = config_dic['image_size']
            image_color_adjustment = config_dic['image_color_adjustment']
            image_format = config_dic['image_format']
            image_preprocessing_save_path = config_dic['image_preprocessing_save_path']
            print('evaluate_id',evaluate_id)
            print('product_type',product_type)
            print('model_path:',model_path)
            print('image_deny_noise:',image_deny_noise)
            print('image_segmentation',image_segmentation)
            print('image_enhanced',image_enhanced)
            print('image_size',image_size)
            print('image_color_adjustment',image_color_adjustment)
            print('image_format',image_format)
            print('image_preprocessing_save_path',image_preprocessing_save_path)


    if flag == 2:
        #model_path = result['model_path']
        #train_data = result['input_data']
        '''
        TEST_PERCENTAGE = result['TEST_PERCENTAGE']
        LEARNING_RATE = result['LEARNING_RATE']
        STEPS = result['STEPS']
        VALIDATION_PERCENTAGE = result['VALIDATION_PERCENTAGE']
        BATCH = result['BATCH']
        Optimizer = result['Optimizer']
        '''

        LEARNING_RATE = config_dic['learning_rate']
        STEPS = config_dic['steps']
        BATCH = config_dic['batch']
        VALIDATION_PERCENTAGE = config_dic['validation_percentage']
        TEST_PERCENTAGE = config_dic['test_percentage']

        train_apis.train_apisimpl(train_data, LEARNING_RATE, STEPS, model_path, VALIDATION_PERCENTAGE,
                                  TEST_PERCENTAGE, BATCH, Optimizer)


    if flag == 3:
        global fid
        global rid
        global lid
        global eid
        collect_id = config_dic['collect_id']
        collect_images_num = int(config_dic['collect_images_num'])
        collect = int(config_dic['collect'])
        if collect == 0:
            print('stop')
            return

        num = collect_images_num

        # camera_exposure_time

        Demo3.anaoshots(num,fid,rid,lid,eid,camera_frame_rate)#        #Demo3.GrabImage(num, fid, rid, lid, eid, camera_frame_rate,camera_exposure_time)
        #time.sleep(10)#




        sub_dirs = [x[0] for x in os.walk(imgupload)]
        print('dirs:',sub_dirs)
        extensions = ['jpg']
        file_list = []
        # dir_name = os.path.basename(sub_dirs[0])
        # print('dir_name:',dir_name)
        #for extension in extensions:
        file_glob = os.path.join(imgupload, '*.jpg')
        print('file_glob:',file_glob)
        print('extend:',glob.glob(file_glob))
        file_list.extend(glob.glob(file_glob))
        print('file_list',file_list)
        info = {'collect_id':collect_id,'path':'','flag':0,'num':num,'name':''}
        while(collect_images_num>1):
            if file_list:
                file_name = file_list.pop(0)
                info['name'] = os.path.basename(file_name)
                print('name:',info['name'])
                info['num'] = num - collect_images_num + 1
                info['path'] = imgupload+'/'+info['name']
                httptools.image_tools0(info)
                collect_images_num -= 1
                print('num:',collect_images_num)
            print('info=',info)
        info['flag'] = 1
        info['name'] = os.path.basename(file_list.pop(0))
        print('name:', info['name'])
        info['num'] = num - collect_images_num + 1
        info['path'] = imgupload + '/' + info['name']


        httptools.image_tools0(info)
        # print('glob:',glob.glob(file_glob))
        for i in (glob.glob(file_glob)):
            os.remove(i)

    if flag == 1:
        work_id = config_dic['work_id']
        start = config_dic['start']
        pause = config_dic['pause']
        stop = config_dic['stop']
        # start_testing_time = config_dic['start_testing_time']
        # stop_testing_time = config_dic['stop_testing_time']
        # if not model_path:print('')
        # if not input_data:print('')
        # else:
        print('input_data=',input_data)
        model_path = '../../data/models'
        if start == 1:
            with open('../param', 'w') as f:
                f.write('0\n'+str(camera_frame_rate)+'\n'+str(camera_exposure_time*100)+'\n'+fid+'\n'+rid+'\n'+lid+'\n'+eid+'\n'+'-1'+'\n2')
                print('fid,rid,lid,eid = ', fid, rid, lid, eid)
            p = multiprocessing.Process(target=evaluate_apis.evaluate_apisimpl, args=(
                input_data, model_path,qualified_samples_upload,degraded_samples_upload,))
            p.start()
        if pause == 1:
            with open('../param', 'w') as f:
                f.write('1\n'+str(camera_frame_rate)+'\n'+str(camera_exposure_time*100)+'\n'+fid+'\n'+rid+'\n'+lid+'\n'+eid+'\n'+'-1'+'\n2')
        if stop == 1:
            with open('../param', 'w') as f:
                f.write('2\n'+str(camera_frame_rate)+'\n'+str(camera_exposure_time*100)+'\n'+fid+'\n'+rid+'\n'+lid+'\n'+eid+'\n'+'-1'+'\n2')




        #evaluate_apis.evaluate_apisimpl(input_data, model_path, qualified_samples_upload, degraded_samples_upload)



    if flag == 4:

        fid = config_dic['fid']
        rid = config_dic['rid']
        lid = config_dic['lid']
        eid = config_dic['eid']
        print('config:fid,rid,lid,eid = ',fid,rid,lid,eid)


#while True:
    #time.sleep(2)
#result = {'flag':3,'collect_id':'123','collect_images_num':10,}
'''
info = { 'mac':'7c:dd:90:eb:e5:89','lightnum':'1','cameranum':'2','factory':'fact1','rid':'rid1',
'line':'line1','point':'point1','tlimit':'0-50','hlimit':'20-40','cambit':'1280*960','camspeed':'100',
'campkt':'10','cam_x':'0','cam_y':'0','almlight':'0','almvoice':'0','lightpower':'100'}
'''
#config(result)
#httptools.image_tools('C:/project/data/flower_photos/daisy/5547758_eea9edfd54_n.jpg','5547758_eea9edfd54_n.jpg','daisy')
#httptools.addpc(info)
