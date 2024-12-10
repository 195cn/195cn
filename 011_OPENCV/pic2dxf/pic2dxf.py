import cv2
import matplotlib.pyplot as plt
import numpy as np
import my_cv_func
from ezdxf import new  
from ezdxf.entities import LWPolyline  

# 这个适合不同色块的pic1.png，需要大对比度

INPUT_NAME = 'input/pic7.png'
OUTPUT_NAME = 'output/pic7.dxf'


pic_name = INPUT_NAME

img=cv2.imread(pic_name)
# img=cv2.imread(pic_name,cv2.IMREAD_GRAYSCALE)
# img = my_cv_func.set_width(img,400)
origin = img.copy()

# 转为灰度图
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  

# 开运算 先腐蚀后膨胀
kernel_pixel = 3
kernel = np.ones((kernel_pixel,kernel_pixel),np.uint8)
gray = cv2.morphologyEx(gray,cv2.MORPH_OPEN,kernel)
# my_cv_func.show_pic('open',img)

# 转换二值图像
ret,thresh = cv2.threshold(gray,110,255,cv2.THRESH_BINARY)

# 提取轮廓
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

# 把红色标记画回原来的彩图
cv2.drawContours(img,contours,-1,(0,0,255),2)

res = np.hstack((gray,thresh))
my_cv_func.show_pic('res',res)

res = np.hstack((origin,img))
my_cv_func.show_pic('res',res)


# 创建一个新的 DXF 文档  
doc = new("R2010")  
msp = doc.modelspace()  


# 将每个轮廓添加到 DXF 文档中  
for contour in contours:  

    # OpenCV 返回的轮廓是由一系列点组成的，每个点包含 (x, y) 坐标  
    # 我们需要将这些点转换为 DXF 所需的格式  
    dxf_points = [(point[0][0], - point[0][1]) for point in contour]  
      
    # 在 DXF 文档中创建 LWPOLYLINE 实体来表示轮廓  
    # 检查轮廓是否闭合，如果是，则闭合它  
    if len(dxf_points) > 2 and dxf_points[0] != dxf_points[-1]:  
        dxf_points.append(dxf_points[0])  

    msp.add_lwpolyline(points=dxf_points)  


# 保存 DXF 文件  
doc.saveas(OUTPUT_NAME)