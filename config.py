class config():
    path_prefix = '.'
    path_data = 'dataset'

    dict_label = {'04': {'00': 0, '07': 1, '08': 2}}

    # general args
    gpu = 0
    train_size = (512, 512)
    train_model = 'resnet50' #'ENet'
    pnum = 79
    crop_name = '04'
    num_classes = 3

    # testing args
    test_model_path = 'weights/sample.pt'
