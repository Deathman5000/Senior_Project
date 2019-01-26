#! /usr/bin/env python

from tkinter import *
import tkinter.messagebox as tm

WIDTH = 350
HEIGHT = 460

class LoginFrame( Frame ):
    def __init__( self, master ):
        super().__init__( master )

        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        #self.checkbox = Checkbutton(self, text="Keep me logged in")
        #self.checkbox.grid(columnspan=2)

        self.logbtn = Button(self, text="Login", command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=2)

        self.pack( anchor = "nw" )

    def _login_btn_clicked(self):
        # print("Clicked")
        username = self.entry_username.get()
        password = self.entry_password.get()

        # print(username, password)
		
        tm.showinfo( "Login info", "Login not implemented.\nAccess unrestricted." )

        #if username == "admin" and password == "password":
        #    tm.showinfo( "Login info", "admin accepted" )
        #else:
        #    tm.showerror( "Login error", "Incorrect username" )


root = Tk()

root.title( "Test UI for AI" )
#root.geometry( '{}x{}'.format( WIDTH, HEIGHT) )
#root.resizable( 0, 0 ) # this prevents from resizing the window

lf = LoginFrame(root)
root.mainloop()
