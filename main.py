from genericpath import exists
import subprocess
from sys import stdout
import tkinter as tk
import util
import cv2
from PIL import Image,ImageTk
import os
import numpy as np
import datetime
class App:
    def __init__(self):
        self.main_window  = tk.Tk() # creating a window 
        self.main_window.geometry('1200x520+350+100') # the size of the window
        
        self.login_button_main_window = util.get_button(self.main_window,'login','green',self.login)
        self.login_button_main_window.place(x=750,y=300) # to position the button
        self.register_new_user_button_main_window = util.get_button(self.main_window,'Register new user','grey',self.register_new_user,fg='black')
        self.register_new_user_button_main_window.place(x=750,y=400)# to position the button
        self.webcam_window = util.get_ima_label(self.main_window)
        self.webcam_window.place(x=18,y=8,width=700,height=500)
        self.add_webcam(self.webcam_window)
        #  to save the datas
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
        self.log = './log.txt'


    def add_webcam(self,label):
        if 'cap'not in self.__dict__:
            self.cap=cv2.VideoCapture(0)
        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret,frame= self.cap.read()
        self.most_recent_cap_arr = frame
        img = cv2.cvtColor(self.most_recent_cap_arr,cv2.COLOR_BGR2RGB)
        self.most_recent_cap_pil = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(self.most_recent_cap_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        self._label.after(20,self.process_webcam)


    def start(self):
        self.main_window.mainloop() # to start the application

    def register_new_user(self):
        self.register_window = tk.Toplevel(self.main_window) # creating a new window
        self.register_window.geometry('1200x520+370+120') # the size of the window
        self.accept_registered_user_btn = util.get_button(self.register_window,'Accept','green',self.accept_registered_user)
        self.accept_registered_user_btn.place(x=750,y=300) # to position the button
        self.try_again_register_new_user_btn = util.get_button(self.register_window,'Try again','red',self.try_again,fg='black')
        self.try_again_register_new_user_btn.place(x=750,y=400)# to position the button

        self.cap_window = util.get_ima_label(self.register_window)
        self.cap_window.place(x=18,y=8,width=700,height=500)
        self.add_cap_window(self.cap_window)
        self.entry_text = util.get_entry(self.register_window)
        self.entry_text.place(x=750,y=170) # to position the button
        self.text_label = util.get_text(self.register_window,'Please \ninput username')
        self.text_label.place(x=750,y=100) # to position the button

#

    def login(self):
        unknown_img_path ='./.tmp.jpg'
        cv2.imwrite(unknown_img_path,self.most_recent_cap_arr)
        # try:
        output = str(subprocess.check_output(['face_recognition',self.db_dir,unknown_img_path],stderr=subprocess.STDOUT,shell=True))
        name =output.split(',')[1][:-5]
        # except subprocess.CalledProcessError as e:
        #     raise RuntimeError(f'command {e.cmd} return with error (code {e.returncode}):{e.output}')
        os.remove(unknown_img_path)
        print(name)
        if name in ['no_persons_found','unknown_person']:
            util.msg_box('Ups!!!','Unknown user. Please register')
        else:
            util.msg_box('Welcome back',f'Welcome {name}')
            with open(self.log,'a') as f:
                f.write(f'\n{name},{datetime.datetime.now()}')
                f.close()

    
    
    def add_cap_window(self,label):
        imgtk = ImageTk.PhotoImage(self.most_recent_cap_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.new_user_capture = self.most_recent_cap_arr.copy()
        
    def accept_registered_user(self):
        name = self.entry_text.get(1.0,'end-1c')
        img= np.array(self.new_user_capture) # it has to be an array
        cv2.imwrite(os.path.join(self.db_dir,f'{name}.jpg'), img)
        util.msg_box('Success','User was registered successfully') # message 
        self.register_window.destroy() # to kill the current window 


    def try_again(self):
        self.register_window.destroy() # to kill the current window 


if __name__ == '__main__':
    app = App()
    app.start()