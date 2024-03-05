import cv2
import matplotlib.pyplot as plt
import numpy as np
import my_cv_func

pic_name = "tuzhijiance/ticket3.png"

kernel_pixel = 3
kernel = np.ones((kernel_pixel, kernel_pixel), np.uint8)

img = cv2.imread(pic_name)
# print(img.shape)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 高斯滤波
# gray = cv2.GaussianBlur(gray,(5,5),0)

# 开运算去掉背景的纹理
opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
# 二值化处理
thresh = cv2.threshold(opening, 110, 255, cv2.THRESH_BINARY)[1]
# 边缘检测
edge = cv2.Canny(opening, 80, 150)

res = np.hstack((gray, thresh, edge))
my_cv_func.show_pic("1", res)


# 轮廓检测 通过边缘
cnts_edge = cv2.findContours(edge.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
img2 = img.copy()
cv2.drawContours(img2, cnts_edge, -1, (0, 0, 255), 1)

# 轮廓检测 通过二值
cnts_thre = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
img3 = img.copy()
cv2.drawContours(img3, cnts_thre, -1, (0, 0, 255), 1)

# 比较了一下，二值化的轮廓比边缘检测轮廓更清晰一些
# 但是二值化通用性差一些
cnts = cnts_edge
# cnts = cnts_thre
# res = np.hstack((img2, img3))
# my_cv_func.show_pic("1", res)

# 只要覆盖面积最大的轮廓，reverse=True是从大到小排序
cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

# 轮廓边缘处理, 最简化矩形轮廓
for i in range(20):
    # 计算轮廓长度
    peri = cv2.arcLength(cnt, True)

    # 简化轮廓
    approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

    # 找到矩形的4个点
    if len(approx) == 4:
        print("Time:" + str(i))
        screenCnt = approx
        break

    cnt = approx

img4 = img.copy()
cv2.drawContours(img4, [screenCnt], -1, (0, 0, 255), 1)
res = np.hstack((img2, img3, img4))
my_cv_func.show_pic("1", res)

# 准备做透视变换，获取变换处的宽和高
# print(screenCnt)
# print(screenCnt.reshape(4,2))

tl = screenCnt[0][0]
tr = screenCnt[1][0]
br = screenCnt[2][0]
bl = screenCnt[3][0]

print(tl, tr, br, bl)

widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
maxWidth = max(int(widthA), int(widthB))


heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
maxHeight = max(int(heightA), int(heightB))

res_loc = np.array(
    [tl, tr, br, bl],
    dtype="float32",
)

dst_loc = np.array(
    [[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]],
    dtype="float32",
)

# 计算变换矩阵
M = cv2.getPerspectiveTransform(res_loc, dst_loc)
warped = cv2.warpPerspective(gray, M, (maxWidth, maxHeight))

# my_cv_func.show_pic("warped", warped)


cv2.imshow("img", img)
cv2.imshow("warped", warped)
cv2.waitKey(0)
cv2.destroyAllWindows()


# 给图纸加个bai边
result = cv2.copyMakeBorder(
    warped, 50, 50, 50, 50, cv2.BORDER_CONSTANT, value=(255, 255, 255)
)
my_cv_func.show_pic("result", result)

cv2.imwrite("tuzhijiance/result.png", result)
