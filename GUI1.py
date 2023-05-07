#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 13:36:58 2021

@author: bing
"""

# import all the required  modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from chat_utils import *
import json
import chat_group
from main import *
# GUI class for the chat


class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""

    def login(self):
        # login window
        self.login = Toplevel()
        # set the title
        self.login.title("Login")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=400,
                             height=300)
        # create a Label
        self.pls = Label(self.login,
                         text="Please login to continue",
                         justify=CENTER,
                         font="Helvetica 14 bold")

        self.pls.place(relheight=0.15,
                       relx=0.2,
                       rely=0.07)
        # create a Label
        self.labelName = Label(self.login,
                               text="Name: ",
                               font="Helvetica 12")

        self.labelName.place(relheight=0.2,
                             relx=0.1,
                             rely=0.2)

        # create a entry box for
        # tyoing the message
        self.entryName = Entry(self.login,
                               font="Helvetica 14")

        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)

        # set the focus of the curser
        self.entryName.focus()

        # 创建password
        self.labelpassword = Label(self.login, text="Password: ", font="Helvetica 12")
        
        self.labelpassword.place(relheight=0.2,
                                 relx=0.1,
                                 rely=0.4)
        
        self.passwordentry = Entry(self.login, font="Helvetica 14")

        self.passwordentry.place(relwidth=0.4,
                                 relheight=0.12,
                                 relx=0.35,
                                 rely=0.4)

        # create a Continue Button
        # along with action
        self.go = Button(self.login,
                         text="CONTINUE",
                         font="Helvetica 14 bold",
                         command=lambda: self.goAhead(self.entryName.get()))

        self.go.place(relx=0.4,
                      rely=0.55)

        # 创建sign up button
        self.signup = Button(self.login,
                             text="Sign Up Here",
                             font="Helvetica 14 bold",
                             command=lambda: self.sign_up_GUI())
        self.signup.place(relx=0.4, rely=0.65)
        self.Window.mainloop()
    
    def sign_up_GUI(self):
        self.signup = Toplevel()
        self.signup.title("Sign Up")
        self.signup.resizable(width=False,
                             height=False)
        self.signup.configure(width=400,
                             height=300)
        self.prompt = Label(self.signup,
                            text="Please enter your name and password",
                            justify=CENTER,
                            font="Helvetica 14 bold")

        self.prompt.place(relheight=0.15,
                          relx=0.2,
                          rely=0.07)
        # create a Label
        self.newlabelName = Label(self.signup,
                               text="Name: ",
                               font="Helvetica 12")

        self.newlabelName.place(relheight=0.2,
                                relx=0.1,
                                rely=0.2)

        # create a entry box for
        # tyoing the message
        self.newentryName = Entry(self.signup,
                                  font="Helvetica 14")

        self.newentryName.place(relwidth=0.4,
                                relheight=0.12,
                                relx=0.35,
                                rely=0.2)

        # set the focus of the curser
        self.newentryName.focus()

        # 创建password
        self.newlabelpassword = Label(self.signup, text="Password: ", font="Helvetica 12")
        
        self.newlabelpassword.place(relheight=0.2,
                                    relx=0.1,
                                    rely=0.4)
        
        self.newpasswordentry = Entry(self.signup, font="Helvetica 14")

        self.newpasswordentry.place(relwidth=0.4,
                                    relheight=0.12,
                                    relx=0.35,
                                    rely=0.4)

        # create a Create Button
        # along with action
        self.create = Button(self.signup,
                             text="Create",
                             font="Helvetica 14 bold")
        self.create.place(relx=0.4,
                          rely=0.55)

        
        

    def goAhead(self, name):
        if len(name) > 0:
            msg = json.dumps({"action": "login", "name": name})
            self.send(msg)
            response = json.loads(self.recv())
            if response["status"] == 'ok':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                self.layout(name)
                self.textCons.config(state=NORMAL)
                # self.textCons.insert(END, "hello" +"\n\n")
                self.textCons.insert(END, menu + "\n\n")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)
                # while True:
                #     self.proc()
            
            
        # the thread to receive messages
            process = threading.Thread(target=self.proc)
            process.daemon = True
            process.start()

    # The main layout of the chat
    def layout(self, name):

        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=470,
                              height=550,
                              bg="#17202A")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)

        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9")

        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)

        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)

        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)

        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)

        self.entryMsg.focus()

        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.03,
                             relwidth=0.22)

        self.textCons.config(cursor="arrow")

        #

        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)

        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)

        self.time_button=Button(self.labelBottom,text="Time",font="Helvetica 7",bg="#ABB2B9",command=lambda:self.insert_time())
        self.time_button.place(relwidth=0.22,relheight=0.03,rely=0.038,relx=0.55)
        self.time_button.focus()

        self.who_button=Button(self.labelBottom, text="Who",font="Helvetica 7",bg="#ABB2B9",command=lambda:self.insert_who())
        self.who_button.place(relwidth=0.22,relheight=0.03,rely=0.015,relx=0.55)
        self.who_button.focus()
        #create a game button
        self.start_game_button=Button(self.labelBottom,text="Start Game",font="Helvetica 7",bg="#ABB2B9",command=lambda:startGame())
        self.start_game_button.place(relwidth=0.22,
                            relheight=0.03,
                            rely=0.038,
                            relx=0.77)
        self.start_game_button.focus()

    # function to basically start the thread for sending messages

    def sendButton(self, msg):
        # self.textCons.config(state=DISABLED)
        self.my_msg = msg
        # print(msg)
        self.entryMsg.delete(0, END)
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, msg + "\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    def proc(self):
        # print(self.msg)
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            # print(self.msg)
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                # print(self.system_msg)
                self.system_msg = self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons.config(state=NORMAL)
                self.textCons.insert(END, self.system_msg + "\n\n")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)
    def insert_time(self):
            self.display_time_window=Toplevel()
        # set the title
            self.display_time_window.title("TIME")
            self.display_time_window.resizable(width=False,
                             height=False)
            self.display_time_window.configure(width=400,
                             height=300)
            self.display_time=Label(self.display_time_window,text=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),font="Helvetica 7")
            self.display_time.pack()
    
    def insert_who(self):
            self.display_who_window=Toplevel()
        # set the title
            self.display_who_window.title("WHO")
            self.display_who_window.resizable(width=False,height=False)
            self.display_who_window.configure(width=400,height=300)
            self.display_who=Label(self.display_time_window,text=chat_group.list_me(),font="Helvetica 7")
            self.display_who.pack()


    def run(self):
        self.login()


# create a GUI class object
if __name__ == "__main__":
    # g = GUI()
    pass
