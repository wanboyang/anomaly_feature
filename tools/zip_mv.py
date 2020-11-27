import glob
import shutil
import os
from tqdm import tqdm
from multiprocessing import Pool

def move(file):
    mo_file = file.replace('windowswan','windows4t')
    mo_path,mo_name = os.path.split(mo_file)
    if os.path.exists(mo_path) == 0:
        try:
            os.makedirs(mo_path)
        except:
            pass
    shutil.copyfile(file,mo_file)
def delete(file):
    os.remove(file)

if __name__ == '__main__':
    files = glob.glob('/home/tu-wan/windowswan/dataset/ARD/denseflow/*/*/*.zip')
    debug = False
    # if debug:
    #     for file in files:
    #         move(file = file)
    # else:
    #     with Pool(processes=4) as p:
    #         max_ = len(files)
    #         with tqdm(total=max_) as pbar:
    #             for i, _ in tqdm(enumerate(p.imap_unordered(move, files))):
    #                 pbar.update()
    if debug:
        for file in files:
            delete(file = file)
    else:
        with Pool(processes=4) as p:
            max_ = len(files)
            with tqdm(total=max_) as pbar:
                for i, _ in tqdm(enumerate(p.imap_unordered(delete, files))):
                    pbar.update()

