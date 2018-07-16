#coding=utf-8

'''
检测需要调用的函数
'''

import glob
import tensorflow as tf
import os.path
import random
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile
import time
#import Fileoperation

BOTTLENECK_TENSOR_SIZE = 2048
BOTTLENECK_TENSOR_NAME = 'pool_3/_reshape:0'
JPEG_DATA_TENSOR_NAME = 'DecodeJpeg/contents:0'

MODEL_DIR = '../../data/inception_dec_2015'
MODEL_FILE= 'tensorflow_inception_graph.pb'
CACHE_DIR = '../../data/bottleneck'
BATCH = 100

def create_image_lists(INPUT_DATA):
    result = {}
    # print('2345')
    sub_dirs = [x[0] for x in os.walk(INPUT_DATA)]
    is_root_dir = True
    for sub_dir in sub_dirs:
        if is_root_dir:
            is_root_dir = False
            continue
        # 打印出文件夹（种类）路径

        extensions = ['jpg']
        file_list = []
        dir_name = os.path.basename(sub_dir)
        # 打印出文件夹（种类）名字
        #print('dir_name=', dir_name)
        for extension in extensions:
            file_glob = os.path.join(INPUT_DATA, dir_name, '*.' + extension)
            print('file_glob=', glob.glob(file_glob))
            file_list.append(glob.glob(file_glob)[0])#
            print('file_glob[0]=', glob.glob(file_glob)[0])
            #print('file_list=', file_list)
        # if not file_list: continue
        print('file_list:',file_list)
        label_name = dir_name.lower()
        #print('label_name=', label_name)

        # 初始化
        testing_images = []
        for file_name in file_list:
            base_name = os.path.basename(file_name)
            # 打印出图片名字
            # print('base_name=',base_name)
            testing_images.append(base_name)
        result[label_name] = {
            'dir': dir_name,
            'testing': testing_images,
        }

    return result

def get_image_path(image_lists, image_dir, label_name, index, category):
    label_lists = image_lists[label_name]
    category_list = label_lists[category]
    mod_index = index % len(category_list)
    base_name = category_list[mod_index]
    sub_dir = label_lists['dir']
    full_path = os.path.join(image_dir, sub_dir, base_name)
    return full_path

def get_bottleneck_path(image_lists, label_name, index, category):
    return get_image_path(image_lists, CACHE_DIR, label_name, index, category) + '.txt'

def run_bottleneck_on_image(sess, image_data, image_data_tensor, bottleneck_tensor):
    bottleneck_values = sess.run(bottleneck_tensor, {image_data_tensor: image_data})
    bottleneck_values = np.squeeze(bottleneck_values)
    return bottleneck_values

def get_or_create_bottleneck(sess, image_lists, label_name, index, category, jpeg_data_tensor, bottleneck_tensor, INPUT_DATA):
    label_lists = image_lists[label_name]
    sub_dir = label_lists['dir']
    sub_dir_path = os.path.join(CACHE_DIR, sub_dir)
    if not os.path.exists(sub_dir_path): os.makedirs(sub_dir_path)
    bottleneck_path = get_bottleneck_path(image_lists, label_name, index, category)
    if not os.path.exists(bottleneck_path):
        image_path = get_image_path(image_lists, INPUT_DATA, label_name, index, category)
        image_data = gfile.FastGFile(image_path, 'rb').read()
        bottleneck_values = run_bottleneck_on_image(sess, image_data, jpeg_data_tensor, bottleneck_tensor)
        bottleneck_string = ','.join(str(x) for x in bottleneck_values)
        with open(bottleneck_path, 'w') as bottleneck_file:
            bottleneck_file.write(bottleneck_string)
    else:
        with open(bottleneck_path, 'r') as bottleneck_file:
            bottleneck_string = bottleneck_file.read()
        bottleneck_values = [float(x) for x in bottleneck_string.split(',')]
    return bottleneck_values


def get_test_bottlenecks(sess, image_lists, n_classes, jpeg_data_tensor, bottleneck_tensor, label_names, INPUT_DATA):
    bottlenecks = []
    ground_truths = []
    testnames = []
    labelname = []
    label_name_list = list(image_lists.keys())
    for label_index, label_name in enumerate(label_name_list):
        category = 'testing'
        # print('fdsfsdf')
        labelname.append(label_name)
        for index, unused_base_name in enumerate(image_lists[label_name][category]):
            bottleneck = get_or_create_bottleneck(sess, image_lists, label_name, index, category, jpeg_data_tensor,
                                                  bottleneck_tensor, INPUT_DATA)
            ground_truth = np.zeros(n_classes, dtype=np.float32)
            if label_name in label_names:
                ground_truth[label_names.index(label_name)] = 1.0
            testnames.append(unused_base_name)
            bottlenecks.append(bottleneck)
            ground_truths.append(ground_truth)
    return bottlenecks, ground_truths, testnames, labelname