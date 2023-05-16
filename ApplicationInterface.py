
import tkinter as tk
from PIL import Image,ImageTk,ImageEnhance
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from ImageProcessor import ImgProcessor
import os
import copy

class AppInterface:
    def __init__(self,master,originImage,parentWindow):
        
        self.imgProcessor=ImgProcessor()
        self.master=master
        self.master.geometry('1000x600')
        self.master.title("Histogram and Linear change")
        self.originImage=originImage
        self.changedImage=None
        self.parentWindow=parentWindow
        
        
        
        
    def init_mainWindow(self):
        #创建 matplotlib图形
        self.fig=Figure(figsize=(6,4),dpi=100)
        self.ax1=self.fig.add_subplot(2,1,1)
        self.ax2=self.fig.add_subplot(2,1,2)
        
        #将matplotlib放入tinker里面
        self.canvas=FigureCanvasTkAgg(self.fig,master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        
        #创建文件选择按钮
        self.load_button=tk.Button(self.master,text="选择图像",command=self.load_image)
        self.load_button.pack(side=tk.LEFT,padx=10,pady=10)
        #创建线性变换处理按钮
        self.linearProcess_button=tk.Button(self.master,text='线性变换',command=self.create_linearProcess_window)
        self.linearProcess_button.pack(side=tk.LEFT,padx=10,pady=10)
        #创建傅里叶变换处理按钮
        self.fourierTransform_button=tk.Button(self.master,text='傅里叶变换',command=self.create_FourierTransform_window)
        self.fourierTransform_button.pack(side=tk.LEFT,padx=10,pady=10)
        # #创建滑块
        # self.silder_label=tk.Label(self.master,text="Contrast: ")
        # self.silder_label.pack(side=tk.LEFT,padx=10,pady=10)
        # self.silder=tk.Scale(self.master,from_=0.0,to=2.0,resolution=0.01,orient=tk.HORIZONTAL,command=self.update_histogram)
        # self.silder.set(1.0)
        # self.silder.pack(side=tk.LEFT,padx=10,pady=10)
        
    def load_image(self):
        file_path=filedialog.askopenfilename()
        if file_path:
            
            self.originImage=Image.open(file_path).convert('RGB')
            #self.imgProcessor.load_img(self.img,self.ax1)
            # self.changedImage=self.imgProcessor.init_img(self.originImage)
            self.init_histogram()
            
    def init_histogram(self):
        if self.originImage is None:
            return
        self.ax1.clear()
        self.ax1.imshow(self.originImage)
        self.ax1.set_title("Changed Image")
        self.ax2.clear()
        #直接声明类型
        originImage_arr:np.ndarray=self.imgProcessor.getArray(self.originImage)
        self.ax2.hist(originImage_arr.ravel(),bins=256)
        self.ax2.set_title('Histogram')
        self.canvas.draw()
            
    def saveImg(self,title):
        if self.changedImage is None:
            return
        filePath=filedialog.askdirectory()
        if filePath is None:
            return
        # image_format=self.changedImage.format
        # if image_format=='JPEG':
        #     file_extension='.jpg'
        # elif image_format=='PNG':
        #     file_extension='.png'
        # else:
        #     file_extension='.'+image_format.lower()
        
        savePath=os.path.join(os.path.abspath(filePath),title+'_changed_img.jpg')
        self.changedImage.save(savePath)
        
    def change_To_Gray(self):
        if self.changedImage is None:
            return
        
        self.changedImage=self.imgProcessor.change_To_Gray(self.changedImage)
        new_array=self.imgProcessor.getArray(self.changedImage)
        self.ax1.clear()
        self.ax1.imshow(self.changedImage,cmap='gray')
        self.ax2.clear()
        self.ax2.hist(new_array.ravel(),bins=256)
        self.canvas.draw()
        self.master.update()
    def saveChanges(self):
        if self.changedImage is None:
            return
        self.originImage=self.changedImage
        
    def update_origin_image(self,newImage) :
        self.originImage=newImage
        self.init_histogram()
    def update_parentwindow(self):
        if self.parentWindow is None:
            return
        self.parentWindow.update_origin_image(self.changedImage)
    def create_linearProcess_window(self):
        if self.originImage is None:
            return
        #self.changedImage=self.imgProcessor.init_img(self.originImage)
        self.changedImage=self.originImage
        child_window=tk.Toplevel(self.master)
        
        child_window.title('线性处理窗口')
        child_window.geometry('1000x800')
        linear_window=LinearWindow(child_window,self.changedImage,self)
        linear_window.init_mainWindow()
        linear_window.init_histogram()
    
    def create_FourierTransform_window(self):
        if self.originImage is None:
            return
        
        child_window=tk.Toplevel(self.master)
        changed_Img=self.originImage.convert('RGB')
        changed_Img=changed_Img.convert('L')
        
        child_window.title('傅里叶变换窗口')
        child_window.geometry('800x800')
        fourier_window=FourierWindow(child_window,changed_Img,self)
        fourier_window.init_mainWindow()
        fourier_window.init_histogram()
    #     self.init_linearProcess_window(linear_window)
        
    # def init_linearProcess_window(self,childWindow):
    #     if childWindow.originImage is None:
    #         print("is null")
    #         return
    #     #创建 matplotlib图形
    #     childWindow.fig=Figure(figsize=(6,4),dpi=100)
        
    #     childWindow.ax1.imshow(childWindow.originImage)
    #     originImage_arr:np.ndarray=self.imgProcessor.getArray(childWindow.originImage)
    #     self.ax2.hist(originImage_arr.ravel(),bins=256)
    #     self.ax2.set_title('Histogram')
        
    #     #将matplotlib放入tinker里面
    #     childWindow.canvas=FigureCanvasTkAgg(childWindow.fig,master=childWindow.master)
        
    #     childWindow.canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)
    #     childWindow.canvas=FigureCanvasTkAgg(childWindow.fig,master=childWindow.master)
    #     childWindow.canvas.draw()
    # def update_histogram(self,val):
    #     if self.originImage is None:
    #         return
    #     self.imgProcessor.getArray(self.originImage)
    #     #待补充


#线性变换调整窗口
class LinearWindow(AppInterface):
    def __init__(self, master, originImage, parentWindow):
        super().__init__(master, originImage, parentWindow)
        self.changedImage=self.originImage
        
    def init_mainWindow(self):
        if self.originImage is None:
            return
        #创建 matplotlib图形
        self.fig=Figure(figsize=(8,4),dpi=100)
        self.ax1=self.fig.add_subplot(2,1,1)
        
        self.ax2=self.fig.add_subplot(2,1,2)
        
        #将matplotlib放入tinker里面
        self.canvas=FigureCanvasTkAgg(self.fig,master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        
        #创建参数输入域
        self.labela=tk.Label(self.master,text="请输入斜率")
        self.labela.pack(side=tk.LEFT,pady=10)
        self.paraA=tk.Entry(self.master,textvariable='a',width=10)
        self.paraA.pack(side=tk.LEFT,pady=10)
        
        self.labelb=tk.Label(self.master,text="请输入截距")
        self.labelb.pack(side=tk.LEFT,pady=10)
        self.paraB=tk.Entry(self.master,textvariable='b',width=10)
        self.paraB.pack(side=tk.LEFT,pady=10)
        #创建应用处理按钮
        self.change_button=tk.Button(self.master,text="应用变换",command=self.applyChange)
        self.change_button.pack(side=tk.LEFT,padx=10,pady=10)
        
        
        
        #创建直方图均衡化按钮
        self.equalized_button=tk.Button(self.master,text="均衡化",command=self.equlizedChange)
        self.equalized_button.pack(side=tk.LEFT,padx=10,pady=10)
        
        #创建重置按钮
        self.reset_button=tk.Button(self.master,text="重置图像",command=self.resetImage)
        self.reset_button.pack(side=tk.RIGHT,padx=10,pady=10)
        
        #创建保存图片按钮
        self.saveImg_button=tk.Button(self.master,text="保存图片",command=lambda: self.saveImg("LinearChange"))
        self.saveImg_button.pack(side=tk.RIGHT,padx=10,pady=10)
        
        #创建转化灰度图按钮
        self.saveImg_button=tk.Button(self.master,text="变为灰度图",command=self.change_To_Gray)
        self.saveImg_button.pack(side=tk.RIGHT,padx=10,pady=10)
        
        #创建一键反相
        self.reverseButton=tk.Button(self.master,text="反相",command=self.reverseFunc)
        self.reverseButton.pack(side=tk.RIGHT,padx=10,pady=10)
        #创建覆盖原图按钮
        self.covertButton=tk.Button(self.master,text="覆盖原图",command=self.update_parentwindow)
        self.covertButton.pack(side=tk.RIGHT,padx=10,pady=10)
        
    def applyChange(self):
        a=float(self.paraA.get())
        b=float(self.paraB.get())
        new_array:np.ndarray=self.imgProcessor.getArray(self.originImage)
        new_array=self.imgProcessor.Get_linearChange_arr(a,b,new_array)
        self.changedImage=Image.fromarray(new_array)
        self.ax1.clear()
        self.ax1.imshow(self.changedImage)
        self.ax2.clear()
        self.ax2.hist(new_array.ravel(),bins=256)
        self.canvas.draw()
        self.master.update()
    def equlizedChange(self):
        # new_array:np.ndarray=self.imgProcessor.getArray(self.originImage)
        # new_array=self.imgProcessor.Get_equlizedChange_arr(new_array)
        new_array=self.imgProcessor.Get_equlizedChange_arr(self.changedImage)
        self.changedImage=Image.fromarray(new_array)
        self.ax1.clear()
        self.ax1.imshow(self.changedImage)
        self.ax2.clear()
        self.ax2.hist(new_array.ravel(),bins=256)
        self.canvas.draw()
        self.master.update()
    def resetImage(self):
        self.ax1.clear()
        self.ax1.imshow(self.originImage)
        self.ax2.clear()
        origin_arr=self.imgProcessor.getArray(self.originImage)
        self.ax2.hist(origin_arr.ravel(),bins=256)
        self.canvas.draw()
        self.master.update()
    def reverseFunc(self):
        a=-1
        b=255
        new_array:np.ndarray=self.imgProcessor.getArray(self.originImage)
        new_array=self.imgProcessor.Get_linearChange_arr(a,b,new_array)
        self.changedImage=Image.fromarray(new_array)
        self.ax1.clear()
        self.ax1.imshow(self.changedImage)
        self.ax2.clear()
        self.ax2.hist(new_array.ravel(),bins=256)
        self.canvas.draw()
        self.master.update()

#傅里叶变换调整窗口
class FourierWindow(AppInterface):
    def __init__(self, master, originImage, parentWindow):
        super().__init__(master, originImage, parentWindow)
        
        self.changedImage=self.originImage
    def init_mainWindow(self):
        if self.originImage is None:
            return
        #创建 matplotlib图形
        self.fig=Figure(figsize=(6,4),dpi=100)
        self.ax1=self.fig.add_subplot(2,1,1)
        
        self.ax2=self.fig.add_subplot(2,1,2)
        
        #将matplotlib放入tinker里面
        self.canvas=FigureCanvasTkAgg(self.fig,master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        
        #创建应用处理按钮
        self.change_button=tk.Button(self.master,text="应用变换",command=self.applyChange)
        self.change_button.pack(side=tk.LEFT,padx=10,pady=10)
        
        
        #创建重置按钮
        self.reset_button=tk.Button(self.master,text="重置图像",command=self.resetImage)
        self.reset_button.pack(side=tk.RIGHT,padx=10,pady=10)
        
    def init_histogram(self):
        if self.originImage is None:
            return
        self.ax1.clear()
        # self.originImage.show()
        self.ax1.imshow(self.originImage,cmap='gray')#需要修改映射空间
        self.ax1.set_title("Changed Image")
        self.ax2.clear()
        #直接声明类型
        magnitude_spectrum=self.imgProcessor.Get_Fourie_arr(self.originImage)
        self.ax2.imshow(magnitude_spectrum,cmap='gray')
        self.ax2.set_title('magnitude spectrum')
        self.canvas.draw()
        
        
    def applyChange(self):
        
        self.ax1.clear()
        self.ax1.imshow(self.changedImage)
        self.ax2.clear()
        #self.ax2.hist(new_array.ravel(),bins=256)
        self.canvas.draw()
        self.master.update()
        
    def resetImage(self):
        self.ax1.clear()
        self.ax1.imshow(self.originImage)
        self.ax2.clear()
        origin_arr=self.imgProcessor.getArray(self.originImage)
        self.ax2.hist(origin_arr.ravel(),bins=256)
        self.canvas.draw()
        self.master.update()
    
        
if __name__=='__main__':
        root=tk.Tk()
        app=AppInterface(root,None,None)
        app.init_mainWindow()
        root.mainloop()