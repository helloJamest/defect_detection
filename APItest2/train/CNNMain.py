#coding=utf-8

from flask import Flask, request, Response
import json
from flask import jsonify

import httptools

import glob
import os.path
import random
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile
import time
import csv

app = Flask(__name__)

BOTTLENECK_TENSOR_SIZE = 2048
BOTTLENECK_TENSOR_NAME = 'pool_3/_reshape:0'
JPEG_DATA_TENSOR_NAME = 'DecodeJpeg/contents:0'


MODEL_DIR = r'../../data/inception_dec_2015'
MODEL_FILE= 'tensorflow_inception_graph.pb'

CACHE_DIR = '../../data/bottleneck'

#BATCH = 16
INPUT_DATA = '../../data/train_data'
LEARNING_RATE = 0.001
STEPS = 1000
model_path = '../../data/models'
VALIDATION_PERCENTAGE = 10
TEST_PERCENTAGE = 10



def traincNN(INPUT_DATA, LEARNING_RATE, STEPS, model_path, VALIDATION_PERCENTAGE, TEST_PERCENTAGE,BATCH,Optimizer):
    def create_image_lists(testing_percentage, validation_percentage):
        result = {}
        sub_dirs = [x[0] for x in os.walk(INPUT_DATA)]
        print('sub_dirs=', sub_dirs)
        is_root_dir = True
        for sub_dir in sub_dirs:
            print('sub_dir=', sub_dir)
            if is_root_dir:
                is_root_dir = False
                continue

            extensions = ['jpg', 'jpeg']

            file_list = []
            dir_name = os.path.basename(sub_dir)
            print('dir_name=', dir_name)
            for extension in extensions:
                file_glob = os.path.join(INPUT_DATA, dir_name, '*.' + extension)
                file_list.extend(glob.glob(file_glob))
            if not file_list: continue

            label_name = dir_name.lower()
            print('label_name=', label_name)

            # 初始化
            training_images = []
            testing_images = []
            validation_images = []
            # print('file_list=',file_list)
            for file_name in file_list:
                base_name = os.path.basename(file_name)
                # print('basename=',base_name)
                # 随机划分数据
                chance = np.random.randint(100)
                if chance < validation_percentage:
                    validation_images.append(base_name)
                elif chance < (testing_percentage + validation_percentage):
                    testing_images.append(base_name)
                else:
                    training_images.append(base_name)

            result[label_name] = {
                'dir': dir_name,
                'training': training_images,
                'testing': testing_images,
                'validation': validation_images,
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

    def get_or_create_bottleneck(sess, image_lists, label_name, index, category, jpeg_data_tensor, bottleneck_tensor):
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

    def get_random_cached_bottlenecks(sess, n_classes, image_lists, how_many, category, jpeg_data_tensor,
                                      bottleneck_tensor):
        bottlenecks = []
        ground_truths = []
        for _ in range(how_many):
            label_index = random.randrange(n_classes)
            label_name = list(image_lists.keys())[label_index]
            image_index = random.randrange(65536)
            bottleneck = get_or_create_bottleneck(
                sess, image_lists, label_name, image_index, category, jpeg_data_tensor, bottleneck_tensor)
            ground_truth = np.zeros(n_classes, dtype=np.float32)
            ground_truth[label_index] = 1.0
            bottlenecks.append(bottleneck)
            ground_truths.append(ground_truth)

        return bottlenecks, ground_truths

    def get_test_bottlenecks(sess, image_lists, n_classes, jpeg_data_tensor, bottleneck_tensor):
        bottlenecks = []
        ground_truths = []
        testnames = []
        label_name_list = list(image_lists.keys())
        for label_index, label_name in enumerate(label_name_list):
            category = 'testing'
            for index, unused_base_name in enumerate(image_lists[label_name][category]):
                bottleneck = get_or_create_bottleneck(sess, image_lists, label_name, index, category, jpeg_data_tensor,
                                                      bottleneck_tensor)
                ground_truth = np.zeros(n_classes, dtype=np.float32)
                ground_truth[label_index] = 1.0
                testnames.append(unused_base_name)
                bottlenecks.append(bottleneck)
                ground_truths.append(ground_truth)
        return bottlenecks, ground_truths, testnames

    mainstart_time = time.time()
    print('start...', time.asctime(time.localtime(mainstart_time)))
    image_lists = create_image_lists(TEST_PERCENTAGE, VALIDATION_PERCENTAGE)
    name_list = list(image_lists.keys())
    print('list=', name_list)
    n_classes = len(image_lists.keys())
    stime = time.asctime(time.localtime(time.time()))
    '''
    with open('D:\python\workspace\训练日志.txt', 'r') as myFile:
        lines = myFile.readlines()
    with open('D:\python\workspace\训练日志.txt', 'w') as f:
        f.write('训练开始时间:%s\n' % stime)
        f.write('图片种类:%d\n' % n_classes)
        lists = image_lists.keys()
        for i in (lists):
            n = len(image_lists[i]['training'])
            m = len(image_lists[i]['validation'])
            l = len(image_lists[i]['testing'])
            f.write('种类名称:%s，  包含训练图片个数:%d，  验证图片个数:%d,  测试图片个数:%d\n' % (i, n, m, l))
        f.write('训练迭代次数:%d\n' % STEPS)
        f.write('-----------------------------------------------------------------------------------------')
        f.write('\n\n\n\n')
        f.writelines(lines)
    '''
    # 读取已经训练好的Inception-v3模型。
    with gfile.FastGFile(os.path.join(MODEL_DIR, MODEL_FILE), 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    bottleneck_tensor, jpeg_data_tensor = tf.import_graph_def(
        graph_def, return_elements=[BOTTLENECK_TENSOR_NAME, JPEG_DATA_TENSOR_NAME])

    # 定义新的神经网络输入
    bottleneck_input = tf.placeholder(tf.float32, [None, BOTTLENECK_TENSOR_SIZE], name='BottleneckInputPlaceholder')
    ground_truth_input = tf.placeholder(tf.float32, [None, n_classes], name='GroundTruthInput')

    # 定义一层全链接层
    with tf.name_scope('final_training_ops'):
        weights = tf.Variable(tf.truncated_normal([BOTTLENECK_TENSOR_SIZE, n_classes], stddev=0.001),
                              name='weights')
        biases = tf.Variable(tf.zeros([n_classes]), name='biases')
        logits = tf.matmul(bottleneck_input, weights) + biases
        final_tensor = tf.nn.softmax(logits)
        label_names = tf.Variable(name_list, name='label_names')


        # label_names = name_list

    # 定义交叉熵损失函数。
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=ground_truth_input)
    cross_entropy_mean = tf.reduce_mean(cross_entropy)
    GLOBAL_STEP = tf.placeholder(tf.int64, name='GLOBAL_STEP')
    if Optimizer == 'GradientDescentOptimizer':
        train_step = tf.train.GradientDescentOptimizer(LEARNING_RATE).minimize(cross_entropy_mean)
    elif Optimizer == 'AdadeltaOptimizer':
        train_step = tf.train.AdadeltaOptimizer(learning_rate=LEARNING_RATE).minimize(cross_entropy_mean)
    # train_step = tf.train.AdagradOptimizer(learning_rate=LEARNING_RATE).minimize(cross_entropy_mean)
    # train_step = tf.train.AdagradDAOptimizer(learning_rate=LEARNING_RATE,global_step=GLOBAL_STEP).minimize(cross_entropy_mean)
    # train_step = tf.train.MomentumOptimizer(learning_rate=LEARNING_RATE)

    # 计算正确率。
    with tf.name_scope('evaluation'):
        correct_prediction = tf.equal(tf.argmax(final_tensor, 1), tf.argmax(ground_truth_input, 1),
                                      name='correct_prediction')
        evaluation_step = tf.reduce_mean(tf.cast(correct_prediction, tf.float32), name='evaluation_step')
        print('evaluation_step=', evaluation_step)

    saver = tf.train.Saver()


    os.environ["CUDA_VISIBLE_DEVICES"] = '0' #use GPU with ID=0
    config = tf.ConfigProto()
    config.gpu_options.per_process_gpu_memory_fraction = 0.5 # maximun alloc gpu50% of MEM
    config.gpu_options.allow_growth = True #allocate dynamically
    # sess = tf.Session(config = config)


    with tf.Session(config=config) as sess:
        init = tf.global_variables_initializer()
        sess.run(init)

        # 训练过程。
        train_stime = time.time()
        print('trin...', time.asctime(time.localtime(train_stime)))
        start_train_time = time.time()
        lossi = 1
        for i in range(STEPS):
            train_bottlenecks, train_ground_truth = get_random_cached_bottlenecks(
                sess, n_classes, image_lists, BATCH, 'training', jpeg_data_tensor, bottleneck_tensor)
            sess.run(train_step,
                     feed_dict={bottleneck_input: train_bottlenecks, ground_truth_input: train_ground_truth})
            # feed_dict={bottleneck_input: train_bottlenecks, ground_truth_input: train_ground_truth,GLOBAL_STEP:i})
            num = STEPS // 10

            if i % num == 0 or i + 1 == STEPS:
                print('Step %d: Loss=%.1f' % (i, sess.run(cross_entropy_mean,
                                                          feed_dict={bottleneck_input: train_bottlenecks,
                                                                     ground_truth_input: train_ground_truth})))

            #if i % 100 == 0 or i + 1 == STEPS:
                validation_bottlenecks, validation_ground_truth = get_random_cached_bottlenecks(
                    sess, n_classes, image_lists, BATCH, 'validation', jpeg_data_tensor, bottleneck_tensor)
                validation_accuracy = sess.run(evaluation_step, feed_dict={
                    bottleneck_input: validation_bottlenecks, ground_truth_input: validation_ground_truth})
                print('Step %d: Validation accuracy on random sampled %d examples = %.1f%%' %
                      (i, BATCH, validation_accuracy * 100))

                if i == 0:
                    predict_time = 100
                    spend_time = time.time() - start_train_time
                    lossi = sess.run(cross_entropy_mean,
                                                          feed_dict={bottleneck_input: train_bottlenecks,
                                                                     ground_truth_input: train_ground_truth})
                else:
                    spend_time = time.time()-start_train_time
                    predict_time = (spend_time)/i*(STEPS-i)

                info = {'flag':'0','step':str(i),'loss':str(sess.run(cross_entropy_mean,
                                                          feed_dict={bottleneck_input: train_bottlenecks,
                                                                     ground_truth_input: train_ground_truth})/lossi),
                        'train_accuracy':str(validation_accuracy * 100),'spend_time':spend_time,'predict_time':str(predict_time)}
                httptools.tools(info)


            #if i % 50 == 0 or (i + 1) == STEPS:
            if (i + 1) == STEPS:
                checkpoint_path = os.path.join(model_path, 'model.ckpt')
                saver.save(sess, checkpoint_path)
        train_time = time.time() - train_stime
        # 在最后的测试数据上测试正确率。
        start_time = time.time()
        test_bottlenecks, test_ground_truth, testnames = get_test_bottlenecks(
            sess, image_lists, n_classes, jpeg_data_tensor, bottleneck_tensor)
        print('testnames=', testnames)
        fin = sess.run(final_tensor, feed_dict={
            bottleneck_input: test_bottlenecks, ground_truth_input: test_ground_truth
        })
        print('fin=', fin)
        print('truth=', test_ground_truth)
        test_accuracy = sess.run(evaluation_step, feed_dict={
            bottleneck_input: test_bottlenecks, ground_truth_input: test_ground_truth})

        cor = sess.run(correct_prediction, feed_dict={
            bottleneck_input: test_bottlenecks, ground_truth_input: test_ground_truth
        })
        print('cor=', cor)
        for i in range(len(cor)):
            if cor[i] == False:
                print('error image=', testnames[i])

        duration = time.time() - start_time
        print('Images Process Time:', train_stime - mainstart_time)
        print('Train Full Time:', train_time)
        print('Final test accuracy = %.1f%%' % (test_accuracy * 100))
        print('Test Full Time:', duration)

        info = {'flag':'1','accuracy':str(test_accuracy * 100),'train_time':train_time}
        httptools.tools(info)

        #return test_accuracy * 100


@app.route('/traincnn', methods=['POST'])
def son():

    print(request.json)
    data = request.json

    model_path = data['model_path']
    print('traincnn....',model_path)

    input_data = data['input_data']

    test_percentage = float(data['test_percentage'])

    learning_rate = float(data['learning_rate'])

    steps = int(data['steps'])

    validation_percentage = float(data['validation_percentage'])
    batch = int(data['batch'])
    optimizer = data['optimizer']

    print('cnnmain.....')
    traincNN(input_data, learning_rate, steps, model_path, validation_percentage, test_percentage,batch,optimizer)

    result = {'code': 10000}
    return Response(json.dumps(result), mimetype='application/json')
if __name__ == '__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')

#traincNN(INPUT_DATA,LEARNING_RATE,STEPS,model_path,VALIDATION_PERCENTAGE,TEST_PERCENTAGE)

