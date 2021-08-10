import albumentations
from config import config as cfg

test_aug = albumentations.Compose([albumentations.Normalize(mean=[0.485, 0.456, 0.406],
                                                             std=[0.229, 0.224, 0.225],
                                                             max_pixel_value=255.0,
                                                             p=1.0)
                                   ], 
                                   p=1.0)