#-*- coding:utf-8 -*-
from multiprocessing import Pool, cpu_count, current_process
import os
import platform
import cv2
# print(cv2.__version__)
import glob
import time
from tqdm import tqdm
def readVideolist(Train,Test):
    TrainAnomalyClass=os.listdir(Train)
    TestAnomalyClass=os.listdir(Test)
    TrainvideoList={}
    TestvideoList={}
    for a_class in TrainAnomalyClass:
        TrainvideoDir=os.path.join(Train, a_class)
        TrainvideoName=os.listdir(TrainvideoDir)
        TestvideoDir=os.path.join(Test, a_class)
        TestvideoName=os.listdir(TestvideoDir)
        for video in TrainvideoName:
            TrainvideoPath=os.path.join(TrainvideoDir,video)
            TrainvideoList[video]=TrainvideoPath
        for video in TestvideoName:
            TestvideoPath=os.path.join(TestvideoDir,video)
            TestvideoList[video]=TestvideoPath

    return TrainvideoList,TestvideoList

def readVideolist2(Train,Test):

    Trainvideos = os.listdir(Train)
    Testvideos = os.listdir(Test)
    TrainvideoList={}
    TestvideoList={}
    for video in Trainvideos:
        TrainvideoPath = os.path.join(Train, video)
        TrainvideoList[video] = TrainvideoPath
    for video in Testvideos:
        TestvideoPath = os.path.join(Test, video)
        TestvideoList[video] = TestvideoPath

    return TrainvideoList,TestvideoList

def readVideolist3(Train):

    Trainvideos = os.listdir(Train)

    TrainvideoList={}

    for video in Trainvideos:
        TrainvideoPath = os.path.join(Train, video)
        TrainvideoList[video] = TrainvideoPath

    return TrainvideoList


def readVideolist_UCF_Crime(Path):

    Class = os.listdir(Path)
    videoList={}
    for a_class in Class:
        videoDir=os.path.join(Path, a_class)
        videoNames=os.listdir(videoDir)
        for video in videoNames:
            videoPath=os.path.join(videoDir,video)
            videoList[a_class+video]=videoPath


    return videoList


def Video2frame(videofilelist=None):
    # for each_video in videofilelist:
        each_video = videofilelist
        current_os = platform.architecture()
        start = time.clock()
        # print(videofilelist)
        if current_os[1] == 'WindowsPE':
            each_videolist = each_video.split('\\')
            each_video_path, each_video_name = os.path.split(each_video)
        else:
            each_videolist = each_video.split('/')
            each_video_path, each_video_name = os.path.split(each_video)
        each_video_name, _ = each_video_name.split('.')
        each_video_name = str(each_video_name)
        target_path = os.path.join(each_video_path.replace('videos/training','frames_224'),each_video_name)
        # target_path = target_path.replace('windows4t','windowswan')
        if os.path.exists(target_path):
            print('视频 {} 视频帧已存在'.format(each_video_name))
        else:
            framedirsavepath = target_path
            if os.path.exists(framedirsavepath) == 0:
                os.makedirs(framedirsavepath)
            cap = cv2.VideoCapture(each_video)
            frame_count = 1
            success = True
            while(success):
                success, frame = cap.read()
                # print ('Read a new frame: ', success)
                if success:
                    # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
                    # frame = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_CUBIC)
                    cv2.imwrite(framedirsavepath + '/'+"{}.jpg" .format(frame_count), frame)

                    # print ('frame_num:',frame_count)
                    frame_count = frame_count + 1
                else:
                    print('准备分割下一视频')
                    end = time.clock()
                    t = end - start
                    print("'视频 {} 分割时间为 ：".format(each_video_name), t)
                    break

            cap.release()

