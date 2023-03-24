
import tkinter as tk
from PIL import Image,ImageTk,ImageEnhance
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from ImageProcessor import ImgProcessor
class AppInterface:
    def __init__(self,master,originImage,parentWindow):
        self.imgProcessor=ImgProcessor()
        self.master=master
        self.master.geometry('800x600')
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
        #创建滑块
        self.silder_label=tk.Label(self.master,text="Contrast: ")
        self.silder_label.pack(side=tk.LEFT,padx=10,pady=10)
        self.silder=tk.Scale(self.master,from_=0.0,to=2.0,resolution=0.01,orient=tk.HORIZONTAL,command=self.update_histogram)
        self.silder.set(1.0)
        self.silder.pack(side=tk.LEFT,padx=10,pady=10)
        
    def load_image(self):
        file_path=filedialog.askopenfilename()
        if file_path:
            
            self.originImage=Image.open(file_path)
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
            

            
    def create_linearProcess_window(self):
        if self.originImage is None:
            return
        self.changedImage=self.imgProcessor.init_img(self.originImage)
        child_window=tk.Toplevel(self.master)
        
        child_window.title('线性处理窗口')
        child_window.geometry('800x800')
        linear_window=AppInterface(child_window,self.changedImage,self)
        linear_window.init_mainWindow()
        self.init_linearProcess_window(linear_window)
        
    def init_linearProcess_window(self,childWindow):
        if childWindow.originImage is None:
            print("is null")
            return
        #创建 matplotlib图形
        childWindow.fig=Figure(figsize=(6,4),dpi=100)
        
        childWindow.ax1.imshow(childWindow.originImage)
        originImage_arr:np.ndarray=self.imgProcessor.getArray(childWindow.originImage)
        self.ax2.hist(originImage_arr.ravel(),bins=256)
        self.ax2.set_title('Histogram')
        
        #将matplotlib放入tinker里面
        childWindow.canvas=FigureCanvasTkAgg(childWindow.fig,master=childWindow.master)
        
        childWindow.canvas.get_tk_widget().pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        childWindow.canvas=FigureCanvasTkAgg(childWindow.fig,master=childWindow.master)
        childWindow.canvas.draw()
    def update_histogram(self,val):
        if self.originImage is None:
            return
        self.imgProcessor.getArray(self.originImage)
        #待补充
                
if __name__=='__main__':
        root=tk.Tk()
        app=AppInterface(root,None,None)
        app.init_mainWindow()
        root.mainloop()