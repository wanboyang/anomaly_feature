import zipfile
import os
import glob
from multiprocessing import Pool
from tqdm import tqdm

def gzip_single(dirs, target):
     ''' 解压单个文件到目标文件夹。
     '''
     path, _ = os.path.split(target)
     if os.path.exists(path) == 0:
         os.makedirs(path)
     _dir = dirs.split('/')[-1]
     cd_command = 'cd {} && cd ..'.format(dirs)
     zip_command = 'time tar -cvf - {}/ | pigz -p 6  > {}'.format(_dir, target)
     print(zip_command)
     with open('zip.sh',mode='a+') as f:
         f.write(cd_command+'\n')
         f.write(zip_command+'\n')

if __name__ == "__main__":
    with open(file='/home/tu-wan/windowswan/dataset/UCF_Crime/larger_video/larger_video.txt', mode='r') as f:
        videos = f.readlines()
    img_path = '/home/tu-wan/windowswan/dataset/UCF_Crime/denseflow_img_6250/Training_Normal_Videos_Anomaly'
    targets = []
    dirs = []
    with open('zip.sh',mode='w') as f:
        f.write('#! /usr/bin/env bash'+'\n')
    for video in videos:
        dirs_tmp = glob.glob(os.path.join(img_path, video.replace('\n', ''), '*'))
        # dirs.append(dirs_tmp)
        dirs += dirs_tmp
    for d in dirs:
        target = d.replace('denseflow_img_6250', 'denseflow').replace('windowswan', 'windows4t') + '.tar'
        targets.append(target)
    for d, t in zip(dirs,targets):
        gzip_single(dirs=d, target=t)





