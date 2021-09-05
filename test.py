import numpy as np
import cv2
from keras.models import load_model
from config import config as cfg
model = load_model('backup/pepper.h5')
# 적용해볼 이미지 
test_image = '/media/user/My Passport/AI HUB2/노지 작물 질병 진단 이미지/Validation/고추이미지/V006_79_1_01_01_01_13_2_9315z_20200922_28_a0009.JPG'

path_dir = "../myapp/public/images"
i = "V006_79_0_00_01_01_13_0_a05_20201111_0001_S01_1.JPG"
# 이미지 resize
img = cv2.imread(path_dir +"/"+ i)
img = cv2.resize(img,dsize=(cfg.IMAGE_WIDTH,cfg.IMAGE_HEIGHT),interpolation=cv2.INTER_AREA)
X =[]
X.append(img/256)
X = np.array(X, dtype = 'float32')
# 예측
pred = model.predict(X)  
print(pred)
result = [np.argmax(value) for value in pred]   # 예측 값중 가장 높은 클래스 반환
print(np.argmax(pred[0]))
categories = ["fruit_0","fruit_1","leaf_0","leaf_1"]
print('New data category : ',categories[result[0]])
