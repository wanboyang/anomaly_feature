import os
import numpy as np

def dir2txt(dir):
    videoname = []
    classes = os.listdir(dir)
    for cla in classes:
        videos = os.listdir(os.path.join(dir, cla))
        for video in videos:
            video = video.replace('f_', 'v_')
            videoname.append(video)
    return videoname

if __name__ == "__main__":
    save_dir = '/home/tu-wan/windowswan/project/anomaly_detect_others/dataset/LAD_tsn/all'
    train_dir = '/home/tu-wan/windowswan/dataset/ARD/ARD_Frames_112/training/'
    test_dir = '/home/tu-wan/windowswan/dataset/ARD/ARD_Frames_112/testing/'
    train_list = dir2txt(train_dir)
    test_list = dir2txt(test_dir)
    np.savetxt(os.path.join(save_dir, 'train_split.txt'), np.asarray(train_list), fmt='%s')
    np.savetxt(os.path.join(save_dir, 'test_split.txt'), np.asarray(test_list), fmt='%s')



