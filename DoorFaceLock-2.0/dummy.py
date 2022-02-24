from cgitb import text
from email import message
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



class Admin:
    def __init__(self) :
        self.bg = '#363433'
        self.fg_title = '#c95e06'
        self.fg = 'white'
        self.font =('Roboto',12,)
        self.title_font = ('Roboto',15,'bold')

    def add_admin(self):
            self.password = self.password_box.get().encode('utf-8')
            self.confirmpass = self.confirm_box.get().encode('utf-8')
            self.hashed_pass = bcrypt.hashpw(self.password, bcrypt.gensalt())
            self.hashed_confirmpass = bcrypt.hashpw(self.confirmpass, bcrypt.gensalt())
            age = self.age_box.get() 

            if self.id_box.get() =="" or self.fn_box.get() == "" or self.ln_box.get() =="" or self.address_box.get() =="" or self.age_box.get() ==""  or self.pos_box.get() == "" or self.username_box.get() == ""  or  self.password_box.get() =="" or self.confirm_box.get() =="":
                messagebox.showwarning("Fill All", "All fields are Empty",parent=self.root)
           
            elif self.password_box.get() != self.confirm_box.get():
                    messagebox.showwarning("Match It", "Password doesn't match",parent = self.root)
                    self.password_box.delete(0,END)
                    self.confirm_box.delete(0,END)
                 
            else:
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
                    if result != None:
                        messagebox.showerror('Error', "Username already exist try another username",parent=self.root)
                        self.username_box.delete(0,END)
                    else:
                        sql_command = "INSERT INTO admin (admin_id,firstname,lastname,address,age,admin_position,username,password,date_added) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        date_now = datetime.datetime.now()
                        x = (self.id_box.get(),self.fn_box.get(),self.ln_box.get(),self.address_box.get(),self.age_box.get(),self.pos_box.get(),self.username_box.get(),self.hashed_pass,date_now)
                        cursor.execute(sql_command,x)
                        conn.commit()
                        conn.close()
                        messagebox.showinfo("Success", "Register Succesful",parent = self.root)
                        self.root.destroy()
                    int(self.age_box)

                except Exception as es:
                        messagebox.showerror('Error',f'Error due to  : {str(es)}',parent = self.root)  
                                        
    def new_admin_form(self,root):
        self.root = Toplevel(root)
        self.root.geometry('400x600')
        self.root.title("R E G I S T R A T I O N")
        self.root.resizable(0,0)
        self.root.configure(bg=self.bg)
        self.admin_frame = Frame(self.root,bg=self.bg)
        self.admin_frame.pack()

        self.title_frame = Frame(self.admin_frame,bg=self.bg)
        self.title_frame.pack(fill=BOTH,expand=1)
        self.title_lbl = Label(self.title_frame,text='REGISTER',font=self.title_font,fg=self.fg_title,bg=self.bg)
        self.title_lbl.pack(pady=20)

        self.form_frame = Frame(self.admin_frame,bg=self.bg)
        self.form_frame.pack(fill=BOTH,expand=1)

        self.id_lbl = Label(self.form_frame,text='ID: ',font=self.font,fg=self.fg,bg=self.bg)
        self.id_lbl.grid(row=0,column=0,sticky=W,pady=(20,10))
        self.id_box = Entry(self.form_frame,fg=self.fg,bg=self.bg,font=self.font)
        self.id_box.grid(row=0,column=1,sticky=W,pady=10)

        self.fn_lbl = Label(self.form_frame,text='Firstname: ',font=self.font,fg=self.fg,bg=self.bg)
        self.fn_lbl.grid(row=1,column=0,sticky=W,pady=10)
        self.fn_box = Entry(self.form_frame,fg=self.fg,bg=self.bg,font=self.font)
        self.fn_box.grid(row=1,column=1,sticky=W,pady=10)

        self.ln_lbl = Label(self.form_frame,text='Lastname: ',font=self.font,fg=self.fg,bg=self.bg)
        self.ln_lbl.grid(row=2,column=0,sticky=W,pady=10)
        self.ln_box = Entry(self.form_frame,fg=self.fg,bg=self.bg,font=self.font)
        self.ln_box.grid(row=2,column=1,sticky=W,pady=10)

        self.address_lbl = Label(self.form_frame,text='Address: ',font=self.font,fg=self.fg,bg=self.bg)
        self.address_lbl.grid(row=3,column=0,sticky=W,pady=10)
        self.address_box = Entry(self.form_frame,fg=self.fg,bg=self.bg,font=self.font)
        self.address_box.grid(row=3,column=1,sticky=W,pady=10)

        self.age_lbl = Label(self.form_frame,text='Age: ',font=self.font,fg=self.fg,bg=self.bg)
        self.age_lbl.grid(row=4,column=0,sticky=W,pady=10)
        self.age_box = Entry(self.form_frame,fg=self.fg,bg=self.bg,font=self.font)
        self.age_box.grid(row=4,column=1,sticky=W,pady=10)

        self.pos_lbl = Label(self.form_frame,text='Position: ',font=self.font,fg=self.fg,bg=self.bg)
        self.pos_lbl.grid(row=5,column=0,sticky=W,pady=10)
        self.pos_box = Entry(self.form_frame,fg=self.fg,bg=self.bg,font=self.font)
        self.pos_box.grid(row=5,column=1,sticky=W,pady=10)

        self.username_lbl = Label(self.form_frame,text='Username: ',font=self.font,fg=self.fg,bg=self.bg)
        self.username_lbl.grid(row=6,column=0,sticky=W,pady=10)
        self.username_box = Entry(self.form_frame,fg=self.fg,bg=self.bg,font=self.font)
        self.username_box.grid(row=6,column=1,sticky=W,pady=10)

        self.password_lbl = Label(self.form_frame,text='Password: ',font=self.font,fg=self.fg,bg=self.bg)
        self.password_lbl.grid(row=7,column=0,sticky=W,pady=10)
        self.password_box = Entry(self.form_frame,fg=self.fg,bg=self.bg,font=self.font,show='*')
        self.password_box.grid(row=7,column=1,sticky=W,pady=10)

        self.confirm_lbl = Label(self.form_frame,text='Confirm Password: ',font=self.font,fg=self.fg,bg=self.bg)
        self.confirm_lbl.grid(row=8,column=0,sticky=W,pady=10)
        self.confirm_box = Entry(self.form_frame,fg=self.fg,bg=self.bg,font=self.font,show='*')
        self.confirm_box.grid(row=8,column=1,sticky=W,pady=10)

        def new_admin_btn(text,ecolor,lcolor):
            self.admin = Admin()
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
                        font=('Roboto',8,'bold'),command=self.add_admin
                        )             
            self.new_admin_btn.bind("<Enter>", on_entera)
            self.new_admin_btn.bind("<Leave>", on_leavea)
            self.new_admin_btn.pack(pady=20)

        new_admin_btn('S U B M I T','white', '#c95e06')
