import os
import numpy as np
from tqdm import tqdm
import pandas as pd

import torch
from torch.utils.data import DataLoader

import torch.distributed as dist
import torch.multiprocessing as mp
from torch.nn.parallel import DistributedDataParallel

import transforms
import datasets
import utils
from models import get_model
from config import config as cfg

from sklearn.metrics import confusion_matrix, classification_report

pnum = cfg.pnum
crop_name = cfg.crop_name

is_cuda = torch.cuda.is_available()

os.environ['CUDA_VISIBLE_DEVICES'] = str(cfg.gpu)

path_images_test = utils.make_data(f'{cfg.path_prefix}/{cfg.path_data}/{cfg.crop_name}', '3.Test')

def test(model, valid_loader, criterion):
    model.eval()

    list_true = []
    list_pred = []
    
    loss_sum = 0
    correct_sum = 0
    
    log_every = len(valid_loader)//5
    
    len_data = 0

    utils.log_with_timestamp(f'Test ... 0%')

    for i, (image, label, name) in enumerate(valid_loader):
        if is_cuda and cfg.gpu is not None:
            image = image.cuda(cfg.gpu, non_blocking=True)
            label = label.cuda(cfg.gpu, non_blocking=True)

        pred = model(image)

        loss = criterion(pred, label)
        loss_sum += loss.item()

        len_data += image.shape[0]
        correct_sum += utils.cnt_correct(label, pred)
        
        list_true.append(label.detach().cpu().numpy().flatten())
        list_pred.append(pred.detach().cpu().numpy().argmax(-1).flatten())
        
        if (i+1)%log_every == 0:
            utils.log_with_timestamp(f'Test ... {((i+1)//log_every)*20}%')
    
    return loss_sum/len_data, correct_sum/len_data, np.concatenate(list_true, axis=0), np.concatenate(list_pred, axis=0)


def main():
    print('========= Test Environment =========\n')
    _ = utils.bash_cmd('cat /proc/cpuinfo | grep "model name" | uniq')
    _ = utils.bash_cmd('nvidia-smi')
    _ = utils.bash_cmd('free -h')
    _ = utils.bash_cmd('df /')
    _ = utils.bash_cmd('cat /etc/os-release')
    
    print('\nPyTorch version: ', torch.__version__, '\n')
    
    utils.log_with_timestamp('Model loading ... ')
    model = get_model(cfg.train_model, cfg.num_classes)
    ckpt = torch.load(cfg.test_model_path, map_location='cpu')
    model.load_state_dict(ckpt['model_state_dict'])

    utils.log_with_timestamp('Model compiling ... ')
    criterion = torch.nn.CrossEntropyLoss()
    
    if cfg.gpu is not None and is_cuda:
        utils.log_with_timestamp(f"Use GPU: {cfg.gpu} for testing")
        torch.cuda.set_device(cfg.gpu)
        model = model.cuda(cfg.gpu)
    else:
        utils.log_with_timestamp('Use CPU, this will be slow')

    test_loader = DataLoader(datasets.CustomDataSet(path_images_test, transforms.test_aug, test=True), batch_size=1, shuffle=False, num_workers=0)

    print('\n===== Start testing =====\n')
    test_loss, test_acc, list_true, list_pred = test(model, test_loader, criterion)

    print('\n===== Test result =====\n')
    print(classification_report(list_true, list_pred, digits=5))
    print('\n========= Confusion Matrix =========\n')
    for rr in confusion_matrix(list_true, list_pred):
        print(rr)

    print('\nLog csv ... ')
    df = pd.DataFrame({'image_name': path_images_test,
                       'true': list_true,
                       'pred': list_pred})
    
    df.to_csv(f'{pnum}_{crop_name}_log_each_sample.csv')
    
    print('\n===== Finished testing =====')
    
    _ = utils.bash_cmd('sh rm_cache.sh')

if __name__ == '__main__':
    main()