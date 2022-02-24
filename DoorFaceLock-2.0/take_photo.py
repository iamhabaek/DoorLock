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

class Photo_Capture:
    def __init__(self,vid_source):
        self.vid = cv2.VideoCapture(vid_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open this Camera \n select another Camera source",vid_source)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    def getFrame(self):
        if self.vid.isOpened():
            
            self.isTrue, frame = self.vid.read()
            if self.isTrue:
                return (self.isTrue, cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
            else:
                return (self.isTrue, None)
        else:
            return (self.isTrue, None)
       
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
