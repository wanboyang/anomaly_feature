import timeit
import os
import glob
from tqdm import tqdm
import torch
# from tensorboardX import SummaryWriter
from torch import nn, optim
from torch.autograd import Variable
from torch.utils.data import DataLoader
# from feature_extraction.UCF_101_pretrain.model import Resnet
from sklearn import metrics
import numpy as np
import argparse
# from torchvision import transforms
from dataset.LAD_tsn import trainDataset, txttans
from model.i3d.src.i3dpt import I3D
from model.C3D_model import C3D
import sys

def feature(data_path, dataset, snapshot, modelName, dataloader, datamodal='rgb', fc_layer='fc6'):
    """
        Args:
            num_classes (int): Number of classes in the data
            num_epochs (int, optional): Number of epochs to train for.
    """

    train_params = []
    if modelName == 'c3d':
        model = C3D(nb_classes=487)
        train_params.append({'params': model.parameters()})
    elif modelName == 'i3d':
        if datamodal == 'rgb':
            model = I3D(400, modality='rgb', dropout_prob=0, name='inception')
        else:
            model = I3D(400, modality='flow', dropout_prob=0, name='inception')
    else:
        print('We only implemented C3D or i3d models.')
        raise NotImplementedError
    if snapshot:
        model.load_state_dict({k.replace('module.', ''): v for k, v in torch.load(snapshot).items()})
    if modelName == 'c3d':
        if fc_layer == 'fc6':
            model = nn.Sequential(*list(model.children())[:-5])
        elif fc_layer == 'fc7':
            model = nn.Sequential(*list(model.children())[:-2])
        feature_save_dir = os.path.join(data_path, 'dataset', dataset, 'features', modelName, fc_layer,
                                            datamodal)
    elif modelName == 'i3d':
        model = nn.Sequential(*list(model.children())[:-2])
        feature_save_dir = os.path.join(data_path, 'dataset', dataset, 'features', modelName, datamodal)

    if os.path.exists(feature_save_dir) == 0:
        os.makedirs(feature_save_dir)
    if os.path.exists(os.path.join('./model_feature/', dataset, modelName)) == 0:
        os.makedirs(os.path.join('./model_feature/', dataset, modelName))
    with open(file=os.path.join('./model_feature/', dataset, modelName,'feature.txt'), mode='a+') as f:
        f.write("dataset:{} ".format(dataset)+ '\n')
        f.write("snapshot:{} ".format(snapshot) + '\n')
        f.write("savedir:{} ".format(feature_save_dir) + '\n')
        f.write("========================================== " + '\n')
    cuda_device_count = torch.cuda.device_count()
    model = torch.nn.DataParallel(model, device_ids=np.arange(cuda_device_count).tolist())
    model.to(device)
    # print('Total params: %.2fM' % (sum(p.numel() for p in model.parameters()) / 1000000.0))
    model_feature(model=model,dataloader=dataloader, feature_save_dir=feature_save_dir,datamodal=datamodal,dataset=dataset)



def model_feature(model, dataloader, feature_save_dir, datamodal, dataset):

    model.eval()
    start_time = timeit.default_timer()
    if dataset=='shanghaitech':
        video_name_po = -2
    else:
        video_name_po = -3
    for img, fileinputs in tqdm(dataloader):
        # move inputs and labels to the device the training is taking place on
        inputs = Variable(img, requires_grad=False).to(device)
        # fileinputs = np.asarray(fileinputs)
        fileinputs = np.asarray(fileinputs).transpose((1, 0))
        with torch.no_grad():
            features = model(inputs)
        features = features.view(features.size(0), -1)
        features = features.data.cpu().numpy()
        for (fileinput, feature) in zip(fileinputs, features):
            if datamodal == 'flow' or datamodal == 'flownet':
                video_name = fileinput[0].split(':')[0].split('/')[video_name_po]
                start_frame = fileinput[0].split(':')[0].split('/')[-1].split('.')[0].split('_')[-1]
                end_frame = fileinput[-1].split(':')[0].split('/')[-1].split('.')[0].split('_')[-1]
                save_path = os.path.join(feature_save_dir, video_name, start_frame + '_' +end_frame + '.npy')
            else:
                video_name = fileinput[0].split('/')[video_name_po]
                start_frame = fileinput[0].split('/')[-1].split('.')[0].split('_')[-1]
                end_frame = fileinput[-1].split('/')[-1].split('.')[0].split('_')[-1]
                save_path = os.path.join(feature_save_dir, video_name, start_frame + '_' +end_frame + '.npy')

            if os.path.exists(os.path.join(feature_save_dir, video_name)) == 0:
                os.makedirs(os.path.join(feature_save_dir, video_name))
            np.save(save_path, feature)


    stop_time = timeit.default_timer()
    print("Execution time: " + str(stop_time - start_time) + "\n")





