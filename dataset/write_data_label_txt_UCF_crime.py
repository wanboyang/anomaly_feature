# coding:utf-8

import numpy as np
import os

def getframeGTScore(gtpath,key):
    nyfile = os.path.join(gtpath,key+'.npy')
    framegt = np.load(nyfile)

    return framegt

def creatdict(framepath, GTfile):
    with open(file=GTfile,mode='r') as f:
        gtfile = f.readlines()
    test_video_list = []
    for gt in gtfile:
        gt_split = gt.split('  ')
        test_video_list.append(gt_split[0].replace('.mp4',''))
    videoclasses = os.listdir(framepath)

    video_dict = {}
    for videoclass in videoclasses:
        videos = os.listdir(os.path.join(framepath, videoclass))
        for video in videos:
            video_dict[video] = os.path.join(framepath, videoclass, video)
    train_video_dict = {}
    test_video_dict = {}
    for k,v in video_dict.items():
        if k in test_video_list:
            test_video_dict[k] = v
        else:
            train_video_dict[k] = v
    return train_video_dict, test_video_dict

def main(Trainvideolist,Testvideolist,GTPath,dataset,dataset_mode,train_video_dict, test_video_dict):
    with open(file=Trainvideolist,mode='r') as f:
        videolist = f.readlines()
        trainvideodict = {}
        for v in videolist:
            v = v.replace('\n','')
            trainvideodict[v] = train_video_dict[v]
    with open(file=Testvideolist,mode='r') as f:
        videolist = f.readlines()
        testvideodict = {}
        for v in videolist:
            v = v.replace('\n','')
            testvideodict[v] = test_video_dict[v]
    if os.path.exists('./{}/{}'.format(dataset,dataset_mode)) == 0:
        os.makedirs('./{}/{}'.format(dataset,dataset_mode))
    with open(file='./{}/{}/trainlist.txt'.format(dataset,dataset_mode),mode='w',encoding='utf-8') as f:
        with open(file='./{}/{}/trainlabel.txt'.format(dataset,dataset_mode),mode='w',encoding='utf-8') as t:
            for k,v in trainvideodict.items():
                frames = os.listdir(v)
                frames.sort(key=lambda x: int(x[:-4]))
                framegt = np.zeros(shape=(len(frames)),dtype='int8')
                classgt = np.zeros(shape=(len(frames)),dtype='int8')
                for i in range(0, len(frames), 1):
                    f.write(os.path.join(v,frames[i]+'\n'))
                    # f.write(os.path.join(Framepath,k,frames[i]+'\n'))
                    t.write(str(framegt[i])+':'+str(classgt[i])+'\n')
                # for i in range(0, len(frames), 2):
                #     f.write(os.path.join(v, frames[i] + '\n'))
                #     # f.write(os.path.join(Framepath,k,frames[i]+'\n'))
                #     t.write(str(framegt[i]) + ':' + str(classgt[i]) + '\n')
                # for i in range(0, len(frames), 3):
                #     f.write(os.path.join(v, frames[i] + '\n'))
                #     # f.write(os.path.join(Framepath,k,frames[i]+'\n'))
                #     t.write(str(framegt[i]) + ':' + str(classgt[i]) + '\n')
                # for i in range(0, len(frames), 4):
                #     f.write(os.path.join(v, frames[i] + '\n'))
                #     # f.write(os.path.join(Framepath,k,frames[i]+'\n'))
                #     t.write(str(framegt[i]) + ':' + str(classgt[i]) + '\n')

    with open(file='./{}/{}/testlist.txt'.format(dataset, dataset_mode),mode='w',encoding='utf-8') as f:
        with open(file='./{}/{}/testlabel.txt'.format(dataset, dataset_mode),mode='w',encoding='utf-8') as t:
            for k,v in testvideodict.items():
                frames = os.listdir(v)
                frames.sort(key=lambda x: int(x[:-4]))
                framegt = getframeGTScore(gtpath=GTPath, key=k)
                classgt = np.zeros(shape=(len(frames)),dtype='int8')
                for i in range(len(frames)):
                    f.write(os.path.join(v,frames[i]+'\n'))
                    # f.write(os.path.join(Framepath,k,frames[i]+'\n'))
                    t.write(str(framegt[i])+':'+str(classgt[i])+'\n')
    # with open(file='./{}/{}/testlist_5frames.txt'.format(dataset, dataset_mode),mode='w',encoding='utf-8') as f:
    #     with open(file='./{}/{}/testlabel_5frames.txt'.format(dataset, dataset_mode),mode='w',encoding='utf-8') as t:
    #         for k,v in testvideodict.items():
    #             frames = os.listdir(v)
    #             frames.sort(key=lambda x: int(x[:-4]))
    #             framegt = getframeGTScore(gtpath=GTPath, key=k)
    #             classgt = np.zeros(shape=(len(frames)),dtype='int8')
    #             for i in range(0, len(frames), 4):
    #                 f.write(os.path.join(v,frames[i]+'\n'))
    #                 # f.write(os.path.join(Framepath,k,frames[i]+'\n'))
    #                 t.write(str(framegt[i])+':'+str(classgt[i])+'\n')
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
    framespath = '/home/tu-wan/windows4t/dataset/UCF_Crime/Frame'
    dataset_mode = 'unary'
    gttxt = '/home/tu-wan/windowswan/dataset/UCF_Crime/GT/Txt_formate/Temporal_Anomaly_Annotation.txt'
    gt_np_dir = os.path.split(gttxt)[0].replace('Txt_formate', 'Numpy_formate')
    train_video_dict, test_video_dict = creatdict(framepath=framespath, GTfile=gttxt)

    original_train_video = []
    original_test_video = []
    for k, v in test_video_dict.items():
            original_test_video.append(k)
    if dataset_mode == 'unary':
        for k,v in train_video_dict.items():
            if k.find('Normal') != -1:
                original_train_video.append(k)
    else:
        for k,v in train_video_dict.items():
            original_train_video.append(k)

    if os.path.exists('./UCF_Crime_224/{}'.format(dataset_mode)) == 0:
        os.makedirs('./UCF_Crime_224//{}'.format(dataset_mode))
    np.savetxt('./UCF_Crime_224/{}/Train.txt'.format(dataset_mode), np.asarray(original_train_video),fmt='%s')
    np.savetxt('./UCF_Crime_224/{}/Test.txt'.format(dataset_mode), np.asarray(original_test_video), fmt='%s')
    Trainvideolist = './UCF_Crime_224/{}/Train.txt'.format(dataset_mode)
    Testvideolist = './UCF_Crime_224/{}/Test.txt'.format(dataset_mode)
    GTPath = gt_np_dir
    dataset = 'UCF_Crime_224'
    main(Trainvideolist=Trainvideolist,
         Testvideolist=Testvideolist,
         GTPath=GTPath,
         dataset=dataset,
         dataset_mode=dataset_mode,
         train_video_dict=train_video_dict,
         test_video_dict=test_video_dict)


