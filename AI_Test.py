import numpy as np
import cv2
from keras.models import load_model
from config import config as cfg

def AI_Test(file):
    model = load_model('backup/pepper.h5')
    # 이미지 resize
    img = cv2.imread(file)
    img = cv2.resize(img,dsize=(cfg.IMAGE_WIDTH,cfg.IMAGE_HEIGHT),interpolation=cv2.INTER_AREA)
    X =[]
    X.append(img/256)
    X = np.array(X, dtype = 'float32')
    # 예측
    pred = model.predict(X)  
    result = [np.argmax(value) for value in pred]   # 예측 값중 가장 높은 클래스 반환
    categories = ["정상","고추탄저병","정상","고추흰가루병"]
    print('New data category : ',categories[result[0]])
    return categories[result[0]]