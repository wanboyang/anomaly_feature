import glob
from tqdm import tqdm
from multiprocessing import Pool

def delect(filelist):
    conmand = 'rm -rf {}'.format(filelist)
    with open(file='imgdelete.sh',mode='a+') as f:
        f.write(conmand+'\n')

if __name__ == "__main__":
    with open(file='imgdelete.sh',mode='w') as f:
        f.write('#!/usr/bin/env bash'+'\n')
    files = glob.glob('/home/tu-wan/windowswan/dataset/UCF_Crime/denseflow_img/Training_Normal_Videos_Anomaly/*.jpg')
    with Pool(processes=6) as p:
        max_ = len(files)
        with tqdm(total=max_) as pbar:
            for i, _ in tqdm(enumerate(p.imap_unordered(delect, files))):
                pbar.update()

