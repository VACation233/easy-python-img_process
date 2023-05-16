import cv2
import numpy as np
from PIL import Image,ImageTk,ImageOps

class ImgProcessor:
    #def __init__(self):
    def change_To_Gray(self,img):
        img=img.convert('L')
        
        
        return img
        
    def init_img(self,img):
        if img is None:
            return
        a=1
        b=0
        img_array = self.getArray(img)
        # new_img_array = np.clip(a * img_array + b, 0, 255).astype(np.uint8)
        new_img_array = self.Get_linearChange_arr(a,b,img_array)
        
        return Image.fromarray(new_img_array)
        
    
    def getArray(self,img)->np.ndarray:
        return np.array(img)
    
    def Get_linearChange_arr(self,a,b,img_array):
        return np.clip(a * img_array + b, 0, 255).astype(np.uint8)
    
    def Get_equlizedChange_arr(self,img):
        #传入参数要求是Img图片
        img_eq=ImageOps.equalize(img)
        
        return self.getArray(img_eq)
    
    def Get_Fourie_arr(self,img):
        f=np.fft.fft2(img)
        fshift=np.fft.fftshift(f)
        return 20*np.log(np.abs(fshift))