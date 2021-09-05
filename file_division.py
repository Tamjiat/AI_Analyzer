import os
import shutil
import json
import cv2
from config import config as cfg
from json_parse import json_parse
from tensorflow.keras.preprocessing.image import ImageDataGenerator

fruit_0,fruit_0_p,fruit_1,fruit_1_p,leaf_0,leaf_0_p,leaf_1,leaf_1_p = json_parse() 
class_name = [fruit_0,fruit_1,leaf_0,leaf_1]
class_point = [fruit_0_p,fruit_1_p,leaf_0_p,leaf_1_p]
categories = ["fruit_0","fruit_1","leaf_0","leaf_1"]
x=0
path2="" #옮길 폴더
for n , p in zip(class_name[3], class_point[3]):
    x=x+1
    img = cv2.imread(cfg.image_path+n)
    img = img[p["ytl"]:p["ybr"],p["xtl"]:p["xbr"]]
    print(n)
    cv2.imwrite("/media/user/My Passport/AI HUB2/노지 작물 질병 진단 이미지/Validation/고추/leaf_1_test/"+n,img)
    print("진행률 : "+str(len(class_name[3]))+" / "+str(x))

for n in fruit_0:
    img = cv2.imread(cfg.image_path+n)
    shutil.move(cfg.image_path+n,path2+"/fruit_0/"+n)