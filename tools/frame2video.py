import cv2
import os
from tqdm import tqdm
from multiprocessing import Pool

def img2video(imgpath):
    video = imgpath.replace('frames','test_video') + '.avi'
    if os.path.exists(os.path.split(video)[0]) == 0:
        os.makedirs(os.path.split(video)[0])
    img_list = os.listdir(imgpath)
    img_list.sort(key=lambda t: int(t[:t.index('.')]))

    [video_w, video_h, _] = cv2.imread(os.path.join(imgpath, img_list[0])).shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    vw = cv2.VideoWriter(video, fourcc, 25, (video_h, video_w))

    for img in img_list:
        frame = cv2.imread(imgpath + '/' + img)  # any depth, cus default 8bit
        vw.write(frame)
        # print('write', img)

    vw.release()

def precess_path(frame_path):
    frame_dirs = os.listdir(frame_path)
    test_frame_dirs = []
    for frame_dir in frame_dirs:
        if len(frame_dir) == 7:
            test_frame_dirs.append(os.path.join(frame_path, frame_dir))
    return test_frame_dirs

if __name__ == '__main__':
    debug = False
    frame_path = '/home/tu-wan/windowswan/dataset/shanghaitech/frames'
    frame_dirs = precess_path(frame_path)
    if debug:
        for frame_dir in frame_dirs:
            img2video(imgpath = frame_dir)
    else:
        with Pool(processes=4) as p:
            max_ = len(frame_dirs)
            with tqdm(total=max_) as pbar:
                for i, _ in tqdm(enumerate(p.imap_unordered(img2video, frame_dirs))):
                    pbar.update()
