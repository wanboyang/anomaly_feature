import zipfile
from PIL import Image
import io
import numpy
import cv2
import numpy as np
import time
import glob


# start1 = time.time()
# zip_file = 'D:/dataset/UCF_Crime/dense_flow/Abuse/Abuse001_x264/flow_x.zip'
# z = zipfile.ZipFile(zip_file)
# for i in range(len(z.namelist())):
#     file_in_zip = z.namelist()[i]
#     data = z.read(file_in_zip)
#     dataEnc = io.BytesIO(data)
#     # img = cv2.imread(dataEnc)
#     img = Image.open(dataEnc)
#     img = np.asarray(img)
#
#         # print(img.shape)
# end1 = time.time()
# time1 = end1 - start1
# print('ssd_zip_time: ',time1)
# start2 = time.time()
# img_files = glob.glob('D:/dataset/UCF_Crime/dense_flow/Abuse/Abuse001_x264/flow_x/*.jpg')
#
# for i in img_files:
#     img = Image.open(i)
#     img = np.asarray(img)
#
#     # print(img.shape)
# end2 = time.time()
# time2 = end2 - start2
# print('ssd_img_time: ',time2)


start3 = time.time()
zip_file = 'E:/test/Abuse001_x264/flow_x.zip'
z = zipfile.ZipFile(zip_file)
for i in range(len(z.namelist())):
    file_in_zip = z.namelist()[i]
    data = z.read(file_in_zip)
    dataEnc = io.BytesIO(data)
    # img = cv2.imread(dataEnc)
    img = Image.open(dataEnc)
    img = np.asarray(img)

        # print(img.shape)
end3 = time.time()
time3 = end3 - start3
print('hdd_zip_time: ',time3)


start4 = time.time()
img_files = glob.glob('E:/test/Abuse001_x264/flow_x/*.jpg')

for i in img_files:
    img = Image.open(i)
    img = np.asarray(img)

    # print(img.shape)
end4 = time.time()
time4 = end4 - start4
print('hdd_img_time: ',time4)