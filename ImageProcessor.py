import cv2
import numpy as np
from PIL import Image,ImageTk
class ImgProcessor:
    #def __init__(self):
        
    def init_img(self,img):
        if img is None:
            return
        a=1
        b=0
        img_array = self.getArray(img)
        # new_img_array = np.clip(a * img_array + b, 0, 255).astype(np.uint8)
        new_img_array = self.linearChange(a,b,img_array)
        return Image.fromarray(new_img_array)
        
    
    def getArray(self,img)->np.ndarray:
        return np.array(img)
    
    def linearChange(self,a,b,img_array):
        return np.clip(a * img_array + b, 0, 255).astype(np.uint8)