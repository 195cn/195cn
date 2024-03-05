import cv2
import matplotlib.pyplot as plt
import numpy as np

# 显示图片
def show_pic(name,img):
    print(img.shape)
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 限制图像宽度
def set_width(img,new_width):
    height, width = img.shape[:2]  

    if width > new_width or False:
        # 计算纵横比  
        aspect_ratio = height / width  
        # 根据纵横比计算新的高度  
        new_height = int(new_width * aspect_ratio)     
        # 使用resize函数缩放图片，同时保持纵横比  
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
        
    return img

# 创建和原图像尺寸一样的纯色图
def create_solid_color_image(img, color='black'):  
    # 获取图片的尺寸  
    height, width, _ = img.shape  
      
    # 根据选择的颜色创建纯色图片  
    if color.lower() == 'black':  
        solid_color_image = np.zeros((height, width, 3), dtype=np.uint8)  
    elif color.lower() == 'white':  
        solid_color_image = np.ones((height, width, 3), dtype=np.uint8) * 255  
    else:  
        raise ValueError("Invalid color. Please provide 'black' or 'white'.")  
      
    return solid_color_image  