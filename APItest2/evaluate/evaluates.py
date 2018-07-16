#coding=utf-8
'''

调用检测
检测需要开启

'''
import sys
sys.path.append(r'../evaluate')
import glob
import os.path
import random
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile
import time
#import Fileoperation
import evalu2,httptools
import shutil
from flask import Flask, request, Response
import json
from flask import jsonify
#import httptools
import os
import glob
import os.path
import random
import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile
import time
import multiprocessing

app = Flask(__name__)

BOTTLENECK_TENSOR_SIZE = 2048
BOTTLENECK_TENSOR_NAME = 'pool_3/_reshape:0'
JPEG_DATA_TENSOR_NAME = 'DecodeJpeg/contents:0'

MODEL_DIR = '../../data/inception_dec_2015'
MODEL_FILE= 'tensorflow_inception_graph.pb'



def evalu(INPUT_DATA, model_path, upload_flag):

    print('start evaluate.......')
    with gfile.FastGFile(os.path.join(MODEL_DIR, MODEL_FILE), 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
    print('reading model.......')
    starttime = time.time()
    bottleneck_tensor, jpeg_data_tensor = tf.import_graph_def(
        graph_def, return_elements=[BOTTLENECK_TENSOR_NAME, JPEG_DATA_TENSOR_NAME])
    print('reading success:',time.time()-starttime)



    # config = tf.ConfigProto(allow_soft_placement=True)
    #
    # # 最多占gpu资源的70%
    # gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.7)
    #
    # # 开始不会给tensorflow全部gpu资源 而是按需增加
    # config.gpu_options.allow_growth = True

    # import tensorflow as tf

    #os.environ["CUDA_VISIBLE_DEVICES"] = '0' #use GPU with ID=0
    #config = tf.ConfigProto()
    #config.gpu_options.per_process_gpu_memory_fraction = 0.5 # maximun alloc gpu50% of MEM
    #config.gpu_options.allow_growth = True #allocate dynamically
   




    with tf.Session() as sess:#config=config
        # model_path = '../../data/models'
        saver = tf.train.import_meta_graph(model_path+'/model.ckpt.meta')
        print('reading success1:',time.time()-starttime)
        saver.restore(sess, tf.train.latest_checkpoint(model_path))
        print('reading success2:',time.time()-starttime)
        graph = tf.get_default_graph()
        print('../../data/models1')
        weights1 = graph.get_tensor_by_name('final_training_ops/weights:0')
        biases1 = graph.get_tensor_by_name('final_training_ops/biases:0')
        label_names = graph.get_tensor_by_name('final_training_ops/label_names:0')
        print('../../data/models2')
        weights1 = weights1.eval()
        biases1 = biases1.eval()
        laname = sess.run(label_names).tolist()
        lanames = []
        print('../../data/models3')
        for st in laname:
            s = str(st)
            s = s[2:len(s) - 1]
            lanames.append(s)
        n = len(lanames)
        count = 0
        qcount = 0
        print('0 n=',count)
        start_evaulate_time = time.time()
        #with open('/home/win/project/APItest2/param', 'r') as f:
        while (True):
            #print('f.read()=',f.read()[0])
            time.sleep(0.08)#!!!!   time.sleep(1)
            with open('../param', 'r') as f:
            #while(True):
                num = 0
                param = f.read()
                #print('len(param)=',len(param))
                #print('param = ',param[0])
                if param[0] == '1':
                    pass
                elif param[0] == '0':
                    try:
                        dirct = INPUT_DATA +'/'+ os.listdir(INPUT_DATA)[0]
                        #print('dirct:',dirct)
                        if (os.listdir(dirct)):

                            print('input_data=',INPUT_DATA)
                            image_lists = evalu2.create_image_lists(INPUT_DATA)
                            normal_name = list(image_lists.keys())[0] #正常图片分类的名称，即test_data目录下文件夹的名称
                            print('image=',image_lists)
                            n_classes = n
                            print('n=',n)
                            bottleneck_input = tf.placeholder(tf.float32, [None, BOTTLENECK_TENSOR_SIZE])
                            ground_truth_input = tf.placeholder(tf.float32, [None, n_classes])


                            with tf.name_scope('final_training_ops'):
                                weights = tf.placeholder(tf.float32, [BOTTLENECK_TENSOR_SIZE, n_classes])
                                biases = tf.placeholder(tf.float32, [n_classes])
                                logits = tf.matmul(bottleneck_input, weights) + biases
                                final_tensor = tf.nn.softmax(logits)
                            with tf.name_scope('evaluation'):
                                correct_prediction = tf.equal(tf.argmax(final_tensor, 1), tf.argmax(ground_truth_input, 1))
                                evaluation_step = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
                            print('-------')

                            # 在测试数据上测试正确率。
                            test_bottlenecks, test_ground_truth, testnames, labelname = evalu2.get_test_bottlenecks(
                                sess, image_lists, n, jpeg_data_tensor, bottleneck_tensor, lanames, INPUT_DATA)
                            # print('-------')
                            # test_accuracy = sess.run(evaluation_step, feed_dict={weights: weights1,
                            #                                                      biases: biases1,
                            #                                                      bottleneck_input: test_bottlenecks,
                            #                                                      ground_truth_input: test_ground_truth})

                            fin = sess.run(final_tensor, feed_dict={weights: weights1,
                                                                    biases: biases1,
                                                                    bottleneck_input: test_bottlenecks})
                            # print('fin=', fin)

                            m1, n1 = np.shape(fin)
                            kjs = []

                            for i in range(m1):
                                maxp = fin[i][0]
                                kj = 0
                                for j in range(n1):
                                    if (maxp < fin[i][j]):
                                        maxp = fin[i][j]
                                        kj = j
                                kjs.append(kj)
                            for i in range(m1):
                                # print('m1=',m1)
                                # print('i=',i)
                                # print('kjs=',kjs)
                                # print('lanames=',lanames)
                                print('该图片分类为: ', lanames[kjs[i]])
                                print('strart_upload_flag=', upload_flag)
                                image_name = image_lists[normal_name]['testing'][i] #第i个图片的名称
                                add_qcount = 0

                                print('image_nane ', image_name)
                                if(lanames[kjs[i]] != normal_name):
                                    add_qcount = 1#增加劣化样本1
                                    print('lanames[[=',lanames[kjs[i]])
                                    qcount += 1
                                   # print('image_name=',image_lists['daisy']['testing'][i])
                                    # print(lanames[kjs[i]])

                                    if upload_flag == 0 or upload_flag == 2:

                                        print('upload_path=',os.path.join(dirct,image_name))
                                        name = image_lists[list(image_lists.keys())[0]]['testing'][i]
                                        category = lanames[kjs[i]]
                                        # print('category',category)
                                        # httptools.image_tools(os.path.join(dirct,image_name),name,category)


                                        # httptools.image_tools(dirct+'/'+image_name,name,category)
                                        p = multiprocessing.Process(target=httptools.image_tools, args=(dirct+'/'+image_name,name,category,))
                                        p.start()

                                        # print('upload_flag=',upload_flag)
                                    elif upload_flag == 1 or upload_flag == 3:
                                        # print('upload_flag=', upload_flag)
                                        pass
                                else:
                                    if upload_flag == 0 or upload_flag == 1:
                                        name = image_lists[list(image_lists.keys())[0]]['testing'][i]
                                        category = lanames[kjs[i]]
                                        # httptools.image_tools(os.path.join(dirct, image_name), name, category)

                                        # httptools.image_tools(dirct+'/'+image_name, name, category)
                                        p = multiprocessing.Process(target=httptools.image_tools,
                                                                    args=(dirct + '/' + image_name, name, category,))
                                        p.start()
                                        # print('path = ', os.path.join(dirct,image_name))
                                        print('path = ', dirct+'/'+image_name)
                                        # print('upload_flag=', upload_flag)
                                    else:
                                        pass

                                count += 1
                                print('count=',count)
                                #info = {}
                                c = 1  #每隔一张图片发一次信息
                                if count % c == 0:
                                    spend_time = time.time() - start_evaulate_time
                                    info = {
                                            'id':'win-desktop',
                                            'qcount': str(qcount),
                                            'count':str(count),
                                            'spend_time': str(spend_time).split('.')[0],
                                            'add_count':str(c),
                                            'add_qcount':str(add_qcount)
                                    }
                                    print('qcount', qcount)


                                # httptools.tools(info)
                                p = multiprocessing.Process(target=httptools.tools,
                                                            args=(info,))
                                p.start()

                            cor = sess.run(correct_prediction, feed_dict={weights: weights1,
                                                                          biases: biases1,
                                                                          bottleneck_input: test_bottlenecks,
                                                                          ground_truth_input: test_ground_truth
                                                                          })
                            #print('cor=', cor)


                            for imagename in image_lists[normal_name]['testing']:
                                print('删除图片',imagename)
                                print('imgremove',INPUT_DATA + '/'+ normal_name + '/' + imagename)
                                os.remove(INPUT_DATA + '/'+ normal_name + '/' + imagename)
#'''



                            #for i in os.listdir(INPUT_DATA + '/'+ normal_name):
                                #os.remove(INPUT_DATA + '/' + normal_name + '/' + i)

                            print('检测完第' + str(count) + '张图片')


                            '''
                            if count%10 == 0:
                                spend_time = time.time()-start_evaulate_time
                                info = {'flag': '1','count':str(count), 'spend_time': str(spend_time)}
                                httptools.tools(info)
                            '''
                        else:

                            pass
                    except:
                        num += 1
                        num %= 10
                        if(num==5):
                            print('正在等待输入检测图片...')
                else:
                    break

@app.route('/evaluatecnn', methods=['POST'])
def son():
    print(request.json)
    data = request.json
    model_path = data['model_path']
    input_data = data['input_data']
    print('model_path',model_path)
    print('input_data',input_data)
    qualified_samples_upload = data['qualified_samples_upload']
    degraded_samples_upload = data['degraded_samples_upload']
    #qualified_samples_upload = dicts['qualified_samples_upload']
    #degraded_samples_upload = dicts['degraded_samples_upload']
    #input_data = dicts['input_data']
    # print('input_data=1234445',input_data)
    if qualified_samples_upload=='yes' and degraded_samples_upload=='yes':
        upload_flag = 0
    elif qualified_samples_upload=='yes' and degraded_samples_upload=='no':
        upload_flag =1
    elif qualified_samples_upload=='no' and degraded_samples_upload=='yes':
        upload_flag =2
    else:
        upload_flag =3
    model_path = '../../data/models'
    evalu(input_data, model_path,upload_flag)
    time.sleep(3)
    result = {'code': 10000}
    return Response(json.dumps(result), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True,port=8081,host='0.0.0.0')




