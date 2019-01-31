#! /usr/bin/env python

from tkinter import *
import tkinter.messagebox as tm
import tkinter.filedialog as fd

WIDTH = 350
HEIGHT = 460
LOGGED_IN = False

class Application( Tk ):
	def __init__( self ):
		super().__init__()
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

		self.label_username = Label( self, text = "Username:" )
		self.label_password = Label( self, text = "Password:" )

		self.entry_username = Entry( self )
		self.entry_password = Entry( self, show = "*" )

		self.label_username.grid( row = 0, sticky = E )
		self.label_password.grid( row = 1, sticky = E )
		self.entry_username.grid( row = 0, column = 1 )
		self.entry_password.grid( row = 1, column = 1 )

		self.login_button = Button( self, text = "Login", command = self._login_clicked )
		self.login_button.grid( columnspan = 2 )

		self.pack( anchor = "nw" )

	def _login_clicked( self ):
		username = self.entry_username.get()
		password = self.entry_password.get()

		tm.showinfo( "Login info", "Login not implemented.\nAccess unrestricted." )

		global LOGGED_IN
		LOGGED_IN = True
		self.master.switch_frame( Choiceframe )

		#if username == "admin" and password == "password":
		#    tm.showinfo( "Login info", "admin accepted" )
		#else:
		#    tm.showerror( "Login error", "Incorrect username" )


class Choiceframe( Frame ):
	def __init__( self, master ):
		super().__init__( master )

		self.enter_button = Button( self, text = "Enter Data", command = self._enter_clicked )
		self.import_button = Button( self, text = "Import File", command = self._import_clicked )

		self.enter_button.grid( row = 0, sticky = E )
		self.import_button.grid( row = 0, column = 1 )

		self.pack( anchor = "nw" )

	def _enter_clicked( self ):
		self.master.switch_frame( EnterDataframe )

	def _import_clicked( self ):
		file_path = fd.askopenfilename()

		if file_path:
			#check file type
			#pass file to file processing
			#pass data in file to AI algorithm
			self.master.switch_frame( ResultFrame )


class EnterDataframe( Frame ):
	def __init__( self, master ):
		super().__init__( master )

		self.default_label_1 = Label( self, text = "Type in the values into each box and" )
		self.default_label_2 = Label( self, text = "then click next data point or continue." )

		self.time_entry = Entry( self )
		self.value_entry = Entry( self )

		self.next_button = Button( self, text = "Next Data Point", command = self._next_clicked )
		self.continue_button = Button( self, text = "Continue", command = self._continue_clicked )

		self.default_label_1.grid( row = 0, sticky = W, columnspan = 2 )
		self.default_label_2.grid( row = 1, sticky = W, columnspan = 2 )
		self.time_entry.grid( row = 2, sticky = E )
		self.value_entry.grid( row = 2, column = 1 )
		self.next_button.grid( row = 3, sticky = E )
		self.continue_button.grid( row = 3, column = 1 )

		self.pack( anchor = "nw" )

	def _next_clicked( self ):
		# append data to data collected
		tm.showinfo( "Button info", "Button not implemented.\nNo action." )

	def _continue_clicked( self ):
		# append data to data collected
		#pass data to AI algorithm
		self.master.switch_frame( ResultFrame )


class ResultFrame( Frame ):
	def __init__( self, master ):
		super().__init__( master )

		self.default_label_1 = Label( self, text = "Result Frame." )
		self.default_label_2 = Label( self, text = "Frame not implemented." )
		self.default_label_3 = Label( self, text = "No progression." )

		self.default_label_1.pack( anchor = "nw" )
		self.default_label_2.pack( anchor = "nw" )
		self.default_label_3.pack( anchor = "nw" )

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
			self.master.switch_frame( Choiceframe )

	def _Exit_selected( self ):
		self.master.destroy()
		self.master = None
		# this exits the program


if __name__ == "__main__":
    app = Application()
app.mainloop()
