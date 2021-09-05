from config import config as cfg
import os
import json
import pandas as pd
import cv2

def json_parse():
    jsonnames = os.listdir(cfg.json_path)
    fruit_0 = []
    fruit_0_p = []
    fruit_1 = []
    fruit_1_p = []
    leaf_0 =[]
    leaf_0_p =[]
    leaf_1 =[]
    leaf_1_p =[]
    for jsonname in jsonnames:
        with open(cfg.json_path+jsonname, "r", encoding="utf8") as f:
            contents = f.read()
            json_data = json.loads(contents)
        if json_data["annotations"]['area'] == 1:
            if json_data["annotations"]["disease"]==0:
                fruit_0.append(jsonname.split('.json')[0])
                fruit_0_p.append(json_data["annotations"]['points'][0])
            else:
                fruit_1.append(jsonname.split('.json')[0])
                fruit_1_p.append(json_data["annotations"]['points'][0])
        elif json_data["annotations"]['area'] == 3:
            if json_data["annotations"]["disease"]==0:
                leaf_0.append(jsonname.split('.json')[0])
                leaf_0_p.append(json_data["annotations"]['points'][0])
            else:
                leaf_1.append(jsonname.split('.json')[0])
                leaf_1_p.append(json_data["annotations"]['points'][0])
    return fruit_0,fruit_0_p,fruit_1,fruit_1_p,leaf_0,leaf_0_p,leaf_1,leaf_1_p
