import cv2 as cv
from aip import AipBodyAnalysis
import os
import base64
import time

def main():
    APP_ID = '22120405'
    API_KEY = '5caxODUpm1FbDp1MCRqvyDa4'
    SECRET_KEY = 'RIknWXhGraZPO58OBUZWcoOqm8piqGTY'
    client = AipBodyAnalysis(APP_ID, API_KEY, SECRET_KEY)
    options = {}
    options["type"] = "foreground"
    path = 'src'
    dirs = os.listdir(path)
    for name in dirs:
        start = time.time()
        filepath = path + '/' + name
        pic_b=openpic(filepath)
        result=client.bodySeg(pic_b,options)
        person_b=base64.b64decode(result["foreground"])
        with open('dst/'+name+'.png', 'wb') as f:
            f.write(person_b)
            print(name,"处理完成！")
        end = time.time()
        print("耗时：",end-start)

def openpic(path):
    f=open(path,'rb')
    pic_b=f.read()
    return pic_b


if __name__ == '__main__':
    main()