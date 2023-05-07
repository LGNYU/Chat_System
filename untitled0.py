# -*- coding: utf-8 -*-
"""
Created on Tue May 10 17:56:53 2022

@author: Patrick Shen
"""
from tkinter import *
import tkinter as tk
window=tk.Tk()
window.title("hello world")
window.geometry("200x100")
var=tk.StringVar()
label=tk.Label(window,textvariable=var,bg="green",font=("Arial",12), width=15,height=2)
label.pack()# or label.place()
on_hit=False
def hit_me():
    global on_hit
    if on_hit==False:
        on_hit=True
        var.set("you hit me")
    else:
        on_hit=False
        var.set("")
    
button=tk.Button(window,text="hit me",bg="green",width=15,height=2,command=hit_me)
button.pack()
window.mainloop()#refresh consistantly

