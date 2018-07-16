#coding=utf-8

import shutil
import os 
import os.path
from PIL import Image

#更改文件格式
def change_img_type(img_path,geshi,paths):
    try:
        img=Image.open(img_path)
        img.save(paths+geshi)
    except Exception as error:
        print('change type error')

#文件重命名
def renamefile(path1,path2,prename):
    try:
        i = 0
        for file in os.listdir(path1):
            if os.path.isfile(os.path.join(path1, file)) == True:
                # print(file)
                if file.find('.') >= 0:
                    print(file)
                    newname = prename + '_' + str(i) + '.jpg'
                    i += 1
                    os.rename(os.path.join(path1, file), os.path.join(path2, newname))
    except Exception as error:
        print('rename error')


#复制一个文件
def filesave1(src,dst):
    path, filename = os.path.split(src)
    newdst = dst + '\\' + filename
    if (os.path.exists(src) == False):
        print('File not exists')
    if (os.path.exists(dst) == False):
        os.makedirs(dst)
    try:
        shutil.copy2(src, newdst)
    except Exception as error:
        print('Copy Error')

#复制多个文件
def filesave2(src,dst):
    if (os.path.exists(dst) == False):
        os.makedirs(dst)
    for i in src:
        if (os.path.exists(i) == False):
            print('File not exists')
        path, filename = os.path.split(i)
        newdst = dst + '\\' + filename
        #print(newdst)
        #print(i)
        try:
            shutil.copy2(i, newdst)
        except Exception as error:
            print('Copy Error')

# dst="D:\\fenlei"
'''
src="D:\images\\33.11mm7.17（1）\\0.tiff"
filesave1(src,dst)
'''
# src=[]
# src.append("D:\images\\33.11mm7.17（1）\\0.tiff")
# src.append("D:\images\\33.11mm7.17（1）\\1.tiff")
# filesave2(src,dst)




# for i in range(100,16272):
#     img = Image.open(file_path+str(i)+r".jpg")
#     img.save(file_path2+str(i)+r".jpg")
#     print(i)
import time

# 修改图片格式以及名称
file_path = r'/home/win/project/data/train_data/open//'#r'C:\project\data\train_data_png\ruoyangxing\\'
file_path2 = r'/home/win/project/data/imgupload//'
num=0
for i in os.listdir(file_path):
    img = Image.open(file_path+str(i))
    img.save(file_path2 + '00000003_00000006_00000010_win-desktop_win-desktop1_'+str(time.time()) + r".jpg")
    num += 1
print(num)
