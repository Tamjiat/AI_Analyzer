import cv2
import numpy as np
import json

import torch
from torch.utils.data import Dataset

import transforms
from config import config as cfg

class CustomDataSet(Dataset):
    def __init__(self, path_images, transform, test=False):
        self.path_images = path_images
        self.transform = transform
        self.test = test

    def __getitem__(self, index):
        image = cv2.imread(self.path_images[index])[:,:,::-1]
        
        with open(f'{self.path_images[index]}.json') as json_file:
            json_decoded = json.load(json_file)

        label = cfg.dict_label[f'{int(json_decoded["annotations"]["crop"]):02d}'][f'{int(json_decoded["annotations"]["disease"]):02d}']
        
        resized_image = cv2.resize(image, cfg.train_size, interpolation = cv2.INTER_LANCZOS4) # INTER_AREA
        augmented_image = self.transform(image=resized_image)['image']

        if not self.test:
            return torch.tensor(augmented_image.transpose(2,0,1)), torch.tensor(label).long()
        else:
            return torch.tensor(augmented_image.transpose(2,0,1)), torch.tensor(label).long(), self.path_images[index]

    def __len__(self):
        return len(self.path_images)