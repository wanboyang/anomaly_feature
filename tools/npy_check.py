import os
import glob
from tqdm import tqdm
from multiprocessing import Pool

def npy_check(file):
    file_path, file_name = os.path.split(file)
    file_n= file_name.split('.')[0].split('_')
    start = int(file_n[0])
    end = int(file_n[1])
    if end - start == 15:
        os.remove(file)


if __name__ == '__main__':
    npys_path = '/home/tu-wan/windowswan/dataset/LAD/features_4frame'
    npys_files = glob.glob(os.path.join(npys_path,'*/*/*/*.npy'))
    with Pool(processes=4) as p:
        max_ = len( npys_files)
        with tqdm(total=max_) as pbar:
            for i, _ in tqdm(enumerate(p.imap_unordered(npy_check,  npys_files))):
                pbar.update()
