import os
import numpy as np
import datetime

import torch

def make_data(path, phase='train'):
    path_images = []
    
    for img_name in os.listdir(f'{path}/{phase}'):
        if img_name.endswith(('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')):
            path_images.append(f'{path}/{phase}/{img_name}')
    
    return np.stack(path_images)

def cnt_correct(y_true, y_pred):
    top_N, top_class = y_pred.topk(1, dim=-1)
    equals = top_class == y_true.view(*top_class.shape)
    return torch.sum(equals.type(torch.FloatTensor)).item()

def log_with_timestamp(msg):
    print(f'{datetime.datetime.today()} : {msg}')

def bash_cmd(cmd):
    print()
    _ = os.system(cmd)
    print()