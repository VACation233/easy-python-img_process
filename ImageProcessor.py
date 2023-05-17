import cv2
import numpy as np
from PIL import Image,ImageTk,ImageOps,ImageFilter

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
    
    def GetImageFromArray(self,img_array):
        img_array = img_array.astype(np.uint8)

        return Image.fromarray(img_array)
    
    #添加噪点
    def add_gaussian_noise(self,img,mean=0,std=1)->np.ndarray:
        img=np.array(img)
        noise=np.random.normal(mean,std,img.shape)#可能会失效
        noisy_img_array=img+noise
        noisy_img_array=np.clip(noisy_img_array,0,255)
        return noisy_img_array
    #添加模糊
    def add_motion(self,img,radius=0):
        img = img.filter(ImageFilter.GaussianBlur(radius=5))
        new_array=self.getArray(img)
        return new_array
    
    def hight_pass_filter(self,img,factor=0):
        kernel = np.array([[0, -1, 0], [-1, 4 + factor, -1], [0, -1, 0]])
        array=self.getArray(img)
        img = cv2.filter2D(array, -1, kernel)
        
        new_array=self.getArray(img)
        return new_array
    
    def low_pass_filter(self,image, kernel_size=3):
        array=self.getArray(image)
        kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size ** 2)
        filtered_image = cv2.filter2D(array, -1, kernel)
        new_array=self.getArray(filtered_image)
        return new_array

