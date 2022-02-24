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
from changepass import ChangePassword

class Admin:
    def __init__(self) :
        self.bg = '#363433'
        self.fg_title = '#c95e06'
        self.fg = 'white'
        self.font =('Roboto',12,)
        self.title_font = ('Roboto',15,'bold')
    
  
        
    def selected(self,e):
        self.clear_boxes()
        self.selected = self.treeview.focus()
        values = self.treeview.item(self.selected,'values')
        
        self.id_box.insert(0,values[0])
        self.fn_box.insert(0,values[1])
        self.ln_box.insert(0,values[2])
        self.pos_box.insert(0,values[3])
        self.address_box.insert(0,values[4])
        self.age_box.insert(0,values[5])
        self.username_box.insert(0,values[6])
        self.add_admin_btn.config(state=DISABLED)
        self.password_box.config(state=DISABLED)
        self.confirm_box.config(state=DISABLED)
    def clear_boxes(self):
        self.id_box.delete(0,END) 
        self.fn_box.delete(0,END)
        self.ln_box.delete(0,END)
        self.pos_box.delete(0,END)
        self.address_box.delete(0,END) 
        self.age_box.delete(0,END) 
        self.username_box.delete(0,END)
        self.add_admin_btn.config(state=ACTIVE)
        self.password_box.config(state=NORMAL)
        self.confirm_box.config(state=NORMAL)
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
        elif (not self.age_box.get().isdigit()):
            messagebox.showwarning("Incorrect Age Input", "Please enter a number")
            self.age_box.delete(0,END)
        elif (not self.id_box.get().isdigit()):
            messagebox.showwarning("Incorrect ID Input", "Please enter a number")
            self.id_box.delete(0,END)
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
                    x = (self.id_box.get(),self.fn_box.get().capitalize(),self.ln_box.get().capitalize(),self.address_box.get().capitalize(),self.age_box.get(),self.pos_box.get().capitalize(),self.username_box.get(),self.hashed_pass,date_now)
                    cursor.execute(sql_command,x)
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Register Succesful",parent = self.root)
                    self.id_box.delete(0,END)
                    self.fn_box.delete(0,END)
                    self.ln_box.delete(0,END)
                    self.pos_box.delete(0,END)
                    self.pos_box.delete(0,END)
                    self.address_box.delete(0,END)
                    self.age_box.delete(0,END)
                    self.username_box.delete(0,END)
                    self.password_box.delete(0,END)
                    self.confirm_box.delete(0,END)
                    self.treeview.delete(*self.treeview.get_children())
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
                    cursor.execute(''' select * from admin;
                    ''')
                    records = cursor.fetchall()
                    #result = cursor.fetchall()
                    #print(result)
                    #print(records)
                    for record in records:
                        if count % 2 ==0:
                            self.treeview.insert(parent='',index='end', iid=count,text='',values=(record[0],record[1],record[2],record[5],record[3],record[4],record[6],record[8]),tags=('evenrow',))
                    
                        else:
                            self.treeview.insert(parent='',index='end', iid=count,text='',values=(record[0],record[1],record[2],record[5],record[3],record[4],record[6],record[8]),tags=('oddrow',))
                        count+=1
                    conn.commit()
                    conn.close()
            except Exception as es:
                messagebox.showerror('Error',f'Error due to  : {str(es)}',parent = self.root)  

    def update_admin(self):
            try:
                    selected = self.treeview.focus()
                    values = self.treeview.item(self.selected,'values')
                    self.treeview.item(selected,text='',values=(self.id_box.get(),self.fn_box.get(),self.ln_box.get(),self.pos_box.get(),self.address_box.get(),self.age_box.get(),self.username_box.get(),values[7]))
                    conn = mysql.connector.connect(
                            host ="localhost",
                            user = "root",
                            password = "B)omerang1",
                            database = "doorsecurity"
                                )
                    cursor = conn.cursor()
                    sql_update = '''update admin set admin_id=%s, firstname=%s ,lastname=%s,address=%s,age=%s,admin_position=%s,username=%s where admin_id=%s '''
                    admin_id = self.id_box.get()
                    fn = self.fn_box.get()
                    ln = self.ln_box.get()
                    address = self.address_box.get()
                    age = self.age_box.get()
                    pos = self.pos_box.get()
                    username = self.username_box.get()
                    inputs = (admin_id,fn,ln,address,age,pos,username,selected[0])
                    cursor.execute(sql_update,inputs)
                    conn.commit()
                    conn.close()
                    self.clear_boxes()
                    messagebox.showinfo("Success", "Update Successful", parent= self.root)
            except Exception as es:
                messagebox.showerror('Error',f'Error due to  : {str(es)}',parent = self.root)  
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
            sql_delete = '''delete from admin where admin_id = %s'''
                
            cursor.execute(sql_delete,(values[0],))
            conn.commit()
            conn.close()
            messagebox.showinfo("Deleted", "User Deleted")
              
        self.clear_boxes()
        self.add_admin_btn.config(state=ACTIVE)
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
            sql_delete = 'delete  from admin where admin_id=%s '
            values = [(a,) for a in ids_to_delete]
            cursor.executemany(sql_delete,values)
            conn.commit()
            conn.close()
        self.clear_boxes()
        self.add_admin_btn.config(state=ACTIVE)
    def clear_treeview(self):
        for record in self.treeview.get_children():
            self.treeview.delete(record) 
    def reset_tree(self):
        self.clear_treeview()
        self.search_box.delete(0,END)
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
        cursor.execute(''' select * from admin;
        ''')
        records = cursor.fetchall()
        for record in records:
            if count % 2 ==0:
                self.treeview.insert(parent='',index='end', iid=count,text='',values=(record[0],record[1],record[2],record[5],record[3],record[4],record[6],record[8]),tags=('evenrow',))
        
            else:
                self.treeview.insert(parent='',index='end', iid=count,text='',values=(record[0],record[1],record[2],record[5],record[3],record[4],record[6],record[8]),tags=('oddrow',))
            count+=1
        conn.commit()
        conn.close()
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
        query = "select admin_id,firstname,lastname,admin_position,address,age,username,date_added from admin where firstname LIKE '%"+search+"%' OR lastname LIKE '%"+search+"%'"
        cursor.execute(query)
        rows = cursor.fetchall()    
        conn.commit()
        self.clear_treeview()
        global count 
        count = 0

        for record in rows:
            if count % 2 ==0:
                self.treeview.insert(parent='',index='end', iid=count,text='',values=(record[0],record[1],record[2],record[5],record[3],record[4],record[6],record[8]),tags=('evenrow',))
        
            else:
                self.treeview.insert(parent='',index='end', iid=count,text='',values=(record[0],record[1],record[2],record[5],record[3],record[4],record[6],record[8]),tags=('oddrow',))
            count+=1

    def admin_management_form(self,root):
        self.root = Toplevel(root)
        self.root.geometry('900x1000')
        self.root.title("A D M I N  L I S T")
        self.root.resizable(0,0)
        #self.invalid_input = self.root.register(self.inValid)

        self.dashboard_frame = Frame(self.root,width=1360,height=1000,bg=self.bg)
        self.dashboard_frame.pack(fill=BOTH,expand=1)
        self.changepass = ChangePassword()
        def change_pass_btn(text,ecolor,lcolor):
            def on_entera(e):
                self.change_pass_btn['background'] ='#03559c' #ffcc66
                self.change_pass_btn['foreground']= ecolor  #000d33

            def on_leavea(e):
                self.change_pass_btn['background'] = lcolor
                self.change_pass_btn['foreground']= ecolor

            self.change_pass_btn = Button(self.dashboard_frame,text=text,
                        width=14,
                        height=3,
                        fg=ecolor,
                        border=0,
                        bg=lcolor,
                        activeforeground=ecolor,
                        activebackground='#03559c',
                        font=('Roboto',8,'bold'),command=lambda:self.changepass.changepass_form(self.root)
                        )             
            self.change_pass_btn.bind("<Enter>", on_entera)
            self.change_pass_btn.bind("<Leave>", on_leavea)
            self.change_pass_btn.pack(pady=(20,0),padx=20,anchor=NE)
        
            
        change_pass_btn('Change Password','white','#0275d8')
        title_lbl = Label(self.dashboard_frame,text='Admin Management',font=('Roboto',25,'bold'),bg=self.bg,fg=self.fg_title)
        title_lbl.pack()
        
        self.manage_frame = Frame(self.dashboard_frame,bg=self.bg)
        self.manage_frame.pack(fill=BOTH,expand=1)
        self.new_admin_frame = LabelFrame(self.manage_frame,bg=self.bg,text='Add Admin',bd=3,fg=self.fg_title,font=('Roboto',12,'bold'))
        self.new_admin_frame.grid(row=0,column=0,sticky=W,padx=(20,0))
        l = ('Roboto',10)
        bg = self.bg
        fg = self.fg
        fg_box = 'white'
        
        self.id_lbl = Label(self.new_admin_frame,text='ID: ',fg=fg,bg=bg,font=l)
        self.id_lbl.grid(row=0,column=0,sticky=W,padx=10)
        self.id_box = Entry(self.new_admin_frame,bg=bg,fg = fg_box,highlightthickness=1,highlightbackground=self.fg,font=l)
        self.id_box.grid(row=1,column=0,padx=10,sticky=W)
        
        self.fn_lbl = Label(self.new_admin_frame,text='First Name: ',fg=fg,bg=bg,font=l)
        self.fn_lbl.grid(row=0,column=1,sticky=W,padx=10)
        self.fn_box = Entry(self.new_admin_frame,bg=bg,fg = fg_box,highlightthickness=1,highlightbackground=self.fg,font=l)
        self.fn_box.grid(row=1,column=1,padx=10,sticky=W)
        self.ln_lbl = Label(self.new_admin_frame,text='Last Name: ',fg=fg,bg=bg,font=l)
        self.ln_lbl.grid(row=0,column=2,padx=10,sticky=W)
        self.ln_box = Entry(self.new_admin_frame,bg=bg,fg = fg_box,highlightthickness=1,highlightbackground='white',font=l)
        self.ln_box.grid(row=1,column=2,padx=10,sticky=W)
        self.pos_lbl = Label(self.new_admin_frame,text='Position: ',fg=fg,bg=bg,font=l)
        self.pos_lbl.grid(row=0,column=3,padx=10,sticky=W)
        self.pos_box = Entry(self.new_admin_frame,bg=bg,fg = fg_box,highlightthickness=1,highlightbackground='white',font=l)
        self.pos_box.grid(row=1,column=3,padx=10,sticky=W)

        self.address_lbl = Label(self.new_admin_frame,text='Address:',fg=fg,bg=bg,font=l)
        self.address_lbl.grid(row=2,column=0,padx=10,sticky=W)
        self.address_box = Entry(self.new_admin_frame,bg=bg,fg = fg_box,highlightthickness=1,highlightbackground='white',font=l)
        self.address_box.grid(row=3,column=0,padx=10,sticky=W)

        self.age_lbl = Label(self.new_admin_frame,text='Age:',fg=fg,bg=bg,font=l)
        self.age_lbl.grid(row=2,column=1,padx=10,sticky=W)
        self.age_box = Entry(self.new_admin_frame,bg=bg,fg = fg_box,highlightthickness=1,highlightbackground='white',font=l)
        self.age_box.grid(row=3,column=1,padx=10,sticky=W)

        self.username_lbl = Label(self.new_admin_frame,text='Username:',fg=fg,bg=bg,font=l)
        self.username_lbl.grid(row=2,column=2,padx=10,sticky=W)
        self.username_box = Entry(self.new_admin_frame,bg=bg,fg = fg_box,highlightthickness=1,highlightbackground='white',font=l)
        self.username_box.grid(row=3,column=2,padx=10,sticky=W)

        self.password_lbl = Label(self.new_admin_frame,text='Password:',fg=fg,bg=bg,font=l)
        self.password_lbl.grid(row=2,column=3,padx=10,sticky=W)
        self.password_box = Entry(self.new_admin_frame,bg=bg,fg = fg_box,highlightthickness=1,highlightbackground='white',font=l,show="*")
        self.password_box.grid(row=3,column=3,padx=10,sticky=W)

        self.confirm_lbl = Label(self.new_admin_frame,text='Confirm Password:',fg=fg,bg=bg,font=l)
        self.confirm_lbl.grid(row=4,column=0,padx=10,sticky=W)
        self.confirm_box = Entry(self.new_admin_frame,bg=bg,fg = fg_box,highlightthickness=1,highlightbackground='white',font=l,show="*")
        self.confirm_box.grid(row=5,column=0,padx=10,sticky=W)

        def clear_btn(text,ecolor,lcolor):
            def on_entera(e):
                self.clear_btn['background'] ='#a6201c'#ffcc66
                self.clear_btn['foreground']=ecolor #000d33

            def on_leavea(e):
                self.clear_btn['background'] = lcolor   
                self.clear_btn['foreground']= ecolor

            self.clear_btn = Button(self.new_admin_frame,text=text,
                        width=10,
                        height=1,
                        fg=ecolor,
                        border=0,
                        bg=lcolor,
                        activeforeground=ecolor,
                        activebackground='#a6201c',
                        font=('Roboto',8,'bold'),command=self.clear_boxes
                        )             
            self.clear_btn.bind("<Enter>", on_entera)
            self.clear_btn.bind("<Leave>", on_leavea)
            self.clear_btn.grid(row=5,column=1,pady=10,padx=10,sticky=W)
            
            
        clear_btn('Clear','white','#d9534f')
        self.buttons_frame = LabelFrame(self.manage_frame,bg=self.bg,fg=self.fg_title,bd=3,text='Commands',font=('Roboto',12,'bold'))
        self.buttons_frame.grid(row= 1,column=0,sticky=W,pady=10,padx=(20,0))
        def add_admin_btn(text,ecolor,lcolor):
            def on_entera(e):
                self.add_admin_btn['background'] = '#2e872e'
                self.add_admin_btn['foreground']= ecolor  

            def on_leavea(e):
                self.add_admin_btn['background'] = lcolor
                self.add_admin_btn['foreground']= ecolor

            self.add_admin_btn = Button(self.buttons_frame,text=text,
                        width=14,
                        height=2,
                        fg=ecolor,
                        border=0,
                        bg=lcolor,
                        activeforeground=ecolor,
                        activebackground='#2e872e',
                        font=('Roboto',8,'bold'),command=self.add_admin
                        )             
            self.add_admin_btn.bind("<Enter>", on_entera)
            self.add_admin_btn.bind("<Leave>", on_leavea)
            self.add_admin_btn.grid(row=0,column=0,pady=10,padx=10,sticky=W)            
            
        add_admin_btn('Add Room User','white','#5cb85c')
        
        
        

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
                        font=('Roboto',8,'bold'),command=self.update_admin
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
        self.treeview['columns'] = ('ID','First Name', 'Last Name', 'Position','Address','Age','Username','Date Added')
        #Format Columns 
        self.treeview.column('#0',width=0,stretch=NO)
        self.treeview.column('ID',width=80,anchor=W)
        self.treeview.column('First Name',width=100,anchor=W)
        self.treeview.column('Last Name',width=100,anchor=CENTER)
        self.treeview.column('Position',width=100,anchor=CENTER)
        self.treeview.column('Address',width=140,anchor=CENTER)
        self.treeview.column('Age',width=80,anchor=CENTER)
        self.treeview.column('Username',width=100,anchor=CENTER)
        self.treeview.column('Date Added',width=140,anchor=CENTER)
        
        # Create Headings 
        self.treeview.heading('ID',text='ID',anchor=W)
        self.treeview.heading('First Name',text='First Name',anchor=W)
        self.treeview.heading('Last Name',text='Last Name',anchor=CENTER)
        self.treeview.heading('Position',text='Position',anchor=CENTER)
        self.treeview.heading('Address',text='Address',anchor=CENTER)
        self.treeview.heading('Age',text='Age',anchor=CENTER)
        self.treeview.heading('Username',text='Username',anchor=CENTER)
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
        cursor.execute(''' select * from admin;
        ''')
        records = cursor.fetchall()
        #result = cursor.fetchall()
        #print(result)
        #print(records)
        for record in records:
            if count % 2 ==0:
                self.treeview.insert(parent='',index='end', iid=count,text='',values=(record[0],record[1],record[2],record[5],record[3],record[4],record[6],record[8]),tags=('evenrow',))
        
            else:
                self.treeview.insert(parent='',index='end', iid=count,text='',values=(record[0],record[1],record[2],record[5],record[3],record[4],record[6],record[8]),tags=('oddrow',))
            count+=1
        self.treeview.bind("<ButtonRelease-1>",self.selected)