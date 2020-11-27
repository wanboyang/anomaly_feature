import zipfile
import os
import glob
from multiprocessing import Pool
from tqdm import tqdm

def unzip_single(src_file):
     ''' 解压单个文件到目标文件夹。
     '''

     zf = zipfile.ZipFile(src_file)
     dest_dir = src_file.replace('.zip','').replace('denseflow', 'denseflow_img').replace('windows4t', 'windowswan').replace('larger_video', 'larger_video1')
     if os.path.exists(dest_dir) == 0:
         os.makedirs(dest_dir)
     try:
         zf.extractall(path=dest_dir)
     except RuntimeError as e:
         print(e)
     zf.close()
     # else:
     #     print('file {} already existed'.format(dest_dir))
if __name__ == "__main__":
    zip_files = []

    zip_files_tmp = glob.glob('/home/tu-wan/windows4t/dataset/UCF_Crime/denseflow/larger_video/Normal_Videos331_x264*/*.zip')
    for i in range(len(zip_files_tmp)):
        zip_file = zip_files_tmp[i]
        # zip_files.append(zip_file)
        if zip_file.find('/img.zip') != -1:
            continue
        else:
            zip_files.append(zip_file)

    with Pool(processes=4) as p:
        max_ = len(zip_files)
        with tqdm(total=max_) as pbar:
            for i, _ in tqdm(enumerate(p.imap_unordered(unzip_single, zip_files))):
                pbar.update()

