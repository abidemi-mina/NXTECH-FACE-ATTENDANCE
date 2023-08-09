import tkinter as tk
from tkinter import messagebox

def get_button(window,text,color,command,fg='white'):
    button = tk.Button(window,
                        text=text,
                        activebackground='black',
                        activeforeground='white',
                        bg=color,
                        fg=fg,
                        command=command,
                        height=2,
                        width=28,
                        font=('Helvetica bold',20)
                    )
    return button

def get_ima_label(window):
    label = tk.Label(window)
    label.grid(row=0,column=0)
    return label

def get_text(window,text):
    label = tk.Label(window,text=text)
    label.config(font=('sans-serif',21),justify='left')
    return label

def get_entry(windows):
    inputxt = tk.Text(windows,height=2,width=15,font=('Arial',32))
    return inputxt

def msg_box(title,description):
    messagebox.showinfo(title,description)