if __name__ == "__main__":
    current_os = platform.architecture()
    # if current_os [1] == 'WindowsPE':
    #     TrainSetpath='E:\\anomaly detection\dataset\ARD\ARD_Videos\\train\\'
    #     TestSetPath ='E:\\anomaly detection\dataset\ARD\ARD_Videos\\test\\'
    #     TrainFramepath='J:\\dataset\\ARD\\ARD_Frames_origin\\training\\'
    #     TestFramePath ='J:\\dataset\\ARD\\ARD_Frames_origin\\testing\\'
    #     framesavepath = TrainFramepath
    #     framesavepath1= TestFramePath
    # elif current_os[1] == 'ELF':
    #     TrainSetpath='/home/tu-wan/windowspan/dataset/ARD/ARD_Videos/training/'
    #     TestSetPath ='/home/tu-wan/windowspan/dataset/ARD/ARD_Videos/testing/'
    #     TrainFramepath='/home/tu-wan/windowswan/dataset/ARD/ARD_Frames/training/'
    #     TestFramePath ='/home/tu-wan/windowswan/dataset/ARD/ARD_Frames/testing/'
    #     framesavepath = TrainFramepath
    #     framesavepath1= TestFramePath

    ##TrainSetpath='/home/tu-wan/windowswan/dataset/Avenue/Videos/training_videos/'
    #TestSetPath ='/home/tu-wan/windowswan/dataset/Avenue/Videos/testing_videos/'
    #TrainFramepath='/home/tu-wan/windowswan/dataset/Avenue/Frame/Training/'
    #TestFramePath ='/home/tu-wan/windowswan/dataset/Avenue/Frame/Testing/'
    #framesavepath='/home/tu-wan/windowswan/dataset/Avenue/Frame/Training/'
    #framesavepath1='/home/tu-wan/windowswan/dataset/Avenue/Frame/Testing/'

    # TrainSetpath1='/home/tu-wan/windowswan/dataset/Avenue/Videos/training_videos/'
    # TestSetPath1 ='/home/tu-wan/windowswan/dataset/Avenue/Videos/testing_videos/'
    # TrainFramepath1='/home/tu-wan/windowswan/dataset/Avenue/Frame/Training/'
    # TestFramePath1 ='/home/tu-wan/windowswan/dataset/Avenue/Frame/Testing/'
    # framesavepath11 = TrainFramepath1
    # framesavepath111 = TestFramePath1
    #
    # TrainSetpath2='/home/tu-wan/windowswan/dataset/Avenue/Videos/training_videos/'
    # TestSetPath2 ='/home/tu-wan/windowswan/dataset/Avenue/Videos/testing_videos/'
    # TrainFramepath2='/home/tu-wan/windowswan/dataset/Avenue/Frame/Training/'
    # TestFramePath2 ='/home/tu-wan/windowswan/dataset/Avenue/Frame/Testing/'
    # framesavepath2='/home/tu-wan/windowswan/dataset/Avenue/Frame/Training/'
    # framesavepath12='/home/tu-wan/windowswan/dataset/Avenue/Frame/Testing/'
    #
    #
    # UCFSetpath='/home/tu-wan/windowswan/dataset/UCF Crime/Videos/'
    #
    # UCFFramepath='/home/tu-wan/windowswan/dataset/UCF Crime/Frame/'
    #
    # framesavepath = UCFFramepath
    TrainSetpath='/home/tu-wan/windowswan/dataset/shanghaitech/videos/test_video'
    TrainvideoList = readVideolist3(TrainSetpath)

    # TrainFrameList, TestFrameList = readVideolist(TrainFramepath, TestFramePath)
    train_values = list(TrainvideoList.values())
    # trainframe_keys = list(TrainFrameList.keys())
    # testframe_keys = list(TestFrameList.keys())
    # Video2frame(videofilelist=train_values, framefilelist=trainframe_keys, savepath=framesavepath)
    with Pool(processes=12) as p:
        max_ = len(train_values)
        with tqdm(total=max_) as pbar:
            for i, _ in tqdm(enumerate(p.imap_unordered(Video2frame, train_values))):
                pbar.update()


    # Video2frame(videofilelist=test_values, framefilelist=testframe_keys, savepath=framesavepath1)

#
