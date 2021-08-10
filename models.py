import torch.nn as nn
import torchvision.models as models

dict_backbone = {'resnet50' : models.resnet50}

def get_model(model_name='resnet50', num_classes=3, pretrained=False): # use pretrained backbone
    assert model_name in dict_backbone.keys()
    
    network = dict_backbone[model_name](pretrained=pretrained)
    network.fc = nn.Linear(network.fc.in_features, num_classes)
    
    return network