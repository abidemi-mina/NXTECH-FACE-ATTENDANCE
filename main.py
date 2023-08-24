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
        self.main_window.geometry('720x400+400+100') # the size of the window and postion the screen
        self.main_window.config(background='#B027EF')
        self.main_window.title('Face recognition attendance App')

        self.welcone_text= util.get_text(self.main_window,'Welcome back.\nLogin to continue or signup \nif not registered','#B027EF',('sans-serif',15,'bold'))
        self.welcone_text.place(x=430,y=50)#position the welcome text
        
        self.login_button_main_window = util.get_button(self.main_window,'Login',self.login)
        self.login_button_main_window.place(x=480,y=160,width=190) # to position the button
        self.register_new_user_button_main_window = util.get_button(self.main_window,'Sign up',self.register_new_user)
        self.register_new_user_button_main_window.place(x=480,y=300,width=190)# to position the button
        self.sign_up_text= util.get_text(self.main_window,'Note:Ensure to be in a good position \nbefore capture','#AF28F0',('sans-serif',12,'bold'),'white')
        self.sign_up_text.place(y=250,x=430)
       
        #image section
        self.webcam_window = util.get_ima_label(self.main_window)
        self.webcam_window.place(x=16,y=30,width=400,height=350)

        # adding the webcam in the image label
        self.access_webcam(self.webcam_window)
        #  to save the datas
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)
        self.log = './log.txt'

#the live camera
    def access_webcam(self,label):
        if 'cap'not in self.__dict__:# if the camera variable is not created
            self.cap=cv2.VideoCapture(0) # access the camera
        self._label = label
        self.process_webcam()#

#camera section
    def process_webcam(self):
        ''' reframing the webcam image from opencv to pillow format ''' 

        ret,frame= self.cap.read()
        self.most_recent_cap_arr = frame
        img = cv2.cvtColor(self.most_recent_cap_arr,cv2.COLOR_BGR2RGB) # color conversion in form of numpy array
        self.most_recent_cap_pil = Image.fromarray(img) # conversion to pil
        imgtk = ImageTk.PhotoImage(self.most_recent_cap_pil) # modifying the image on tkinter 
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        self._label.after(20,self.process_webcam) #re takes video after 20 seconds


   

    def register_new_user(self):
        self.register_window = tk.Toplevel(self.main_window) # creating a new window
        self.register_window.geometry('720x400+400+100') # the size of the window
        self.register_window.config(background='#B027EF')
        self.register_window.title('Registration page') # the name of the window
        self.accept_registered_user_btn = util.get_button(self.register_window,'Accept',self.accept_registered_user,'green')
        self.accept_registered_user_btn.place(x=465,y=230,width=190) # to position the button
        self.try_again_register_new_user_btn = util.get_button(self.register_window,'Try again',self.try_again,'red')
        self.try_again_register_new_user_btn.place(x=465,y=300,width=190)# to position the button

        self.cap_window = util.get_ima_label(self.register_window)
        self.cap_window.place(x=16,y=30,width=400,height=350)

        #adds captured image
        self.add_cap_window(self.cap_window)
        self.entry_text = util.get_entry(self.register_window)
        self.entry_text.place(x=460,y=100) # to position the button
        self.text_label = util.get_text(self.register_window,'Please input username','#B027EF',('sans-serif',15,'bold'))
        self.text_label.place(x=460,y=50) # to position the button

#

    def login(self):
        unknown_img_path ='./.tmp.jpg'
        cv2.imwrite(unknown_img_path,self.most_recent_cap_arr)


        # checks if the images exists
        output = str(subprocess.check_output(['face_recognition',self.db_dir,unknown_img_path],stderr=subprocess.STDOUT,shell=True)) #
        print(output)
        name =output.split(',')[1][:-5]
        
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
        '''captures image from the webcam'''
        imgtk = ImageTk.PhotoImage(self.most_recent_cap_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.new_user_capture = self.most_recent_cap_arr.copy()
        
    def accept_registered_user(self):
        unknown_img_path ='./.tmp.jpg'
        cv2.imwrite(unknown_img_path,self.most_recent_cap_arr)
        output = str(subprocess.check_output(['face_recognition',self.db_dir,unknown_img_path],stderr=subprocess.STDOUT,shell=True))
        user =output.split(',')[1][:-5]

        # checks if the user exists
        if user not  in ['no_persons_found','unknown_person']:
            util.msg_box('Ups!!!',user+' please login')
            self.register_window.destroy()
        else:
            name = self.entry_text.get(1.0,'end-1c')
            img= np.array(self.new_user_capture) # it has to be an array
            cv2.imwrite(os.path.join(self.db_dir,f'{name}.jpg'), img)# saving the image
            util.msg_box('Success','User was registered successfully') # message 
            self.register_window.destroy() # to kill the current window 


    def try_again(self):
        self.register_window.destroy() # to kill the current window 

    def start(self):
        self.main_window.mainloop() # to start the application

if __name__ == '__main__':
    app = App()
    app.start()