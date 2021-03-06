# 将某一文件夹下的jpg文件，等比例缩小到某宽度一下
# 每次上传新图片都应该运行一次
# create time   :   2022/4/3
# author        :   195
# version       :   1.0

import numpy as np
import os
import cv2

def resize_pic(file, max_width):
    # 读取图片及尺寸
    img = cv2.imread(file)
    w = img.shape[1]
    h = img.shape[0]
    print(w, h)

    # 判断是否超过尺寸
    if w <= max_width:
        print("Don't need resize")
        return

    # 按比例缩放尺寸
    h = int(h * (max_width / w))
    w = max_width
    print(w, h)
    img = cv2.resize(img, (w, h))
    cv2.imwrite(file, img)

def rename(file):
    if RENAME_FLAG:
        temp_name = file.replace(" ", "").replace("(", "").replace(")", "")
        os.rename(file, temp_name)

    pass


DIR = "./"
RENAME_FLAG = True

# 获取文件夹下所有文件
path = os.path.join(DIR)
img_list = os.listdir(path)
# print(img_list)

# 遍历所有图片
for i in img_list:
    # print(i)
    end_str = os.path.splitext(i)[1]
    if end_str == ".jpg" or end_str == ".jpeg":
        print(DIR + i)
        # img = cv2.imread(DIR + i)
        # cv2.imshow("", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        resize_pic(DIR+i, 400)
        rename(DIR+i)
