import cv2 as cv
from aip import AipBodyAnalysis
import threading as td
import os
import shutil
import base64
import math
import time
from retrying import retry


APP_ID = [
        '22120405',
        '22128436',
        '22128442',
        '22387692'
        ]
API_KEY = [
        '5caxODUpm1FbDp1MCRqvyDa4',
        'HefzxzGSX1GDI5KxGSuQ49xy',
        'B9IRS0r3E8jwF0XObD2Fkj6j',
        'E2oGkcQ2WplEM20Efh35udfL'
        ]
SECRET_KEY = [
        'RIknWXhGraZPO58OBUZWcoOqm8piqGTY',
        'hPmOD1a3Nsk2dgoSTOURjB3FnlzIVAhA',
        'gsoXWw2njWQCPIZM1Hk73iez90qu1XlS',
        'XnmjDizrRxLd1vUsRAOaph41gHvfMBF8'
        ]
options = {}
options["type"] = "foreground"


def main():
    video_name = input("请输入视频文件的名称（视频文件应与本程序在同一级文件夹下）：")
    gen_src(video_name)     # 预处理
    path = 'src'
    dirs = os.listdir(path)
    core=int(input("请输入线程数（最大为4。请确保线程数不多于图片数量的一半，否则会出错！）:"))
    if core > 0 and core < 5:
        list_dir = split_list(dirs,core)
    else:
        print("线程数输入有误！")
    get_person(list_dir,core)

def get_person(list,core):
    for i in range(core):
        td.Thread(target=get_body,args=(list,i)).start()

def get_body(list,i):
    global APP_ID,API_KEY,SECRET_KEY,options
    dirs = list[i]
    client = AipBodyAnalysis(APP_ID[i], API_KEY[i], SECRET_KEY[i])
    for name in dirs:
        start=time.time()
        filepath = 'src/' + name
        pic_b=openpic(filepath)
        person_b=try_to_get_person(client,pic_b,options)  #多线程容易出错，使用了retry模块
        with open('dst/'+name+'.png', 'wb') as f:
            f.write(person_b)
            print(name,"处理完成！")
        end = time.time()
        print("耗时：", end - start)


@retry(stop_max_attempt_number=10)       #重试3次还不行就放弃，报错后有一个进程会终止
def try_to_get_person(client,pic_b,options):
    result = client.bodySeg(pic_b, options)
    person_b = base64.b64decode(result["foreground"])
    return person_b

def openpic(path):
    f=open(path,'rb')
    pic_b=f.read()
    return pic_b


def split_list(dirs,core):    # 切分列表
    l = math.ceil(len(dirs)/core)   # 核心数少于图片数量的一半用向上取整，否则用向下取整！！！
    return [dirs[i:i + l] for i in range(0, len(dirs), l)]


def gen_src(video_name):    #预处理
    if os.path.exists('src'):
        shutil.rmtree('src')
    if os.path.exists('dst'):
        shutil.rmtree('dst')
    os.mkdir('src')
    os.mkdir('dst')
    command="ffmpeg -i "+video_name+" -q:v 1 src\\%6d.jpeg"     #-q:v 1表示输出的图片质量，一般是1到5之间（1 为质量最高）
    os.system(command)

if __name__ == '__main__':
    main()