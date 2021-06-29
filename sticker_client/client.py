#coding: utf-8
import os,sys,requests,json,traceback
#from requests.adapters import HTTPAdapter
#from requests.packages.urllib3.util.retry import Retry
import base64

import time
import datetime

import numpy as np
import cv2
from numpy import int32

##################################
#image to json
##################################
imgpath = 'input_imgs/img0(3-Happy).jpg'
with open(imgpath,'rb') as fin:
    image_byte_client = fin.read()#bytes
    base64data_client = base64.b64encode(image_byte_client)#bytes
    strdata_client = base64data_client.decode('utf-8')#str
    json_dict_client = {"imgbase64":strdata_client}#dict


json_dict_client = {"imgbase64":strdata_client}#dict   
json_str_client = json.dumps(json_dict_client)#str
#print("json_str_client: ",json_str_client)
#print("generate imput image json")

try:
    
    t0 = time.time()
    request = requests.post(url='http://0.0.0.0:5000/api', data=json_str_client)
    #request = requests.post(url='http://ApiDemo-env.eba-qyf98pxi.us-east-1.elasticbeanstalk.com/api', data=json_str_client)
    t1 = time.time()
    print('send time is %.3f'%(t1-t0))
    
    response = request.json()
    print("response: ", response)
    print(response['code'])
    json_dict_server = response['data']
    print("The image emotion: ",json_dict_server['emotion'])
    img_client = json_dict_server['sticker']
    #print(img_client)

    base64data_server = img_client.encode('utf-8')
    image_byte_server = base64.b64decode(base64data_server)    
    nparr = np.fromstring(image_byte_server,dtype=np.uint8)
    img = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
    cv2.imwrite('output_imgs/sticker.jpg', img)


except Exception as e:
    print("exception: "+str(e)) 
    traceback.print_exc(file=sys.stdout)

