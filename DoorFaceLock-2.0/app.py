from tkinter import *
from tkinter import ttk
from tkinter.font import ROMAN
from PIL import ImageTk,Image
from tkinter import messagebox
from tkinter import filedialog
import pickle
import numpy as np
import cv2
import mysql.connector
import bcrypt
import datetime
from login import Login


class DoorLock:

    def __init__(self,root):
        self.root = root
        self.login = Login(self.root)
        self.login.login_form()





if __name__ == "__main__":
    root = Tk()
    door = DoorLock(root)
    root.mainloop()