if __name__ == "__main__":

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("Device being used:", device)
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot", help='path of testing model_weight', default='model/i3d/i3d_model_weight/model_kinetics_flow.pth', type=str)
    parser.add_argument("--datamodal", help='rgb or flow', default='flownet', type=str)
    parser.add_argument("--dataset", help='Name of dataset', default='shanghaitech_flownet', type=str)
    parser.add_argument("--modelName", help='Name of model', default='i3d', type=str)
    parser.add_argument("--fc_layer", help='layer of feature extraction', default='fc6', type=str)
    args = parser.parse_args()
    snapshot = args.snapshot
    Dataset = args.dataset
    datamodal = args.datamodal
    if sys.platform == 'win32':
        data_path = 'D:/'
    elif sys.platform == 'linux':
        data_path = '/home/tu-wan/windows4t'


    if Dataset == 'LAD':

        origin_filelist = './dataset/LAD_tsn/all/{}_list.txt'.format(datamodal)
        origin_labellist = './dataset/LAD_tsn/all/label.txt'
        trainfile_list = './dataset/LAD_tsn/all/{}_list_numJoints.txt'.format(datamodal)
        trainlabel_list = './dataset/LAD_tsn/all/trainlabel_numJoints.txt'
        numJoints = 16
        txttans(origin_filelist=origin_filelist,
                origin_labellist=origin_labellist,
                processed_filelist=trainfile_list ,
                processed_labellist=trainlabel_list,
                numJoints=numJoints,
                model='train',
                framework=' ')
        # trans = transforms.Compose(transforms=[
        #     transforms.ToTensor()
        #     # transforms.Normalize(mean=[])
        # ])
        train_dataset = trainDataset(list_file=trainfile_list,
                                 GT_file=trainlabel_list,
                                     transform=None,
                                     cliplen=numJoints,
                                     datamodal=datamodal,
                                     args=args)

        train_dataloader = DataLoader(dataset=train_dataset,batch_size=48, pin_memory=True,
                                  num_workers=5,shuffle=False)
    elif Dataset == 'shanghaitech':
        # origin_filelist = './dataset/shanghaitech_224/unary/trainlist.txt'
        # origin_labellist = './dataset/shanghaitech_224/unary/trainlabel.txt'
        # origin_test_filelist = './dataset/shanghaitech_224/unary/testlist.txt'
        # origin_test_labellist = './dataset/shanghaitech_224/unary/testlabel.txt'
        # trans = transforms.Compose(transforms=[
        #     transforms.re
        #     transforms.ToTensor(),
        #     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        # ])
        # train_dataloader = DataLoader(trainDataset(list_file=origin_filelist,
        #                 GT_file=origin_labellist, transform=trans), batch_size=64, shuffle=False, num_workers=0)
        # test_dataloader = DataLoader(trainDataset(list_file=origin_test_filelist,
        #                                            GT_file=origin_test_labellist, transform=trans), batch_size=64,
        #                               shuffle=False, num_workers=0)
        datamodal = args.datamodal

        origin_filelist = './dataset/{}_tsn/all/{}_list.txt'.format(Dataset, datamodal)
        origin_labellist = './dataset/{}_tsn/all/label.txt'.format(Dataset)
        trainfile_list = './dataset/{}_tsn/all/{}_list_numJoints.txt'.format(Dataset, datamodal)
        trainlabel_list = './dataset/{}_tsn/all/trainlabel_numJoints.txt'.format(Dataset)
        # origin_testfile_list = './LAD/testlist.txt'
        # origin_testlabel_list = './LAD/testlabel.txt'
        # testfile_list = './LAD/testlist_numJoints.txt'
        # testlabel_list = './LAD/testlabel_numJoints.txt'

        numJoints = 16

        txttans(origin_filelist=origin_filelist,
                origin_labellist=origin_labellist,
                processed_filelist=trainfile_list,
                processed_labellist=trainlabel_list,
                numJoints=numJoints,
                model='train',
                framework='reconstruction')
        # txttans(origin_filelist=origin_testfile_list,
        #         origin_labellist=origin_testlabel_list,
        #         processed_filelist=testfile_list ,
        #         processed_labellist=testlabel_list,
        #         numJoints=numJoints,
        #         model='test')
        # trans = transforms.Compose(transforms=[
        #     transforms.ToTensor()
        #     # transforms.Normalize(mean=[])
        # ])
        train_dataset = trainDataset(list_file=trainfile_list,
                                     GT_file=trainlabel_list, transform=None, cliplen=numJoints, datamodal=datamodal, args=args)
        #
        train_dataloader = DataLoader(dataset=train_dataset, batch_size=16, pin_memory=True,
                                  num_workers=5, shuffle=False)

    elif Dataset == 'shanghaitech_flownet':
        datamodal = args.datamodal
        origin_filelist = './dataset/{}/all/{}_list.txt'.format(Dataset, datamodal)
        origin_labellist = './dataset/{}/all/label.txt'.format(Dataset)
        trainfile_list = './dataset/{}/all/{}_list_numJoints.txt'.format(Dataset, datamodal)
        trainlabel_list = './dataset/{}/all/trainlabel_numJoints.txt'.format(Dataset)
        # origin_testfile_list = './LAD/testlist.txt'
        # origin_testlabel_list = './LAD/testlabel.txt'
        # testfile_list = './LAD/testlist_numJoints.txt'
        # testlabel_list = './LAD/testlabel_numJoints.txt'

        numJoints = 16

        txttans(origin_filelist=origin_filelist,
                origin_labellist=origin_labellist,
                processed_filelist=trainfile_list,
                processed_labellist=trainlabel_list,
                numJoints=numJoints,
                model='train',
                framework='reconstruction')

        train_dataset = trainDataset(list_file=trainfile_list,
                                     GT_file=trainlabel_list,
                                     transform=None,
                                     cliplen=numJoints,
                                     datamodal=datamodal,
                                     args=args)
        #
        train_dataloader = DataLoader(dataset=train_dataset,
                                      batch_size=16,
                                      pin_memory=True,
                                      num_workers=1,
                                      shuffle=False)
    elif Dataset == 'UCF_Crime':
        origin_filelist = './dataset/UCF_Crime_tsn/all/{}_list.txt'.format(datamodal)
        origin_labellist = './dataset/UCF_Crime_tsn/all/label.txt'
        trainfile_list = './dataset/UCF_Crime_tsn/all/{}_list_numJoints.txt'.format(datamodal)
        trainlabel_list = './dataset/UCF_Crime_tsn/all/trainlabel_numJoints.txt'
        numJoints = 16
        txttans(origin_filelist=origin_filelist,
                origin_labellist=origin_labellist,
                processed_filelist=trainfile_list ,
                processed_labellist=trainlabel_list,
                numJoints=numJoints,
                model='train',
                framework=' ')
        # trans = transforms.Compose(transforms=[
        #     transforms.ToTensor()
        #     # transforms.Normalize(mean=[])
        # ])
        train_dataset = trainDataset(list_file=trainfile_list,
                                 GT_file=trainlabel_list, transform=None, cliplen=numJoints,datamodal=datamodal, args=args)
        #
        train_dataloader = DataLoader(dataset=train_dataset, batch_size=24, pin_memory=True,
                                  num_workers=1, shuffle=False)

    elif Dataset == 'Avenue':
        origin_filelist = './dataset/{}_tsn/all/{}_list.txt'.format(Dataset, datamodal)
        origin_labellist = './dataset/{}_tsn/all/label.txt'.format(Dataset)
        trainfile_list = './dataset/{}_tsn/all/{}_list_numJoints.txt'.format(Dataset, datamodal)
        trainlabel_list = './dataset/{}_tsn/all/trainlabel_numJoints.txt'.format(Dataset)
        numJoints = 16
        txttans(origin_filelist=origin_filelist,
                origin_labellist=origin_labellist,
                processed_filelist=trainfile_list ,
                processed_labellist=trainlabel_list,
                numJoints=numJoints,
                model='train',
                framework=' ')
        # trans = transforms.Compose(transforms=[
        #     transforms.ToTensor()
        #     # transforms.Normalize(mean=[])
        # ])
        train_dataset = trainDataset(list_file=trainfile_list,
                                 GT_file=trainlabel_list,transform=None, cliplen=numJoints,datamodal=datamodal, args=args)
        #
        train_dataloader = DataLoader(dataset=train_dataset,batch_size=24, pin_memory=True,
                                  num_workers=5,shuffle=False)
    elif Dataset == 'UCSDPed2':
        origin_filelist = './dataset/{}_tsn/all/{}_list.txt'.format(Dataset, datamodal)
        origin_labellist = './dataset/{}_tsn/all/label.txt'.format(Dataset)
        trainfile_list = './dataset/{}_tsn/all/{}_list_numJoints.txt'.format(Dataset, datamodal)
        trainlabel_list = './dataset/{}_tsn/all/trainlabel_numJoints.txt'.format(Dataset)
        numJoints = 16
        txttans(origin_filelist=origin_filelist,
                origin_labellist=origin_labellist,
                processed_filelist=trainfile_list ,
                processed_labellist=trainlabel_list,
                numJoints=numJoints,
                model='train',
                framework=' ')
        # trans = transforms.Compose(transforms=[
        #     transforms.ToTensor()
        #     # transforms.Normalize(mean=[])
        # ])
        train_dataset = trainDataset(list_file=trainfile_list,
                                 GT_file=trainlabel_list,transform=None, cliplen=numJoints,datamodal=datamodal, args=args)
        #
        train_dataloader = DataLoader(dataset=train_dataset,batch_size=24, pin_memory=True,
                                  num_workers=5,shuffle=False)

    modelName = args.modelName  # Options: C3D or R2Plus1D or R3D


    feature(data_path=data_path,
            dataset=Dataset,
            snapshot=snapshot,
            modelName = modelName,
            dataloader= train_dataloader,
            datamodal= datamodal,
            fc_layer=args.fc_layer)
    # feature(dataset=Dataset, snapshot=snapshot,  modelName =modelName,dataloader=test_dataloader)
