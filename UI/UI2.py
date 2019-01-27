#! /usr/bin/env python

from tkinter import *
import tkinter.messagebox as tm

WIDTH = 350
HEIGHT = 460
LOGGED_IN = False

class Application( Tk ):
	def __init__( self ):
		Tk.__init__( self) 
		self.title( "GeLP" )
		#self.geometry( '{}x{}'.format( WIDTH, HEIGHT) )
		#self.resizable( 0, 0 ) # this prevents from resizing the window
		self._menu = TopMenu( self )
		self._frame = None
		self.switch_frame( LoginFrame )

	def switch_frame( self, frame_class ):
		#Destroys current frame and replaces it with a new one.
		new_frame = frame_class( self )

		if self._frame is not None:
			self._frame.destroy()

		self._frame = new_frame

class LoginFrame( Frame ):
	def __init__( self, master ):
		super().__init__( master )

		self.label_username = Label( self, text = "Username" )
		self.label_password = Label( self, text = "Password" )

		self.entry_username = Entry( self )
		self.entry_password = Entry( self, show = "*" )

		self.label_username.grid( row = 0, sticky = E )
		self.label_password.grid( row = 1, sticky = E )
		self.entry_username.grid( row = 0, column = 1 )
		self.entry_password.grid( row = 1, column = 1 )

		self.logbtn = Button( self, text = "Login", command = self._login_btn_clicked )
		self.logbtn.grid( columnspan = 2 )

		self.pack( anchor = "nw" )

	def _login_btn_clicked( self ):
		username = self.entry_username.get()
		password = self.entry_password.get()
		
		tm.showinfo( "Login info", "Login not implemented.\nAccess unrestricted." )

		global LOGGED_IN
		LOGGED_IN = True
		self.master.switch_frame( second_frame )

		#if username == "admin" and password == "password":
		#    tm.showinfo( "Login info", "admin accepted" )
		#else:
		#    tm.showerror( "Login error", "Incorrect username" )


class second_frame( Frame ):
	def __init__( self, master ):
		super().__init__( master )

		self.text_1 = Label( self, text = "Sample Text" )
		self.text_1.pack( anchor = "nw" )

		self.pack( anchor = "nw" )

class TopMenu( Menu ):
	def __init__( self, master ):
		super().__init__( master )

		master.configure( menu = self )

		self.sub_menu = Menu( master, tearoff = 0 )
		self.add_cascade( menu = self.sub_menu, label = "File" )
		self.sub_menu.add_command( label = "Log out", command = self._Log_out_selected )
		self.sub_menu.add_command( label = "Reset", command = self._Reset_selected )
		self.sub_menu.add_command( label = "Exit", command = self._Exit_selected )

	def _Log_out_selected(self):
		global LOGGED_IN

		if( LOGGED_IN ):
			LOGGED_IN = False
			self.master.switch_frame( LoginFrame )

	def _Reset_selected(self):
		global LOGGED_IN

		if( LOGGED_IN ):
			self.master.switch_frame( second_frame )

	def _Exit_selected( self ):
		self.master.destroy()
		self.master = None
		# this exits the program


if __name__ == "__main__":
    app = Application()
    app.mainloop()
