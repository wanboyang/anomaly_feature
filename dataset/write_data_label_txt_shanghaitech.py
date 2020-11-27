# coding:utf-8

import numpy as np
import os

def getframeGTScore(gtpath,key):
    nyfile = os.path.join(gtpath,key+'.npy')
    framegt = np.load(nyfile)

    return framegt

def main(Trainvideolist,Testvideolist,Framepath,GTPath,dataset,dataset_mode):
    with open(file=Trainvideolist,mode='r') as f:
        videolist = f.readlines()
        trainvideodict = {}
        for v in videolist:
            v = v.replace('\n','')
            trainvideodict[v] = os.path.join(Framepath,v)
    with open(file=Testvideolist,mode='r') as f:
        videolist = f.readlines()
        testvideodict = {}
        for v in videolist:
            v = v.replace('\n','')
            testvideodict[v] = os.path.join(Framepath,v)
    if os.path.exists('./{}/{}'.format(dataset,dataset_mode)) == 0:
        os.makedirs('./{}/{}'.format(dataset,dataset_mode))

    with open(file='./{}/{}/trainlist.txt'.format(dataset,dataset_mode),mode='w',encoding='utf-8') as f:
        with open(file='./{}/{}/trainlabel.txt'.format(dataset,dataset_mode),mode='w',encoding='utf-8') as t:
            for k,v in trainvideodict.items():
                frames = os.listdir(v)
                frames.sort(key=lambda x: int(x[:-4]))
                if len(k) == 7:
                    framegt = getframeGTScore(gtpath=GTPath,key=k)
                elif len(k) == 6:
                    framegt = np.zeros(shape=(len(frames)),dtype='int8')
                else:
                    print('Videoname_error')
                    exit()
                classgt = np.ones(shape=(len(frames)),dtype='int8')*int(k.split('_')[0])-1
                for i in range(0, len(frames), 1):
                    f.write(os.path.join(Framepath.replace('../../../','../../'),k,frames[i]+'\n'))
                    # f.write(os.path.join(Framepath,k,frames[i]+'\n'))
                    t.write(str(framegt[i])+':'+str(classgt[i])+'\n')
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

    with open(file='./{}/{}/testlist.txt'.format(dataset, dataset_mode),mode='w',encoding='utf-8') as f:
        with open(file='./{}/{}/testlabel.txt'.format(dataset, dataset_mode),mode='w',encoding='utf-8') as t:
            for k,v in testvideodict.items():
                frames = os.listdir(v)
                frames.sort(key=lambda x: int(x[:-4]))
                if len(k) == 7:
                    framegt = getframeGTScore(gtpath=GTPath,key=k)
                elif len(k) == 6:
                    framegt = np.zeros(shape=(len(frames)),dtype='int8')
                else:
                    print('Videoname_error')
                    exit()
                classgt = np.ones(shape=(len(frames)),dtype='int8')*int(k.split('_')[0])-1
                for i in range(len(frames)):
                    f.write(os.path.join(Framepath.replace('../../../','../../'),k,frames[i]+'\n'))
                    # f.write(os.path.join(Framepath,k,frames[i]+'\n'))
                    t.write(str(framegt[i])+':'+str(classgt[i])+'\n')
    # with open(file='./{}/{}//testlist_5frames.txt'.format(dataset, dataset_mode),mode='w',encoding='utf-8') as f:
    #     with open(file='./{}/{}//testlabel_5frames.txt'.format(dataset, dataset_mode),mode='w',encoding='utf-8') as t:
    #         for k,v in testvideodict.items():
    #             frames = os.listdir(v)
    #             frames.sort(key=lambda x: int(x[:-4]))
    #             if len(k) == 7:
    #                 framegt = getframeGTScore(gtpath=GTPath,key=k)
    #             elif len(k) == 6:
    #                 framegt = np.zeros(shape=(len(frames)),dtype='int8')
    #             else:
    #                 print('Videoname_error')
    #                 exit()
    #             classgt = np.ones(shape=(len(frames)),dtype='int8')*int(k.split('_')[0])-1
    #             for i in range(0,len(frames),4):
    #                 f.write(os.path.join(Framepath.replace('../../../','../../'),k,frames[i]+'\n'))
    #                 # f.write(os.path.join(Framepath,k,frames[i]+'\n'))
    #                 t.write(str(framegt[i])+':'+str(classgt[i])+'\n')




if __name__ == '__main__':
    dataset_mode = 'unary'
    original_train_video = []
    original_test_video = []
    videopath = '/home/tu-wan/windowswan/dataset/shanghaitech/frames'
    videonames = os.listdir(videopath)
    for videoname in videonames:
        if len(videoname) == 6:
            original_train_video.append(videoname)
        else:
            original_test_video.append(videoname)
    if os.path.exists('./shanghaitech_224/{}'.format(dataset_mode)) == 0:
        os.makedirs('./shanghaitech_224/{}'.format(dataset_mode))
    np.savetxt('./shanghaitech_224/{}/SH_Train.txt'.format(dataset_mode), np.asarray(original_train_video),fmt='%s')
    np.savetxt('./shanghaitech_224/{}/SH_Test.txt'.format(dataset_mode), np.asarray(original_test_video), fmt='%s')
    Trainvideolist = './shanghaitech_224/{}/SH_Train.txt'.format(dataset_mode)
    Testvideolist = './shanghaitech_224/{}/SH_Test.txt'.format(dataset_mode)
    Framepath = '/home/tu-wan/windowswan/dataset/shanghaitech/frames'
    GTPath = '../../../dataset/shanghaitech/gt/frame_mask'
    dataset = 'shanghaitech_224'
    main(Trainvideolist=Trainvideolist,
         Testvideolist=Testvideolist,
         Framepath=Framepath,
         GTPath=GTPath,
         dataset=dataset,
         dataset_mode=dataset_mode)


