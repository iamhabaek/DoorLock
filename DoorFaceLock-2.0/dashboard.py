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
from admin import Admin
from camera import Camera
from recognizer import Recognizer
from changepass import ChangePassword


class Dashboard:
    def __init__(self,root):
        self.root = Toplevel(root)
        self.root.geometry("900x1000")
        self.root.title("D A S H B O A R D")
        #self.root.resizable(0,0)
        self.bg = '#363433'
        self.fg_title = '#c95e06'
        self.fg = 'white'
        self.changepass = ChangePassword()
        self.root.configure(bg=self.bg)
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.file_menu = Menu(self.menu)
        self.menu.add_cascade(label="File",menu=self.file_menu)
        self.edit_menu = Menu(self.menu)
        self.menu.add_cascade(label="Edit",menu=self.edit_menu)
        self.edit_menu.add_command(label="Change Password",command=lambda:self.changepass.changepass_form(self.root))
        

    
    
    
    def current(self,admin):
            global current
            current = admin

    def add_room_user(self):#,fn,ln,pos,filepath
        #print(filepath)
        
        if self.fn_box.get() == "" or self.ln_box.get() ==""  or self.pos_box.get() == "":
            messagebox.showwarning("Fill All", "All fields are Empty",parent=self.root)
           
        elif self.profile_photo.cget("text") != "":
                messagebox.showwarning("No Image", "Please Add Image",parent = self.root)
        else:
            try:
                
         
                conn = mysql.connector.connect(
                        host ="localhost",
                        user = "root",
                        password = "B)omerang1",
                        database = "doorsecurity"
                            )
                cursor = conn.cursor()
                cursor.execute('select * from room_users where firstname = %s AND lastname= %s',(self.fn_box.get(),self.ln_box.get()))
                result = cursor.fetchone()
                if result != None:
                    messagebox.showerror('Error', "Room user already exist try another name",parent=self.root)
                    self.fn_box.delete(0,END)
                    self.ln_box.delete(0,END)
                else:
                    
                    sql_add = '''insert into room_users (firstname,lastname,position,photo,admin_id,date_added) values(%s,%s,%s,%s,%s,%s)'''
                    date_added = datetime.date.today()
                    inputs = (self.fn_box.get().capitalize(),self.ln_box.get().capitalize(),self.pos_box.get().capitalize(),binaryData,current,date_added)
                    #inputs = (fn,ln,pos,binaryData,current,date_added)
                    cursor.execute(sql_add,inputs)
                    conn.commit()
                    self.clear_boxes()
                    self.treeview.delete(*self.treeview.get_children())
                    global count 
                    count = 0
                    cursor.execute("SELECT * FROM room_users")
                    records = cursor.fetchall()
                    self.treeview.imglist= []
                    for record in records:
                        self.img = Image.open(io.BytesIO(record[4]))
                        self.img.thumbnail((50,50)) # resize the image to desired size
                        self.img = ImageTk.PhotoImage(self.img)
                        if count % 2 ==0:
                            self.treeview.insert(parent='',index='end', iid=count,text='',image =self.img,values=(record[0],record[1],record[2],record[3],record[5],record[6]),tags=('evenrow',))
                            self.treeview.imglist.append(self.img)
                        else:
                            self.treeview.insert(parent='',index='end', iid=count,text='',image = self.img,values=(record[0],record[1],record[2],record[3],record[5],record[6]),tags=('oddrow',))
                            self.treeview.imglist.append(self.img)
                        count+=1
                    openfile =""
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Room User Added",parent=self.root)
            except Exception as es:
                    messagebox.showerror('Error',f'Error due to  : {str(es)}',parent = self.root)  
    def clear_boxes(self):
        self.fn_box.delete(0,END)
        self.ln_box.delete(0,END)
        self.pos_box.delete(0,END)
        self.add_user_btn.config(state=ACTIVE)
        self.profile_photo.config(image="")
        self.profile_photo.config(text='Profile Picture')
        selected = 0

    def selected(self,e):
        self.clear_boxes()   
        self.selected = self.treeview.focus()
        values = self.treeview.item(self.selected,'values')
        conn = mysql.connector.connect(
                        host ="localhost",
                        user = "root",
                        password = "B)omerang1",
                        database = "doorsecurity"
                            )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM room_users where id=%s",(values[0],))
        self.records = cursor.fetchone()
        img =Image.open(io.BytesIO(self.records[4]))
        img.thumbnail((50,50)) # resize the image to desired size
        pic = ImageTk.PhotoImage(img)
        self.profile_photo.config(image=pic)
        self.profile_photo.config(text="")
        self.add_img_btn.config(text="Change Image")
        self.fn_box.insert(0,values[1])
        self.ln_box.insert(0,values[2])
        self.pos_box.insert(0,values[3])
        self.add_user_btn.config(state=DISABLED)
    def delete_one(self):
        
        response = messagebox.askyesno("Delete","Are you sure you want to delete this?")
            
        if response == 1:  
            x =self.treeview.selection()[0]
            values = self.treeview.item(self.selected,'values')
            self.treeview.delete(x)
            conn = mysql.connector.connect(
                        host ="localhost",
                        user = "root",
                        password = "B)omerang1",
                        database = "doorsecurity"
                            )
            cursor = conn.cursor()
            sql_delete = '''delete from room_users where id = %s'''
                
            cursor.execute(sql_delete,(values[0],))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "User Deleted")
                
            self.clear_boxes()
            self.add_user_btn.config(state=ACTIVE)
       

    def delete_all(self):
            response = messagebox.askyesno("Delete","Are you sure you want to delete all selected?")

            if response == 1:
                x =self.treeview.selection()

                ids_to_delete = []
                    
                for record in x:
                    ids_to_delete.append(self.treeview.item(record,'values')[0]) 
                        
                for record in x:
                    self.treeview.delete(record)
                conn = mysql.connector.connect(
                    host ="localhost",
                    user = "root",
                    password = "B)omerang1",
                    database = "doorsecurity"
                            )
                cursor = conn.cursor()
                sql_delete = 'delete  from room_users where id=%s '
                values = [(a,) for a in ids_to_delete]
                cursor.executemany(sql_delete,values)
                conn.commit()
                conn.close()
                self.clear_boxes()
                self.add_user_btn.config(state=ACTIVE)      
    def update_room_user(self):
        if self.fn_box.get() == "" or self.ln_box.get() ==""  or self.pos_box.get() == "":
            messagebox.showwarning("Fill All", "All fields are Empty",parent=self.root)
           
        elif self.profile_photo.cget("text") != "":
                messagebox.showwarning("No Image", "Please Add Image",parent = self.root)
        else:
            try:
                    selected = self.treeview.focus()
                    values = self.treeview.item(self.selected,'values')
                    self.treeview.item(selected,text='',values=(values[0],self.fn_box.get(),self.ln_box.get(),self.pos_box.get(),values[4],values[5]))
                    conn = mysql.connector.connect(
                                host ="localhost",
                                user = "root",
                                password = "B)omerang1",
                                database = "doorsecurity"
                                    )
                    cursor = conn.cursor()
                    sql_update = '''update room_users set firstname=%s ,lastname=%s, position=%s, photo=%s where id=%s '''
                    firstname = self.fn_box.get()
                    lastname = self.ln_box.get()
                    position = self.pos_box.get()
                    if self.profile_photo.cget("text") == "":
                        binaryData = self.records[4]
                    
                    inputs =(firstname,lastname,position,binaryData,values[0])
                    cursor.execute(sql_update,inputs)
                    conn.commit()
                    self.clear_boxes()
                    messagebox.showinfo("Success", "Update Successful", parent= self.root)
            except Exception as es:
                messagebox.showerror('Error',f'Error due to  : {str(es)}',parent = self.root)       
    def clear_treeview(self):
        for record in self.treeview.get_children():
            self.treeview.delete(record)
    def reset_tree(self):
        self.clear_treeview()
        self.search_box.delete(0,END)
        #Add data to screen
        global count 
        count = 0
        #cursor.execute("SELECT * FROM users")
        conn = mysql.connector.connect(
                                host ="localhost",
                                user = "root",
                                password = "B)omerang1",
                                database = "doorsecurity"
                                )
        cursor = conn.cursor()   
        cursor.execute(''' select room_users.id,room_users.firstname,
        room_users.lastname,room_users.position,room_users.photo,admin.lastname,room_users.date_added
        from room_users join admin on room_users.admin_id = admin.admin_id;
        ''')
        records = cursor.fetchall()
        #result = cursor.fetchall()
        #print(result)
        #print(records)
        self.treeview.imglist= []
        for record in records:
            self.img = Image.open(io.BytesIO(record[4]))
            self.img.thumbnail((25,25)) # resize the image to desired size
            self.img = ImageTk.PhotoImage(self.img,master = self.manage_frame)
            if count % 2 ==0:
                self.treeview.insert(parent='',index='end', iid=count,text='',image =self.img,values=(record[0],record[1],record[2],record[3],record[5],record[6]),tags=('evenrow',))
                self.treeview.imglist.append(self.img)
            else:
                self.treeview.insert(parent='',index='end', iid=count,text='',image = self.img,values=(record[0],record[1],record[2],record[3],record[5],record[6]),tags=('oddrow',))
                self.treeview.imglist.append(self.img)
            count+=1

    def search_user(self):
        search = self.search_var.get()
        conn = mysql.connector.connect(
                    host ="localhost",
                    user = "root",
                    password = "B)omerang1",
                    database = "doorsecurity"
                        )
        cursor = conn.cursor()
        #query = "SELECT id,firstname,lastname,position FROM room_users where firstname LIKE '%"+search+"%' OR lastname LIKE '%"+search+"%' "
        query = "select room_users.id,room_users.firstname,room_users.lastname,room_users.position,room_users.photo,admin.lastname,room_users.date_added from room_users join admin on room_users.admin_id = admin.admin_id where room_users.firstname LIKE '%"+search+"%' OR room_users.lastname LIKE '%"+search+"%'"
        cursor.execute(query)
        rows = cursor.fetchall()    
        conn.commit()
        self.clear_treeview()
        #Add data to screen
        global count 
        count = 0

        #result = cursor.fetchall()
        #print(result)
        #print(records)
        self.treeview.imglist= []
        for record in rows:
            self.img = Image.open(io.BytesIO(record[4]))
            self.img.thumbnail((25,25)) # resize the image to desired size
            self.img = ImageTk.PhotoImage(self.img,master = self.manage_frame)
            if count % 2 ==0:
                self.treeview.insert(parent='',index='end', iid=count,text='',image =self.img,values=(record[0],record[1],record[2],record[3],record[5],record[6]),tags=('evenrow',))
                self.treeview.imglist.append(self.img)
            else:
                self.treeview.insert(parent='',index='end', iid=count,text='',image = self.img,values=(record[0],record[1],record[2],record[3],record[5],record[6]),tags=('oddrow',))
                self.treeview.imglist.append(self.img)
            count+=1

    def dashboard(self):
        self.root.config(menu=self.menu)
        self.dashboard_frame = Frame(self.root,width=1360,height=1000,bg=self.bg)
        self.dashboard_frame.pack(fill=BOTH,expand=1)

        
        self.title_frame = Frame(self.dashboard_frame,bg=self.bg)
        self.title_frame.pack(fill=BOTH,expand =1,padx=(40,0))
        
        title_lbl = Label(self.title_frame,text='Door Security Management',font=('Roboto',25,'bold'),bg=self.bg,fg=self.fg_title)
        title_lbl.grid(row=1,column=1,columnspan=2,padx=(100,100),pady=(20,0))
        self.recognizer_frame = Frame(self.title_frame,width=200,height=50,bg=self.bg)
        self.recognizer_frame.grid(row=2,column=0)
        def recognize_user_btn(text,ecolor,lcolor):
            self.recognizer = Recognizer()
            def on_entera(e):
                self.recognize_user_btn['background'] = '#a6201c' #ffcc66
                self.recognize_user_btn['foreground']= 'white'  #000d33

            def on_leavea(e):
                self.recognize_user_btn['background'] = lcolor
                self.recognize_user_btn['foreground']= ecolor

            self.recognize_user_btn = Button(self.recognizer_frame,text=text,
                        width=12,
                        height=2,
                        fg=ecolor,
                        border=0,
                        bg=lcolor,
                        activeforeground='white',
                        activebackground= '#a6201c',
                        font=('Roboto',8,'bold'),command=self.recognizer.recognizer
                        )             
            self.recognize_user_btn.bind("<Enter>", on_entera)
            self.recognize_user_btn.bind("<Leave>", on_leavea)
            self.recognize_user_btn.grid(row=0,column=0)

        recognize_user_btn('Recognizer','white','#d9534f')
        
        def logout():
                self.current = ''
                print(self.current)
                self.root.quit()
            
        def logout_btn(text,ecolor,lcolor):
            def on_entera(e):
                self.logout_btn['background'] = '#a6201c' #ffcc66
                self.logout_btn['foreground']= 'white'  #000d33

            def on_leavea(e):
                self.logout_btn['background'] = lcolor
                self.logout_btn['foreground']= ecolor

            self.logout_btn = Button(self.title_frame,text=text,
                        width=12,
                        height=2,
                        fg=ecolor,
                        border=0,
                        bg=lcolor,
                        activeforeground='white',
                        activebackground= '#a6201c',
                        font=('Roboto',8,'bold'),command=logout
                        )             
            self.logout_btn.bind("<Enter>", on_entera)
            self.logout_btn.bind("<Leave>", on_leavea)
            self.logout_btn.grid(row=0,column=3,pady=(20,0),padx=(0,50),sticky=E)
            
            
        logout_btn('L O G O U T','white','#d9534f')
        def manage_admin_btn(text,ecolor,lcolor):
            self.admin = Admin()
            def on_entera(e):
                self.manage_admin_btn['background'] = '#963403' #ffcc66
                self.manage_admin_btn['foreground']= 'white'  #000d33

            def on_leavea(e):
                self.manage_admin_btn['background'] = lcolor
                self.manage_admin_btn['foreground']= ecolor

            self.manage_admin_btn = Button(self.title_frame,text=text,
                        width=12,
                        height=2,
                        fg=ecolor,
                        border=0,
                        bg=lcolor,
                        activeforeground='white',
                        activebackground='#963403',
                        font=('Roboto',8,'bold'),command=lambda:self.admin.admin_management_form(self.root)
                        )             
            self.manage_admin_btn.bind("<Enter>", on_entera)
            self.manage_admin_btn.bind("<Leave>", on_leavea)
            self.manage_admin_btn.grid(row=0,column=2,pady=(20,0),sticky=E,padx=(0,20))
            
            
        manage_admin_btn('Manage Admin','white', self.fg_title)
        
        self.manage_frame = Frame(self.dashboard_frame,bg=self.bg)
        self.manage_frame.pack(fill=BOTH,expand=1)
        self.new_user_frame = LabelFrame(self.manage_frame,bg=self.bg,text='Add Room User',bd=3,fg=self.fg_title,font=('Roboto',12,'bold'))
        self.new_user_frame.grid(row=0,column=0,sticky=W,padx=(20,0))
        l = ('Roboto',10)
        bg = self.bg
        fg = self.fg
        fg_box = 'white'
        
        self.fn_lbl = Label(self.new_user_frame,text='First Name',fg=fg,bg=bg,font=l)
        self.fn_lbl.grid(row=0,column=0,sticky=W,padx=10)
        self.fn_box = Entry(self.new_user_frame,bg=bg,fg = fg_box,highlightthickness=1,highlightbackground=self.fg,font=l)
        self.fn_box.grid(row=1,column=0,padx=10,sticky=W)
        self.ln_lbl = Label(self.new_user_frame,text='Last Name',fg=fg,bg=bg,font=l)
        self.ln_lbl.grid(row=0,column=1,padx=10,sticky=W)
        self.ln_box = Entry(self.new_user_frame,bg=bg,fg = fg_box,highlightthickness=1,highlightbackground='white',font=l)
        self.ln_box.grid(row=1,column=1,padx=10,sticky=W)
        self.pos_lbl = Label(self.new_user_frame,text='Position',fg=fg,bg=bg,font=l)
        self.pos_lbl.grid(row=0,column=2,padx=10,sticky=W)
        self.pos_box = Entry(self.new_user_frame,bg=bg,fg = fg_box,highlightthickness=1,highlightbackground='white',font=l)
        self.pos_box.grid(row=1,column=2,padx=10,sticky=W)
        def camera_btn(text,ecolor,lcolor):
            self.camera = Camera()
            def on_entera(e):
                self.take_photo['background'] = '#308aa6' #ffcc66
                self.take_photo['foreground']= ecolor  #000d33

            def on_leavea(e):
                self.take_photo['background'] = lcolor
                self.take_photo['foreground']= ecolor

            self.take_photo = Button(self.new_user_frame,text=text,
                        width=8,
                        height=2,
                        fg=ecolor,
                        border=0,
                        bg=lcolor,
                        activeforeground=ecolor,
                        activebackground='#308aa6',
                        font=('Roboto',8,'bold'),command=lambda:self.camera.camera_form(self.root)
                        )             
            self.take_photo.bind("<Enter>", on_entera)
            self.take_photo.bind("<Leave>", on_leavea)
            self.take_photo.grid(row=2,column=0,pady=10,padx=10,sticky=W)
            
            
        camera_btn('Camera','white','#5bc0de')
        def add_img():
            global openfile
            openfile= filedialog.askopenfilename(initialdir="/images",title='Select Images',filetypes=(("jpg files","*.jpg"),("png files","*.png")))
            img = Image.open(openfile)
            img.thumbnail((25,25))
            profile_pic = ImageTk.PhotoImage(img)
            self.profile_photo.config(image=profile_pic)  
            self.profile_photo.image_names
            self.profile_photo.config(text='')

            with open(openfile,"rb") as File:
                    global binaryData
                    binaryData = File.read()
        def add_img_btn(text,ecolor,lcolor):
            def on_entera(e):
                self.add_img_btn['background'] ='#963403' #ffcc66
                self.add_img_btn['foreground']= ecolor  #000d33

            def on_leavea(e):
                self.add_img_btn['background'] = lcolor
                self.add_img_btn['foreground']= ecolor

            self.add_img_btn = Button(self.new_user_frame,text=text,
                        width=12,
                        height=2,
                        fg=ecolor,
                        border=0,
                        bg=lcolor,
                        activeforeground=ecolor,
                        activebackground='#963403',
                        font=('Roboto',8,'bold'),command=add_img
                        )             
            self.add_img_btn.bind("<Enter>", on_entera)
            self.add_img_btn.bind("<Leave>", on_leavea)
            self.add_img_btn.grid(row=2,column=1,pady=10,padx=10,sticky=W)
        
        self.profile_photo = Label(self.new_user_frame,text="Profile Picture")
        self.profile_photo.grid(row=2,column=2,padx=10,pady=10,sticky=W)    
        
        add_img_btn('Add Image','white',self.fg_title)
        
        def clear():
            self.clear_boxes()
            self.add_user_btn.config(state=ACTIVE)
        
        def clear_btn(text,ecolor,lcolor):
            def on_entera(e):
                self.clear_btn['background'] ='#a6201c'#ffcc66
                self.clear_btn['foreground']=ecolor #000d33

            def on_leavea(e):
                self.clear_btn['background'] = lcolor
                self.clear_btn['foreground']= ecolor

            self.clear_btn = Button(self.new_user_frame,text=text,
                        width=10,
                        height=2,
                        fg=ecolor,
                        border=0,
                        bg=lcolor,
                        activeforeground=ecolor,
                        activebackground='#a6201c',
                        font=('Roboto',8,'bold'),command=clear
                        )             
            self.clear_btn.bind("<Enter>", on_entera)
            self.clear_btn.bind("<Leave>", on_leavea)
            self.clear_btn.grid(row=2,column=3,pady=10,padx=10,sticky=W)
            
            
        clear_btn('Clear','white','#d9534f')
        
        self.buttons_frame = LabelFrame(self.manage_frame,bg=self.bg,fg=self.fg_title,bd=3,text='Commands',font=('Roboto',12,'bold'))
        self.buttons_frame.grid(row= 1,column=0,sticky=W,pady=10,padx=(20,0))
        def add_user_btn(text,ecolor,lcolor):
            def on_entera(e):
                self.add_user_btn['background'] = '#2e872e'
                self.add_user_btn['foreground']= ecolor  

            def on_leavea(e):
                self.add_user_btn['background'] = lcolor
                self.add_user_btn['foreground']= ecolor

            self.add_user_btn = Button(self.buttons_frame,text=text,
                        width=14,
                        height=2,
                        fg=ecolor,
                        border=0,
                        bg=lcolor,
                        activeforeground=ecolor,
                        activebackground='#2e872e',
                        font=('Roboto',8,'bold'),command=self.add_room_user)#self.add_room_user(self.fn_box.get().capitalize(),self.ln_box.get().capitalize(),self.pos_box.get().capitalize(),openfile)
                                     
            self.add_user_btn.bind("<Enter>", on_entera)
            self.add_user_btn.bind("<Leave>", on_leavea)
            self.add_user_btn.grid(row=0,column=0,pady=10,padx=10,sticky=W)            
            
        add_user_btn('Add Room User','white','#5cb85c')
        
        
        

        def update_btn(text,ecolor,lcolor):
            def on_entera(e):
                self.update_btn['background'] = '#963403'#ffcc66
                self.update_btn['foreground']= ecolor  #000d33

            def on_leavea(e):
                self.update_btn['background'] = lcolor
                self.update_btn['foreground']= ecolor

            self.update_btn = Button(self.buttons_frame,text=text,
                        width=10,
                        height=2,
                        fg=ecolor,
                        border=0,
                        bg=lcolor,
                        activeforeground=ecolor,
                        activebackground='#963403',
                        font=('Roboto',8,'bold'),command=self.update_room_user
                        )             
            self.update_btn.bind("<Enter>", on_entera)
            self.update_btn.bind("<Leave>", on_leavea)
            self.update_btn.grid(row=0,column=1,pady=10,padx=10,sticky=W)
            
        update_btn('Update','white',self.fg_title)
        def del_btn(text,ecolor,lcolor):
            def on_entera(e):
                self.del_btn['background'] ='#a6201c'#ffcc66
                self.del_btn['foreground']= ecolor  #000d33

            def on_leavea(e):
                self.del_btn['background'] = lcolor
                self.del_btn['foreground']= ecolor

            self.del_btn = Button(self.buttons_frame,text=text,
                        width=10,
                        height=2,
                        fg=ecolor,
                        border=0,
                        bg=lcolor,
                        activeforeground=ecolor,
                        activebackground='#a6201c',
                        font=('Roboto',8,'bold'),command=self.delete_one
                        )             
            self.del_btn.bind("<Enter>", on_entera)
            self.del_btn.bind("<Leave>", on_leavea)
            self.del_btn.grid(row=0,column=2,pady=10,padx=10,sticky=W)
            
        del_btn('Delete','white','#d9534f')
        def del_all_btn(text,ecolor,lcolor):
            def on_entera(e):
                self.del_all_btn['background'] = '#a6201c'#ffcc66
                self.del_all_btn['foreground']= ecolor  #000d33

            def on_leavea(e):
                self.del_all_btn['background'] = lcolor
                self.del_all_btn['foreground']= ecolor

            self.del_all_btn = Button(self.buttons_frame,text=text,
                        width=10,
                        height=2,
                        fg=ecolor,
                        border=0,
                        bg=lcolor,
                        activeforeground=ecolor,
                        activebackground='#a6201c',
                        font=('Roboto',8,'bold'),command=self.delete_all
                        )             
            self.del_all_btn.bind("<Enter>", on_entera)
            self.del_all_btn.bind("<Leave>", on_leavea)
            self.del_all_btn.grid(row=0,column=3,pady=10,padx=10,sticky=W)            
        del_all_btn('Delete All','white','#d9534f')

        self.search_frame = Frame(self.manage_frame,bg=bg)
        self.search_frame.grid(row=2,column=0,sticky=W,padx=(20,0))
        self.search_by = Label(self.search_frame,text='Search here: ',font=l,bg=bg,fg=fg)
        self.search_by.grid(row=4,column=0,sticky=W)
        self.search_var = StringVar()
        self.search_box = Entry(self.search_frame,bg=bg,fg = fg_box,textvariable=self.search_var,font=l)
        self.search_box.grid(row=4,column=1,sticky=W)
        def search_user_btn(text,ecolor,lcolor):
            def on_entera(e):
                self.search_room_user['background'] ='#03559c' #ffcc66
                self.search_room_user['foreground']= ecolor  #000d33

            def on_leavea(e):
                self.search_room_user['background'] = lcolor
                self.search_room_user['foreground']= ecolor

            self.search_room_user = Button(self.search_frame,text=text,
                        width=8,
                        height=2,
                        fg=ecolor,
                        border=0,
                        bg=lcolor,
                        activeforeground=ecolor,
                        activebackground='#03559c',
                        font=('Roboto',8,'bold'),command=self.search_user
                        )             
            self.search_room_user.bind("<Enter>", on_entera)
            self.search_room_user.bind("<Leave>", on_leavea)
            self.search_room_user.grid(row=4,column=2,pady=10,padx=10,sticky=W)
        
            
        search_user_btn('Search','white','#0275d8')
       
        def reset_tree_btn(text,ecolor,lcolor):
            def on_entera(e):
                self.reset_tree_btn['background'] = '#a6201c' #ffcc66
                self.reset_tree_btn['foreground']= ecolor  #000d33

            def on_leavea(e):
                self.reset_tree_btn['background'] = lcolor
                self.reset_tree_btn['foreground']= ecolor

            self.reset_tree_btn = Button(self.search_frame,text=text,
                        width=8,
                        height=2,
                        fg=ecolor,
                        border=0,
                        bg=lcolor,
                        activeforeground=ecolor,
                        activebackground= '#a6201c',
                        font=('Roboto',8,'bold'),command=self.reset_tree
                        )             
            self.reset_tree_btn.bind("<Enter>", on_entera)
            self.reset_tree_btn.bind("<Leave>", on_leavea)
            self.reset_tree_btn.grid(row=4,column=3,pady=10,padx=10,sticky=W)
        
            
        reset_tree_btn('Reset','white','#d9534f')
       
        self.treeview_frame = Frame(self.manage_frame)
        self.treeview_frame.grid(row=3,column=0,pady=20,padx=(20,0))
        
        #Add Style 
        self.style = ttk.Style()
        #Pick a theme
        self.style.theme_use("clam")
        #configure treeview colors
        self.style.configure('Treeview',
                            background= '#D3D3D3',
                            foreground = 'black',
                            rowheight = 25,
                            fieldbackground = '#D3D3D3')
        # Change selected color
        self.style.map('Treeview',background = [('selected','#000000')])
        #Create Treeview Frame
        self.tree_frame = Frame(self.treeview_frame)
        self.tree_frame.pack(pady=(10,0))
        #Create Treeview Scrollbar
        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)
        #Create Treeview
        self.treeview = ttk.Treeview(self.tree_frame,yscrollcommand=self.tree_scroll.set,selectmode='extended',height=8)
        self.treeview.pack(fill=BOTH)
        #Configure Scrollbar
        self.tree_scroll.config(command=self.treeview.yview)
        #Define Columns
        self.treeview['columns'] = ('ID','First Name', 'Last Name', 'Position','Added By','Date Added')
        #Format Columns 
        self.treeview.column('#0',width=80,stretch=NO)
        self.treeview.column('ID',width=50,anchor=W)
        self.treeview.column('First Name',width=140,anchor=W)
        self.treeview.column('Last Name',width=140,anchor=CENTER)
        self.treeview.column('Position',width=140,anchor=CENTER)
        self.treeview.column('Added By',width=140,anchor=CENTER)
        self.treeview.column('Date Added',width=140,anchor=CENTER)
        
        # Create Headings 
        self.treeview.heading('#0',text='Photo',anchor=W)
        self.treeview.heading('ID',text='ID',anchor=W)
        self.treeview.heading('First Name',text='First Name',anchor=W)
        self.treeview.heading('Last Name',text='Last Name',anchor=CENTER)
        self.treeview.heading('Position',text='Position',anchor=CENTER)
        self.treeview.heading('Added By',text='Added By',anchor=CENTER)
        self.treeview.heading('Date Added',text='Date Added',anchor=CENTER)
        

        #Create Striped row
        self.treeview.tag_configure('oddrow',background='white')
        self.treeview.tag_configure('evenrow',background='lightblue')
        
        #Add data to screen
        global count 
        count = 0
        #cursor.execute("SELECT * FROM users")
        conn = mysql.connector.connect(
                                host ="localhost",
                                user = "root",
                                password = "B)omerang1",
                                database = "doorsecurity"
                                )
        cursor = conn.cursor()   
        cursor.execute(''' select room_users.id,room_users.firstname,
        room_users.lastname,room_users.position,room_users.photo,admin.lastname,room_users.date_added
        from room_users join admin on room_users.admin_id = admin.admin_id;
        ''')
        records = cursor.fetchall()
        #result = cursor.fetchall()
        #print(result)
        #print(records)
        self.treeview.imglist= []
        for record in records:
            self.img = Image.open(io.BytesIO(record[4]))
            self.img.thumbnail((25,25)) # resize the image to desired size
            self.img = ImageTk.PhotoImage(self.img,master = self.manage_frame)
            if count % 2 ==0:
                self.treeview.insert(parent='',index='end', iid=count,text='',image =self.img,values=(record[0],record[1],record[2],record[3],record[5],record[6]),tags=('evenrow',))
                self.treeview.imglist.append(self.img)
            else:
                self.treeview.insert(parent='',index='end', iid=count,text='',image = self.img,values=(record[0],record[1],record[2],record[3],record[5],record[6]),tags=('oddrow',))
                self.treeview.imglist.append(self.img)
            count+=1
        self.treeview.bind("<ButtonRelease-1>",self.selected)