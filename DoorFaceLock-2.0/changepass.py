from cgitb import text
from doctest import master
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
import io


class ChangePassword:
    def __init__(self) :
        self.bg = '#363433'
        self.fg_title = '#c95e06'
        self.fg = 'white'
        self.font =('Roboto',12,)
        self.title_font = ('Roboto',15,'bold')

    def save(self):
        try:
            conn = mysql.connector.connect(
                                    host ="localhost",
                                    user = "root",
                                    password = "B)omerang1",
                                    database = "doorsecurity"
                                    )
            cursor = conn.cursor()   
            cursor.execute("select * from admin where username=%s",(self.username_box.get(),))
            result =cursor.fetchone()
            print(result[6])           
            row7 = result[7]
            newrow = row7.encode('utf-8')    
            currentpass = self.current_pass_box.get().encode('utf-8')
            newpass = self.new_pass_box.get().encode('utf-8')
            hashpass = bcrypt.hashpw(currentpass,bcrypt.gensalt())
            print(hashpass)
            hashnewpass = bcrypt.hashpw(newpass,bcrypt.gensalt())
            
            if self.new_pass_box.get() != self.confirm_box.get():
                messagebox.showerror("Error", "Password doesn't match",parent=self.root)
                self.new_pass_box.delete(0,END)
                self.confirm_box.delete(0,END)
            elif bcrypt.checkpw(currentpass,newrow):
                conn = mysql.connector.connect(
                            host ="localhost",
                            user = "root",
                            password = "B)omerang1",
                            database = "doorsecurity"
                                )
                cursor = conn.cursor()
                cursor.execute('update admin set password = %s where username  = %s',(hashnewpass,result[6]))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Password has been changed",parent=self.root)
                self.root.destroy()
            
        except Exception as es:
            messagebox.showerror('Error',f'Error due to  : {str(es)}',parent = self.root)  

    def changepass_form(self,root):
        self.root = Toplevel(root)
        self.root.geometry('400x400')
        self.root.title("CHANGE PASSWORD")
        self.root.resizable(0,0)
        self.root.configure(bg=self.bg)
        self.admin_frame = Frame(self.root,bg=self.bg)
        self.admin_frame.pack()

        self.title_frame = Frame(self.admin_frame,bg=self.bg)
        self.title_frame.pack(fill=BOTH,expand=1)
        self.title_lbl = Label(self.title_frame,text='CHANGE PASSWORD',font=self.title_font,fg=self.fg_title,bg=self.bg)
        self.title_lbl.pack(pady=20)

        self.form_frame = Frame(self.admin_frame,bg=self.bg)
        self.form_frame.pack(fill=BOTH,expand=1)

        self.username = Label(self.form_frame,text='Username: ',font=self.font,fg=self.fg,bg=self.bg)
        self.username.grid(row=0,column=0,sticky=W,pady=(20,10))
        self.username_box = Entry(self.form_frame,fg=self.fg,bg=self.bg,font=self.font)
        self.username_box.grid(row=0,column=1,sticky=W,pady=10)

        self.current_pass = Label(self.form_frame,text='Current Password: ',font=self.font,fg=self.fg,bg=self.bg)
        self.current_pass.grid(row=1,column=0,sticky=W,pady=10)
        self.current_pass_box = Entry(self.form_frame,fg=self.fg,bg=self.bg,font=self.font,show='*')
        self.current_pass_box.grid(row=1,column=1,sticky=W,pady=10)

        self.new_pass = Label(self.form_frame,text='New Password: ',font=self.font,fg=self.fg,bg=self.bg)
        self.new_pass.grid(row=2,column=0,sticky=W,pady=10)
        self.new_pass_box = Entry(self.form_frame,fg=self.fg,bg=self.bg,font=self.font,show='*')
        self.new_pass_box.grid(row=2,column=1,sticky=W,pady=10)

        self.confirm = Label(self.form_frame,text='New Password: ',font=self.font,fg=self.fg,bg=self.bg)
        self.confirm.grid(row=3,column=0,sticky=W,pady=10)
        self.confirm_box = Entry(self.form_frame,fg=self.fg,bg=self.bg,font=self.font,show='*')
        self.confirm_box.grid(row=3,column=1,sticky=W,pady=10)


        def new_admin_btn(text,ecolor,lcolor):
            
            def on_entera(e):
                self.new_admin_btn['background'] = '#963403' #ffcc66
                self.new_admin_btn['foreground']= 'white'  #000d33

            def on_leavea(e):
                self.new_admin_btn['background'] = lcolor
                self.new_admin_btn['foreground']= ecolor

            self.new_admin_btn = Button(self.admin_frame,text=text,
                        width=12,
                        height=2,
                        fg=ecolor,
                        border=0,
                        bg=lcolor,
                        activeforeground='white',
                        activebackground='#963403',
                        font=('Roboto',8,'bold'),command=self.save
                        )             
            self.new_admin_btn.bind("<Enter>", on_entera)
            self.new_admin_btn.bind("<Leave>", on_leavea)
            self.new_admin_btn.pack(pady=20)

        new_admin_btn('C H A N G E','white', '#c95e06')