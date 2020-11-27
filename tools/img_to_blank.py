import zipfile
import os
import glob
from multiprocessing import Pool
from tqdm import tqdm

def blank(dir):
     ''' 解压单个文件到目标文件夹。
     '''

     zip_command = 'rsync --delete-before -d /tmp/blank/ {}/'.format(dir)
     print(zip_command)
     with open('img_remove.sh',mode='a+') as f:
         f.write(zip_command+'\n')
     # print('zip {} creat'.format(target))
if __name__ == "__main__":
    img_path = '/home/tu-wan/windowswan/dataset/UCF_Crime/denseflow_img/'
    dirs = glob.glob(os.path.join(img_path, '*', '*', 'flow*'))
    with open('img_remove.sh', mode='w') as f:
        f.write('#!/usr/bin/env bash' + '\n')
    for dir in dirs:
        blank(dir)





