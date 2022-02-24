from cgitb import text
from email.mime import image
from textwrap import fill
from tkinter import *
from tkinter import ttk
from tkinter import font
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
from dashboard import Dashboard


class Login:
    def __init__(self,root):
        self.root = root
        self.root.geometry("400x300+400+100")
        self.root.title("L O G I N")
        self.root.resizable(0,0)
        self.bg = '#363433'
        self.fg_title = '#c95e06'
        self.fg = 'white'
        self.root.configure(bg=self.bg)
        

    def login_form(self):
        # Create Login Form Frame
        self.title_frame =Frame(self.root,width=400,height=100,bg=self.bg)
        self.title_frame.pack()
        #Title
        self.title_label = Label(self.title_frame,text="DOOR SECURITY LOGIN",font=('Roboto',20,'bold'),bg=self.bg,fg=self.fg_title )
        self.title_label.pack(pady=20)
        self.form_frame =Frame(self.root,width=400,height=300,bg=self.bg)
        self.form_frame.pack()
        self.username_lbl = Label(self.form_frame,text="Username:",font=('Roboto',12),bg=self.bg,fg=self.fg ,anchor=W)
        self.username_lbl.grid(row=0,column=0,padx=20,pady=20)
        self.username_box = Entry(self.form_frame,bg =self.bg,highlightthickness=1,highlightbackground='white',font=('Roboto',12),fg=self.fg )
        self.username_box.grid(row=0,column=1,pady=20,ipadx=3)
        self.password_lbl = Label(self.form_frame,text="Password:",font=('Roboto',12),bg=self.bg,fg=self.fg,anchor=W)
        self.password_lbl.grid(row=1,column=0,padx=20,pady=10)
        self.password_box = Entry(self.form_frame,bg=self.bg,highlightthickness=1,highlightbackground='white',font=('Roboto',12),fg=self.fg,show='*')
        self.password_box.grid(row=1,column=1,pady=10,ipadx=3)
        self.btn_frame =Frame(self.root,width=400,height=100,bg=self.bg)
        self.btn_frame.pack()
        def bttn(text,ecolor,lcolor):
            def on_entera(e):
                self.save_btn['background'] = '#963403' #ffcc66
                self.save_btn['foreground']= 'white'  #000d33

            def on_leavea(e):
                self.save_btn['background'] = lcolor
                self.save_btn['foreground']= ecolor
            
            self.save_btn = Button(self.btn_frame,text=text,
                        width=15,
                        height=2,
                        fg=ecolor,
                        border=0,
                        bg=lcolor,
                        activeforeground= 'white',
                        activebackground='#963403',command=self.login
                        )             
            self.save_btn.bind("<Enter>", on_entera)
            self.save_btn.bind("<Leave>", on_leavea)
            self.save_btn.grid(row=0,column=0,pady=20,padx=(20,0))
 
        bttn("L O G I N",'white',self.fg_title) 

    def login(self):

        global current
        current = ""
        
        if self.username_box.get() == "" and self.password_box.get() =="":
            messagebox.showerror("Error", "Fields are Empty", parent=self.root)
        elif self.username_box.get() == "" :
            messagebox.showerror("Error", "Username is empty", parent=self.root)
        elif  self.password_box.get() =="":
            messagebox.showerror("Error", "Password is Empty", parent=self.root)
        
        else:
            try:
                
                conn = mysql.connector.connect(
                        host ="localhost",
                        user = "root",
                        password = "B)omerang1",
                        database = "doorsecurity"
                            )
                cursor = conn.cursor()
                cursor.execute('''
                SELECT * FROM admin where 
                username=%s
                ''',(self.username_box.get(),))
                admin = cursor.fetchone()
    
                if admin == None:
                    messagebox.showerror('Error', "Username is incorrect",parent=self.root)
                    self.username_box.delete(0,END)

                elif bcrypt.checkpw(self.password_box.get().encode('utf-8'), str(admin[7]).encode()):
                    current  = admin[0]
                    self.dashboard = Dashboard(self.root)
                    self.dashboard.current(current)
                    self.dashboard.dashboard()
                    self.root.withdraw()
                else:
                   messagebox.showerror('Error',"Password is incorrect",parent=self.root)
                   self.password_box.delete(0,END)
                    
            except Exception as es:
                messagebox.showerror('Error',f'Error due to  : {str(es)}',parent = self.root)
