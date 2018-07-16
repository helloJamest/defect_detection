#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''相机拍摄程序'''

#import cv2
import numpy as np
import time
import os
#from matplotlib import pyplot as plt  
# import sys
# sys.path.append('/home/win/project/APItest2/MvCameraControl_build20161114/demo/64/c/GrabImage/')
# import GrabImageso
import json
import requests


import pygame
import pygame.camera
from pygame.locals import *
import time
import os



def eval_anaoshots():
    # initialize
    pygame.init()
    pygame.camera.init()
    # capture a image
    camera = pygame.camera.Camera("/dev/video0", (640, 480))
    camera.start()
    print("open camera success")

    while (True):

        time.sleep(0.1)
        with open('../param', 'r') as f:
            for i, line in enumerate(f):
                if i == 0: flag = line.strip()#开始暂停标志位
                if i == 1: camera_frame_rate = line.strip()#帧率
                if i == 2: camera_exposure_time = line.strip()#曝光时间
                if i == 3: fid = line.strip()
                if i == 4: rid = line.strip()
                if i == 5: lid = line.strip()
                if i == 6: eid = line.strip()
            print('param1 = ', flag.rstrip())
            print('camera_frame_rate = ', camera_frame_rate)
            separatedtime = 1/float(camera_frame_rate)  # 每隔0.1s读取一帧
            if flag == '1':
                pass
            elif flag == '0':
                
                time.sleep(separatedtime)
                c = 0
                number = 2
                starttime = time.time()

                while True:  # 循环读取视频帧
                    image = camera.get_image()
                    pygame.image.save(image, r'../../data/test_data/'+ os.listdir('../../data/test_data/')[0] + '/' +fid+'_'+rid+'_'+lid+'_'+eid+'_'+eid+'1_'+str(time.time()) + '.jpg')
                    print('save the image')

                    print(time.time() - starttime)
                    c += 1
                    if c >= number:
                        break
                    usetime = time.time() - starttime
                    sleeptime = separatedtime * c - usetime
                    if sleeptime > 0: time.sleep(sleeptime)
            else:
                continue
    print('close')
    camera.stop()







'''
#检测时拍照函数
def eval_anaoshots2():
    vc = cv2.VideoCapture(1)  #笔记本内置摄像头一般为 0          #NOTE:pi 1;PC 0
    if vc.isOpened():  # 判断是否正常打开
        #rval, frame = vc.read()
        print("open camera success")
    else:
        rval = False
        print("read error")

    while (True):
        rval, frame = vc.read()
        time.sleep(0.5)
        with open('../param', 'r') as f:
            for i, line in enumerate(f):
                if i == 0: flag = line.strip()#开始暂停标志位
                if i == 1: camera_frame_rate = line.strip()#帧率
                if i == 2: camera_exposure_time = line.strip()
                if i == 3: fid = line.strip()
                if i == 4: rid = line.strip()
                if i == 5: lid = line.strip()
                if i == 6: eid = line.strip()
            print('param1 = ', flag.rstrip())
            print('camera_frame_rate = ', camera_frame_rate)
            if flag == '1':
                pass
            elif flag == '0':

        # with open('../param', 'r') as f:
        #     param = f.read()
        #     print('len(param)=',len(param))
        #     print('param = ',param[0])
        #     if param[0] == '1':
        #         pass
        #     elif param[0] == '0':
                separatedtime = 1/int(camera_frame_rate)  # 每隔0.1s读取一帧
                c = 0
                number = 2
                starttime = time.time()

                while rval:  # 循环读取视频帧
                    #rval, frame = vc.read()
                    print(time.time() - starttime)
                    cv2.imwrite(r'../../data/test_data/'+ os.listdir('../../data/test_data/')[0] + '/' +fid+'_'+rid+'_'+lid+'_'+eid+'_'+eid+'1_'+str(time.time()) + '.jpg', frame)  # 存储为图像
                    c += 1
                    if c >= number:
                        break
                    usetime = time.time() - starttime
                    sleeptime = separatedtime * c - usetime
                    if sleeptime > 0: time.sleep(sleeptime)
            else:
                continue
'''


