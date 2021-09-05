
from json_parse import json_parse
from models import get_model
from keras.models import load_model
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping, ReduceLROnPlateau #콜백 클래스 import
from config import config as cfg
import numpy as np
import cv2
import os

fruit_0,fruit_0_p,fruit_1,fruit_1_p,leaf_0,leaf_0_p,leaf_1,leaf_1_p = json_parse() #disease_1 은 고추탄저병, disease_2 은 고추흰가루병

earlystop = EarlyStopping(patience=10) #학습 중 정확도가 10번 떨어질 경우 학습 종료
#학습률 조정 클래스
learning_rate_reduction = ReduceLROnPlateau(monitor='val_accuracy',
                                           patience=2,
                                           verbose=1,
                                           factor=0.5,
                                           min_lr=0.00001) 
callbacks = [earlystop, learning_rate_reduction] #콜백 클래스 합침.
class_name = [fruit_0,fruit_1,leaf_0,leaf_1]
class_point = [fruit_0_p,fruit_1_p,leaf_0_p,leaf_1_p]
categories = ["fruit_0","fruit_1","leaf_0","leaf_1"]
disease=-1 # 0은 정상 열매, 1은 질병 열매, 2는 정상 잎, 3은 질병 잎
X=[]
Y=[]
for index, area in enumerate(categories):
    label = [0 for i in range(len(categories))] 
    label[index] = 1
    x=0
    for n , p in zip(class_name[index], class_point[index]):
        img = cv2.imread(cfg.image_path+n)
        img = img[p["ytl"]:p["ybr"],p["xtl"]:p["xbr"]]
        img = cv2.resize(img,dsize=(cfg.IMAGE_WIDTH,cfg.IMAGE_HEIGHT),interpolation=cv2.INTER_AREA)
        X.append(img/256)
        print("-----------------------------------------------------")
        x = x+1
        print("Image resize || class : "+area+" | "+"Image count : "+str(len(class_name[index]))+" / "+str(x))
        Y.append(label)
X = np.array(X, dtype = 'float32')
Y = np.array(Y, dtype = 'int32')


X_train, X_test, Y_train, Y_test = train_test_split(X,Y)
# xy = (X_train, X_test, Y_train, Y_test)
# np.save("pepper.npy", xy)
model = get_model(X_train,len(categories)) #모델 정의
model.fit(
    x=X_train,
    y=Y_train,
    validation_data=(X_test, Y_test),
    epochs=50,
    batch_size=4,
    verbose=1,
    callbacks=callbacks
)
model.save('backup/pepper.h5')

# new_model = load_model('backup/pepper.h5')
# new_model.fit(
#     x=X_train,
#     y=Y_train,
#     validation_data=(X_test, Y_test),
#     epochs=50,
#     batch_size=64,
#     verbose=1,
#     callbacks=callbacks
# )
# new_model.save('pepper_3.h5')

#모델 평가하기 
score = model.evaluate(X_test, Y_test)
print('loss=', score[0])        # loss 오차
print('accuracy=', score[1])    # acc 정확도