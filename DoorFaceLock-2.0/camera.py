from tkinter import *
from PIL import ImageTk,Image
from tkinter import messagebox
from tkinter import filedialog
import pickle
import numpy as np
import cv2
import mysql.connector
import bcrypt
import datetime
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import QUrl
import time
from take_photo import Photo_Capture


class Camera:
    def __init__(self,vid_source=0):
        self.vid_source = vid_source
        self.vid = Photo_Capture(self.vid_source)

    def camera_form(self,root):
        self.window = Toplevel(root)
        self.window.resizable(0,0)
        self.window.title("C A M E R A")
        self.window["bg"] = "black"

        self.label = Label(self.window,text='Camera',font=15,bg='blue',fg='white').pack(side=TOP,fill=BOTH)

        self.canvas = Canvas(self.window,width=self.vid.width,height=self.vid.height,bg='red')
        self.canvas.pack()
        self.update()
        self.btn = Button(self.window,text='Capture',width=30,bg='goldenrod2',activebackground='red',command=self.capture)
        self.btn.pack(expand=True)



    def capture(self):
        check, frame = self.vid.getFrame()
        if check:
            image = "IMG-" + time.strftime("%H-%M-%S-%d-%m") + ".jpg"
            cv2.imwrite(image,cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
            msg = Label(self.window, text="Image Saved"+image,bg='black',fg='green').place(x=430,y=510)
    def update(self):
        isTrue, frame = self.vid.getFrame()
        if isTrue:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0,0,image=self.photo,anchor = NW)
        self.window.after(15,self.update)
    def exit_camera(self):
        self.vid.__del__()
        self.window.destroy()
       
        