#控制工业相机采集图片
def GrabImage(number,fid,rid,lid,eid,camera_frame_rate,camera_exposure_time):
    # GrabImageso.GrabImage(number,fid,rid,lid,eid,camera_frame_rate)
    '''
    user_info = {'number': number,'fid':fid,'rid':rid,'lid':lid,
                 'eid':eid,'camera_frame_rate':camera_frame_rate,'camera_exposure_time':camera_exposure_time}
    headers = {'content-type': 'application/json'}
    print('train_apisimpl.....')
    r = requests.post("http://127.0.0.1:3000/GrabImage", data=json.dumps(user_info), headers=headers)
    print('train_apisimpl.....')
    '''
    with open('../param', 'w') as f:
        f.write('0\n' + str(camera_frame_rate) + '\n' + str(
            camera_exposure_time * 100) + '\n' + fid + '\n' + rid + '\n' + lid + '\n' + eid+'\n'+str(number)+'\n1')#1采集2检测


        print('fid,rid,lid,eid = ', fid, rid, lid, eid)

    # import ctypes
    #
    # fid = ctypes.c_char_p(str.encode(fid))# 将String转成wchar_t*
    # rid = ctypes.c_char_p(str.encode(rid))
    # lid = ctypes.c_char_p(str.encode(lid))
    # eid = ctypes.c_char_p(str.encode(eid))
    #
    # camera_frame_rate = ctypes.c_float(float(camera_frame_rate))
    #
    # # fid = fid.ctypes.data_as(ctypes.c_char_p)
    # # rid = rid.ctypes.data_as(ctypes.c_char_p)  # 将String转成wchar_t*
    # # lid = lid.ctypes.data_as(ctypes.c_char_p)  # 将String转成wchar_t*
    # # eid = eid.ctypes.data_as(ctypes.c_char_p)  # 将String转成wchar_t*
    # # camera_frame_rate = int(camera_frame_rate)
    #
    # # ctypes.CDLL('/home/win/project/APItest2/MvCameraControl_build20161114/lib/64/libMVGigEVisionSDK.so', mode=ctypes.RTLD_GLOBAL)
    # # ctypes.CDLL('/home/win/project/APItest2/MvCameraControl_build20161114/lib/64/libMvCameraControl.so', mode=ctypes.RTLD_GLOBAL)
    # #
    # # ctypes.CDLL('/home/win/project/APItest2/MvCameraControl_build20161114/demo/64/c/GrabImage/GrabImage.so', mode=ctypes.RTLD_GLOBAL)
    # so = ctypes.cdll.LoadLibrary
    #
    #
    #
    #
    # lib = so("./GrabImage.so") #调用C函数
    # lib.mainee(number,fid,rid,lid,eid,camera_frame_rate)



#采集图片函数  无法修改分辨率/曝光时间;
def anaoshots(number,fid,rid,lid,eid,camera_frame_rate):
    # initialize
    pygame.init()
    pygame.camera.init()
    # capture a image
    camera = pygame.camera.Camera("/dev/video0", (640, 480))
    camera.start()
    print("open camera success")
    c = 1
    starttime = time.time()
    while c<=number:  # 循环读取视频帧
        image = camera.get_image()
        pygame.image.save(image, r'../../data/test_data/'+ os.listdir('../../data/test_data/')[0] + '/' +fid+'_'+rid+'_'+lid+'_'+eid+'_'+eid+'1_'+str(time.time()) + '.jpg')
        print('save the image',c)
        print(time.time() - starttime)
        c += 1
        usetime = time.time() - starttime

        # sleeptime = separatedtime * c - usetime
        #if sleeptime > 0: time.sleep(sleeptime)
    print('采集结束')
    camera.stop()


'''
#采集图片函数  无法修改分辨率/曝光时间 opencv
def anaoshots(number,fid,rid,lid,eid,camera_frame_rate):
    vc = cv2.VideoCapture(0)  #笔记本内置摄像头一般为 0#pi 1;PC 0
    c = 0
    if vc.isOpened(): #判断是否正常打开
        rval,frame = vc.read()
        print("read ok")
    else:
        rval = False
        print("read error")

    # vc.set(cv2.cv.CV_ZAP_PROP_FRAME_WIDTH,1280)

    #number = 400000
    starttime = time.time()
    camera_frame_rate = int(camera_frame_rate)
    separatedtime = 1/camera_frame_rate # 每隔*s读取一帧

    while rval:   #循环读取视频帧
        #rval, frame = vc.read()
        print(time.time()-starttime)
        cv2.imwrite(r'../../data/imgupload/'+fid+'_'+rid+'_'+lid+'_'+eid+'_'+eid+'1_'+str(time.time()) + '.jpg',frame) #存储为图像  +'00000003_00000006_00000010_win-desktop_win-desktop1_'
        
        c += 1
        if c>= number:
            break
        usetime = time.time()-starttime
        sleeptime = separatedtime*c-usetime
        print('sleeptime:',sleeptime)
        if sleeptime>0:time.sleep(sleeptime)
        #cv2.waitKey(1)
	#print("Input 'q' to quit!")	
'''



if __name__=='__main__':
    #anaoshots(5,'fid','rid','lid','eid',10)
    # GrabImage(5,'rer','rerew','lid','eid',10,1000)
    eval_anaoshots()


