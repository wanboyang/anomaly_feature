#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import glob
from tqdm import tqdm
from multiprocessing import Pool


def converter(file_mp4):
    file_avi = file_mp4.replace('.mp4', '.avi')
    # file_new = file_name.replace('.3gp', '.mp4')
    comm = 'ffmpeg -i {0} -strict -2 {1}'.format(file_mp4, file_avi)
    os.system(comm)
    print(file_mp4, 'has been convert to', file_avi)

if __name__ == "__main__":

    mp4_files = glob.glob('/home/tu-wan/windows4t/dataset/UCF_Crime/Video/*/*.mp4')
    with Pool(processes=8) as p:
        max_ = len(mp4_files)
        with tqdm(total=max_) as pbar:
            for i, _ in tqdm(enumerate(p.imap_unordered(converter, mp4_files))):
                pbar.update()
