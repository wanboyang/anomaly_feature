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

def video_split(file):
    file_avi = file_mp4.replace('.mp4', '.avi')
    # file_new = file_name.replace('.3gp', '.mp4')
    comm = 'ffmpeg -i {0} -strict -2 {1}'.format(file_mp4, file_avi)
    os.system(comm)
    print(file_mp4, 'has been convert to', file_avi)

if __name__ == "__main__":
    large_videos = []
    video_files = glob.glob('/home/tu-wan/windows4t/dataset/UCF_Crime/Video/Training_Normal_Videos_Anomaly/*.avi')
    video_names = []
    for video_file in video_files:
        video_names.append(os.path.split(video_file)[1])
    denseflow_dir = '/home/tu-wan/windowswan/dataset/UCF_Crime/denseflow_img/Training_Normal_Videos_Anomaly'
    existed_videos = os.listdir(denseflow_dir)
    for video_name in video_names:
        if video_name.replace('.avi', '') not in existed_videos:
            large_videos.append(video_name)




#     with Pool(processes=8) as p:
#         max_ = len(mp4_files)
#         with tqdm(total=max_) as pbar:
#             for i, _ in tqdm(enumerate(p.imap_unordered(converter, mp4_files))):
#                 pbar.update()
#
import string

import os
import time
import re
import math
import sys
from optparse import OptionParser
import subprocess

print("Test by gongjia start...")

parser = OptionParser()
parser.add_option("-i", "--input", dest="input", action="store_true", help="input x y for each file by user")
parser.add_option("-q", "--quality", dest="q", action="store", help="input xvid q arg", default="24")
parser.add_option("-v", "--vcodec", dest="vcodec", action="store", help="input video codec", default="x264")
parser.add_option("-n", "--noaudio", dest="an", action="store_true", help="no audio")
parser.add_option("-p", "--preset", dest="preset", action="store", help="", default="")
parser.add_option("-m", "--maxWidth", dest="maxWidth", action="store", help="input max width for output video",
                  default="")
parser.add_option("-f", "--fileType", dest="fileType", action="store", help="", default="mp4")
parser.add_option("-o", "--ogg", dest="ogg", action="store_true", help="user ogg instead of aac", default="")
parser.add_option("-3", "--mp3", dest="mp3", action="store_true", help="user mp3 instead of aac", default="")
parser.add_option("-1", "--pad", dest="pad", action="store_true", help="pad to 16:9", default="")
parser.add_option("-s", "--src", dest="srcD", action="store", help="source dir", default="/usr/local/src/test/videoin")
parser.add_option("-t", "--target", dest="targetD", action="store", help="target dir",
                  default="/usr/local/src/test/videoout")
parser.add_option("-w", "--workdir", dest="workdir", action="store", help="work dir",
                  default="/usr/local/src/test/video")
parser.add_option("-e", "--split", dest="split", action="store_true", help="split to multiple file with size")
parser.add_option("-d", "--splitsize", dest="splitsize", action="store", help="split to multiple file with size",
                  default="2")  # Minutes
parser.add_option("-j", "--prefix", dest="prefix", action="store", help="target file name prefix", default="")

(options, args) = parser.parse_args()

if options.srcD == None or options.srcD[0:1] == '-':
    print('srcD Err, quit')
    exit()
if options.targetD == None or options.targetD[0:1] == '-':
    print('targetD Err, quit')
    exit()
if options.fileType == None or options.fileType[0:1] == '-':
    print('fileType Err, quit')
    exit()
if options.workdir == None or options.workdir[0:1] == '-':
    print('workdir Err, quit')
    exit()

    # ??videoin????
for root, dirs, files in os.walk(options.srcD):
    for name in files:
        name = name.replace('[', '''\[''')  # ??????[????
        newname = name[0: name.rindex('.')]
        print("Test newname: " + newname)
        print("Test name: " + name)
        os.chdir(options.workdir)
        cmd = 'mkdir -p ffm;rm -f ffm/ffm.txt;/usr/local/src/ffmpeg-git-20181015-64bit-static/ffmpeg -i ' + options.srcD + '/' + name + ' >& ffm/ffm.txt;pwd'
        cmd1 = ['grep', 'Duration', 'ffm/ffm.txt']
        for i in cmd.split(';'):
            print
            i
            time.sleep(3)
            t1 = subprocess.Popen(i, shell=True)
        obj = subprocess.Popen(cmd1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (s1, s2) = obj.communicate()
        print
        s1
        reg = '''Duration\:\s(\d+)\:(\d+)\:([\d\.]+)'''
        result = re.compile(reg).findall(s1)
        print
        result
        for c in result:
            print
            'split file to', options.splitsize, 'minutes, Duration:', c[0], c[1], c[2]
            duration = int(c[0]) * 3600 + int(c[1]) * 60 + float(c[2])  ##????????s
            nameLength = int(math.log(int(duration / (int(options.splitsize) * 60))) / math.log(10)) + 1
            print
            nameLength
            for i in range(int(duration / (int(options.splitsize) * 60)) + 1):  ##??????????
                print
                i
                if duration > int(options.splitsize) * 60 * (i + 1):
                    _t = str(int(options.splitsize) * 60)
                else:
                    _t = str(duration - int(options.splitsize) * 60 * i)
                os.chdir(options.workdir)
                cmd = "touch ffm/output.log;/usr/local/src/ffmpeg-git-20181015-64bit-static/ffmpeg -y -i " + options.srcD + "/" + name + " -codec: copy -ss " + str(
                    i * int(
                        options.splitsize) * 60) + " -t " + _t + " " + options.targetD + "/" + options.prefix + newname + '_' + string.replace(
                    ('%' + str(nameLength) + 's') % str(i), ' ', '0') + "." + options.fileType + ' >& ffm/output.log'
                for i in cmd.split(';'):
                    print
                    i
                    time.sleep(2)
                    t1 = subprocess.Popen(i, shell=True)
                    print
#                     t1
#
# time.sleep(3)