import os
import numpy as np
import glob
import shutil
from tqdm import tqdm
from multiprocessing import Pool

def move(filelist):
    [origin_file, target_file] = filelist
    mo_path,mo_name = os.path.split(target_file)
    if os.path.exists(mo_path) == 0:
        try:
            os.makedirs(mo_path)
        except:
            pass
    shutil.move(origin_file, target_file)

if __name__ == "__main__":
    # with open(file='/home/tu-wan/windowswan/dataset/UCF_Crime/denseflow_img/larger_video/larger_video.txt') as f:
    #     large_videos = f.readlines()
    #
    # large_video_clips_path = '/home/tu-wan/windowswan/dataset/UCF_Crime/denseflow_img/larger_video'
    # large_video_features_path = '/home/tu-wan/windowswan/dataset/UCF_Crime/features_video/i3d/larger'
    # for large_video in large_videos:
    #     videos_clips = glob.glob(os.path.join(large_video_clips_path, large_video.replace('\n', '')+'_*'))
    #     if videos_clips == []:
    #         continue
    #     videos_clips.sort(key=lambda x: int(x[-2:]))
    #     types = ['combine','rgb','flow']
    #     for t in types:
    #         tim = 0
    #         for videos_clip in videos_clips:
    #             clip_np = np.load(os.path.join(large_video_features_path, t, videos_clip.split('/')[-1], 'feature.npy'), allow_pickle=True)
    #             if tim == 0:
    #                 tmp_np = clip_np.copy()
    #                 tim += 1
    #             else:
    #                 tmp_np = np.concatenate((tmp_np, clip_np), axis=0)
    #
    #         save_path = os.path.join(large_video_features_path, t, large_video.replace('\n', ''))
    #         if os.path.exists(save_path) == 0:
    #             os.makedirs(save_path)
    #         np.save(os.path.join(save_path, 'feature.npy'),tmp_np)
    #         print('video {} combined'.format(large_video.replace('\n', '')))
    with open(file='/home/tu-wan/windowswan/dataset/UCF_Crime/larger_video/larger_video1.txt') as f:
        large_videos = f.readlines()

    large_video_clips_path = '/home/tu-wan/windowswan/dataset/UCF_Crime/denseflow_img/larger_video1/'
    file_list = []
    for large_video in large_videos:
        # if large_video != 'Normal_Videos331_x264\n':
        #     continue
        videos_clips = glob.glob(os.path.join(large_video_clips_path, large_video.replace('\n', '')+'_*'))
        # videos_clips = glob.glob(os.path.join(large_video_clips_path, large_video.replace('\n', '') + '*'))
        if videos_clips == []:
            continue
        videos_clips.sort(key=lambda x: int(x.split('_')[-1]))
        types = ['img']
        for t in types:
            count = 1
            save_path = os.path.join(large_video_clips_path, large_video.replace('\n', ''), t)
            if os.path.exists(save_path) == 0:
                os.makedirs(save_path)
            for videos_clip in videos_clips:
                frames = os.listdir(os.path.join(large_video_clips_path, videos_clip.split('/')[-1], t))
                frames.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))
                for frame in frames:
                    origin_file = os.path.join(large_video_clips_path, videos_clip.split('/')[-1], t, frame)
                    zill_len = len(frame.split('_')[-1].split('.')[0])
                    target_file = os.path.join(large_video_clips_path.replace('denseflow_img/larger_video1','denseflow_img_6250'), large_video.replace('\n',''), t, t.replace('flow_', '')+'_'+str(count).zfill(zill_len)+'.jpg')
                    # shutil.copyfile(origin_file, target_file)
                    file_list.append([origin_file, target_file])
                    count += 1
            print('video {} combined'.format(large_video.replace('\n', '')))
    with Pool(processes=6) as p:
        max_ = len(file_list)
        with tqdm(total=max_) as pbar:
            for i, _ in tqdm(enumerate(p.imap_unordered(move, file_list))):
                pbar.update()


