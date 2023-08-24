import tkinter as tk
from tkinter import messagebox

def get_button(window,text,command,fg='black'):
    
    button = tk.Button(window,
                        text=text,
                        activebackground='black',
                        activeforeground='white',
                        bg='white',
                        fg=fg,
                        command=command,
                        font=('Helvetica bold',18),
                        borderwidth=0,
                    )
    return button

def get_ima_label(window):
    label = tk.Label(window)
    label.grid(row=0,column=0)
    return label

def get_text(window,text,bg,font=False,fg='#1A0442'):
    label = tk.Label(window,text=text,bg=bg,font=font,fg=fg,)
    label.config(justify='center')
    return label

def get_entry(windows):
    inputxt = tk.Text(windows,height=1.5,width=13,font=('Arial',22))
    return inputxt

def msg_box(title,description):
    messagebox.showinfo(title,description)



