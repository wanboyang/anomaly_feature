import os
import glob
import zipfile
import tarfile
from multiprocessing import Pool
from tqdm import tqdm


def unzip_single(src_file):
    ''' 解压单个文件到目标文件夹。
    '''
    if src_file.split('.')[-1]  == 'zip':
        pass
        zf = zipfile.ZipFile(src_file)
        dest_dir = src_file.replace('.zip', '').replace('denseflow', 'denseflow_img_6250').replace('windows4t',
                                                                                              'windowswan')
        if os.path.exists(dest_dir) == 0:
            os.makedirs(dest_dir)
        if os.listdir(dest_dir):
            pass
        else:
            try:
                zf.extractall(path=dest_dir)
            except RuntimeError as e:
                print(e)

        zf.close()
        # else:
        #     print('file {} already existed'.format(dest_dir))
    elif src_file.split('.')[-1]  == 'tar':
        pass
        # tar = tarfile.open(src_file,mode='r')
        # dest_dir = src_file.replace('.tar', '').replace('denseflow', 'denseflow_img_6250').replace('windows4t',
        #                                                                                       'windowswan')
        # if os.path.exists(dest_dir) == 0:
        #     os.makedirs(dest_dir)
        # if os.listdir(dest_dir):
        #     zip_command = 'rsync --delete-before -d /tmp/blank/ {}/'.format(dest_dir)
        #     print(zip_command)
        #     with open('img_remove.sh', mode='a+') as f:
        #         f.write(zip_command + '\n')
        #
        # else:
        #     zip_command = 'tar xvf {} -C {}'.format(src_file, dest_dir)
        #     print(zip_command)
        #     with open('tar_unpress.sh', mode='a+') as f:
        #         f.write(zip_command + '\n')
        #     # try:
            #     tar.extractall()
            # except RuntimeError as e:
            #     print(e)
        # tar.close()
        # else:
        #     print('file {} already existed'.format(dest_dir))



if __name__ == "__main__":
    path = '/home/tu-wan/windowswan/dataset/UCF_Crime/features/c3d/fc6/rgb'
    dirs = glob.glob(os.path.join(path, '*'))
    ziplist = []
    videolist = []
    for dir in dirs:
        feature_number = os.listdir(dir)
        if len(feature_number) >= 6250:
            videolist.append(dir)
            zips_dir = glob.glob(dir.replace('windowswan', 'windows4t').
                             replace('features/c3d/fc6/rgb', 'denseflow/*')+'/*')
            ziplist +=zips_dir
    with Pool(processes=4) as p:
        max_ = len(ziplist)
        with tqdm(total=max_) as pbar:
            for i, _ in tqdm(enumerate(p.imap_unordered(unzip_single, ziplist))):
                pbar.update()




    aa=1
