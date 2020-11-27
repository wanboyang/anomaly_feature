# coding:utf-8

import numpy as np
import os
import glob

# def getframeGTScore(gtpath,key):
#     nyfile = os.path.join(gtpath,key+'.npy')
#     framegt = np.load(nyfile)
#
#     return framegt

def main(original_video_dict,dataset,dataset_mode):

    if os.path.exists('./{}/{}'.format(dataset, dataset_mode)) == 0:
        os.makedirs('./{}/{}'.format(dataset, dataset_mode))


    with open(file='./{}/{}/flownet_list.txt'.format(dataset, dataset_mode), mode='w', encoding='utf-8') as flo:
        with open(file='./{}/{}/label.txt'.format(dataset,dataset_mode),mode='w',encoding='utf-8') as t:
            for k, v in original_video_dict.items():
                frames = glob.glob(os.path.join(v, 'x', '*.png'))
                frames_number = int(len(frames))
                framegt = np.zeros(shape=(frames_number), dtype='int8')
                classgt = np.zeros(shape=(frames_number), dtype='int8')
                for i in range(0, frames_number, 1):
                    flo.write(os.path.join(v, 'x', str(i).zfill(6) + '.png'+':'))
                    flo.write(os.path.join(v, 'y', str(i).zfill(6) + '.png' + '\n'))
                    t.write(str(framegt[i-1])+':'+str(classgt[i-1])+'\n')
                # for i in range(0, len(frames), 2):
                #     f.write(os.path.join(Framepath.replace('../../../','../../'),k,frames[i]+'\n'))
                #     # f.write(os.path.join(Framepath,k,frames[i]+'\n'))
                #     t.write(str(framegt[i])+':'+str(classgt[i])+'\n')
                # for i in range(0, len(frames), 3):
                #     f.write(os.path.join(Framepath.replace('../../../','../../'),k,frames[i]+'\n'))
                #     # f.write(os.path.join(Framepath,k,frames[i]+'\n'))
                #     t.write(str(framegt[i])+':'+str(classgt[i])+'\n')
                # for i in range(0, len(frames), 4):
                #     f.write(os.path.join(Framepath.replace('../../../','../../'),k,frames[i]+'\n'))
                #     # f.write(os.path.join(Framepath,k,frames[i]+'\n'))
                #     t.write(str(framegt[i])+':'+str(classgt[i])+'\n')

if __name__ == '__main__':
    dataset = 'shanghaitech'
    dataset_mode = 'all'
    original_video = []
    original_video_dict = {}
    # original_test_video = []
    videopath = '/home/tu-wan/windows4t/dataset/shanghaitech/flownetxy/'.format(dataset)
    videonames = os.listdir(videopath)
    for videoname in videonames:
        original_video_dict[videoname] = os.path.join(videopath, videoname)
    if os.path.exists('./{}_flownet/{}'.format(dataset, dataset_mode)) == 0:
        os.makedirs('./{}_flownet/{}'.format(dataset, dataset_mode))
    np.savetxt('./{}_flownet/{}/videoname.txt'.format(dataset, dataset_mode), np.asarray(videonames).reshape(-1),fmt='%s')

    dataset = '{}_flownet'.format(dataset)
    main(original_video_dict=original_video_dict,
         dataset=dataset,
         dataset_mode=dataset_mode)


