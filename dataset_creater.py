import numpy as np
import os
import glob
from multiprocessing import Pool
from tqdm import tqdm
import json
import pandas as pd
import pickle
import argparse

def combine_feature(video):
    combine_fea= []
    rgb_fea = []
    flow_fea = []
    rgb_features = glob.glob(os.path.join('/home/tu-wan/windowswan/dataset/{}//features//{}'.format(dataset, pretrain_model),'rgb',video, '*.npy'))
    rgb_features.sort(key=lambda x: int(x[-9:-4]))
    flow_features = glob.glob(os.path.join('/home/tu-wan/windowswan/dataset/{}//features//{}'.format(dataset, pretrain_model), 'flownet', video, '*.npy'))
    flow_features.sort(key=lambda x: int(x[-9:-4]))
    for i in range(len(rgb_features)):
        rgb_fea_np = np.load(rgb_features[i])
        flow_fea_np = np.load(flow_features[i])
        rgb_fea.append(rgb_fea_np)
        flow_fea.append(flow_fea_np)
        feature = np.hstack((rgb_fea_np,flow_fea_np))
        combine_fea.append(feature)
    combine_fea = np.asarray(combine_fea)
    rgb_fea = np.asarray(rgb_fea)
    flow_fea = np.asarray(flow_fea)
    save_path = os.path.join('/home/tu-wan/windowswan/dataset/{}//features_video//{}'.format(dataset, pretrain_model), 'combine_flownet',video)
    if os.path.exists(save_path) == 0:
        os.makedirs(save_path)
    if os.path.exists(os.path.join('/home/tu-wan/windowswan/dataset/{}//features_video//{}'.format(dataset, pretrain_model), 'rgb', video)) == 0:
        os.makedirs(os.path.join('/home/tu-wan/windowswan/dataset/{}//features_video//{}'.format(dataset, pretrain_model), 'rgb', video))
    if os.path.exists(os.path.join('/home/tu-wan/windowswan/dataset/{}//features_video//{}'.format(dataset, pretrain_model), 'flownet', video)) == 0:
        os.makedirs(os.path.join('/home/tu-wan/windowswan/dataset/{}//features_video//{}'.format(dataset, pretrain_model), 'flownet', video))
    np.save(file=os.path.join(save_path, 'feature.npy'),arr=combine_fea)
    np.save(file=os.path.join('/home/tu-wan/windowswan/dataset/{}//features_video//{}'.format(dataset, pretrain_model), 'rgb', video, 'feature.npy'), arr=rgb_fea)
    np.save(file=os.path.join('/home/tu-wan/windowswan/dataset/{}//features_video//{}'.format(dataset, pretrain_model), 'flownet', video,  'feature.npy'), arr=flow_fea)



if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", help='Name of dataset', default='shanghaitech', type=str)
    args = parser.parse_args()
    pretrain_model = 'i3d'
    dataset = args.dataset
    feature_dir = '/home/tu-wan/windowswan/dataset/{}/features/{}'.format(dataset, pretrain_model)
    # # #
    '''combine the rgb and flow feature on every video'''
    rgb_feature_dir = os.path.join(feature_dir,'rgb')
    flow_feature_dir = os.path.join(feature_dir, 'flownet')
    videos = os.listdir(rgb_feature_dir)
    # videos = ['Normal_Videos579_x264']
    with Pool(processes=6) as p:
        max_ = len(videos)
        with tqdm(total=max_) as pbar:
            for i, _ in tqdm(enumerate(p.imap_unordered(combine_feature, videos))):
                pbar.update()

    # """creat dataset"""
    # train_list = []
    # test_list = []
    # #
    # video_frame_label_dict = {}
    # video_label_dict = {}
    # label_dict = {}
    # videonames = os.listdir(feature_dir + '/rgb')
    # labels_dir = '/home/tu-wan/windowswan/dataset/UCF_Crime/GT'
    # # labels_files = glob.glob(os.path.join(labels_dir, '*', '*', '*.xlsx')) #ARD
    # # labels_files = glob.glob(os.path.join(labels_dir, '*.npy'))
    # labels_files = glob.glob(os.path.join(labels_dir, '*/*.npy'))
    # for labels_file in labels_files:
    #     # labels_file_name = os.path.split(labels_file)[1].split('.')[0].replace('gt_', 'v_') #ARD
    #     labels_file_name = os.path.split(labels_file)[1].split('.')[0]
    #     label_dict[labels_file_name] = labels_file
    #     """
    #     uncomment for ARD
    #     """
    # for videoname in videonames:
    #     if videoname in label_dict.keys():
    #         csv = pd.read_excel(label_dict[videoname])
    #         data = csv.values
    #         frame_label = data[:, 1]
    #     else:
    #         frame_label = []
    #     if videoname.find('_a_') != -1:
    #         video_label_dict[videoname] = [1.]
    #     else:
    #         video_label_dict[videoname] = [0.]
    #     video_frame_label_dict[videoname] = frame_label
    #
    #
    # """
    # uncomment for shanghaitech and UCF_Crime
    # """
    # test_dict = label_dict.copy()
    # for videoname in videonames:
    #     if videoname in label_dict.keys():
    #         test_dict.pop(videoname)
    #         test_list.append(videoname)
    #         frame_label = np.load(label_dict[videoname])
    #         if np.max(frame_label) > 0:
    #             video_label_dict[videoname] = [1.]
    #         else:
    #             video_label_dict[videoname] = [0.]
    #         video_frame_label_dict[videoname] = frame_label
    #     else:
    #         train_list.append(videoname)
    #         video_frame_number = len(os.listdir(os.path.join(feature_dir + '/rgb', videoname))) * 16
    #         frame_label = []  #shanghaitech
    #
    #         # video_label_dict[videoname] = [0.] #shanghaitech
    #
    #         if videoname.find('Normal') != -1:
    #             video_label_dict[videoname] = [0.]
    #         else:
    #             video_label_dict[videoname] = [1.]
    #         video_frame_label_dict[videoname] = frame_label
    # with open(file=os.path.join(labels_dir, 'frame_label.pickle'), mode='wb') as f:
    #     pickle.dump(video_frame_label_dict, f, protocol=pickle.HIGHEST_PROTOCOL)
    # with open(file=os.path.join(labels_dir, 'video_label.pickle'), mode='wb') as f:
    #     pickle.dump(video_label_dict, f, protocol=pickle.HIGHEST_PROTOCOL)
    # np.savetxt(os.path.join('/home/tu-wan/windowswan/dataset/UCF_Crime', 'train_split.txt'), np.asarray(train_list), fmt='%s')
    # np.savetxt(os.path.join('/home/tu-wan/windowswan/dataset/UCF_Crime', 'test_split.txt'), np.asarray(test_list), fmt='%s')
    #
    #







