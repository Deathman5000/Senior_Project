# UI.py

import openpyxl
from typing import List
from tkinter import *
import tkinter.messagebox as tm
import tkinter.filedialog as fd
import threading

import AI_Manager

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
		self.switch_frame( LoginFrame( self ) )

	def switch_frame( self, new_frame: Frame ):
		#Destroys current frame and replaces it with a new one.
		if self._frame is not None:
			self._frame.destroy()

		self._frame = new_frame
		self.update()


class LoginFrame( Frame ):
	def __init__( self, input_master: Tk ):

		self._master = input_master
		super().__init__( input_master )

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
		self._master.switch_frame( Choiceframe( self._master ) )

		#if username == "admin" and password == "password":
		#    tm.showinfo( "Login info", "admin accepted" )
		#else:
		#    tm.showerror( "Login error", "Incorrect username" )


class Choiceframe( Frame ):
	def __init__( self, input_master: Tk ):

		self._master = input_master
		super().__init__( input_master )

		self.enter_button = Button( self, text = "Enter Data", command = self._enter_clicked )
		self.import_button = Button( self, text = "Import File", command = self._import_clicked )

		self.enter_button.grid( row = 0, sticky = E )
		self.import_button.grid( row = 0, column = 1 )

		self.pack( anchor = "nw" )

	def _enter_clicked( self ):
		self._master.switch_frame( EnterDataframe( self._master ) )

	def _import_clicked( self ):
		file_path = fd.askopenfilename()

		if file_path: # if a file was selected
			try:
				# Open file and load workbook
				workbook = openpyxl.load_workbook( file_path, read_only = True )

			except openpyxl.utils.exceptions.InvalidFileException:
				tm.showerror( "File error", "Unable to open file as XLSX file" )
				return

			## pass workbook to loading frame
			self._master.switch_frame( Loadingframe( self._master, "File loading.", ResultFrame, subprocess_workbook, [ workbook ] ) )

def subprocess_workbook( input_workbook: openpyxl.Workbook, caller: Frame, target_frame: Frame ):

	data_array = AI_Manager.process_workbook( input_workbook )

	# waits until the loading frame that called this is completely loaded
	while not caller._master._frame == caller:
		pass

	caller._master.switch_frame( target_frame( caller._master, data_array ) )


class Loadingframe( Frame ):
	def __init__( self, input_master: Tk, loading_text: StringVar, target_frame: Frame, todo_function, todo_arguments ):

		self._master = input_master

		workbook_thread = threading.Thread( target = todo_function, args = todo_arguments + [ self, target_frame ] )
		workbook_thread.start()

		super().__init__( self._master )

		self.default_label = Label( self, text = loading_text )
		self.default_label.pack( anchor = "nw" )

		self.pack( anchor = "nw" )


class EnterDataframe( Frame ):
	def __init__( self, input_master: Tk ):

		self._master = input_master
		super().__init__( input_master )

		self.default_label_1 = Label( self, text = "Type in the values into each box and" )
		self.default_label_2 = Label( self, text = "then click Next Data Point or Continue." )

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

		self.data = {}

		self.pack( anchor = "nw" )

	def _next_clicked( self ):
		time_text = self.time_entry.get()
		value_text = self.value_entry.get()

		if time_text or value_text:		# if the entries are not empty
			try:
				time_ = float( time_text )
				value_ = float( value_text )
			except ValueError:
				tm.showinfo( "Input Error", "Invalid entry" )
				return

			# append data to data collected
			self.data.update( { time_: value_ } )

			# clear entrys
			self.time_entry.delete( 0, END )
			self.value_entry.delete( 0, END )

	def _continue_clicked( self ):
		time_text = self.time_entry.get()
		value_text = self.value_entry.get()

		if time_text or value_text:		# if the entries are not empty
			try:
				time_ = float( time_text )
				value_ = float( value_text )
			except ValueError:
				tm.showinfo( "Input Error", "Invalid entry" )
				return

			# append data to data collected
			self.data.update( { time_: value_ } )

		# continue only if data is not empty
		if self.data == {}:
			return

		keys = list( self.data.keys() )
		keys.sort()

		# organize time and value into two ordered lists
		data_array = [ keys, [ self.data[ index ] for index in keys ] ]

		## pass data to AI algorithm
		self._master.switch_frame( ResultFrame( self._master, data_array ) )


class ResultFrame( Frame ):
	def __init__( self, input_master: Tk, input_data: List[ float ] ):

		self._master = input_master
		super().__init__( input_master )

		for column_index, column in enumerate( input_data ):
			for row_index, value in enumerate( column ):
				default_label = Label( self, text = value )
				default_label.grid( row = row_index, column = column_index )

		#self.default_label_1.grid( row = 0, sticky = E )

		self.pack( anchor = "nw" )


class TopMenu( Menu ):
	def __init__( self, input_master: Tk ):

		self._master = input_master
		super().__init__( input_master )

		self._master.configure( menu = self )

		self.sub_menu = Menu( self._master, tearoff = 0 )
		self.add_cascade( menu = self.sub_menu, label = "File" )
		self.sub_menu.add_command( label = "Log out", command = self._Log_out_selected )
		self.sub_menu.add_command( label = "Reset", command = self._Reset_selected )
		self.sub_menu.add_command( label = "Exit", command = self._Exit_selected )

	def _Log_out_selected(self):
		global LOGGED_IN

		if( LOGGED_IN ):
			LOGGED_IN = False
			self._master.switch_frame( LoginFrame( self._master ) )

	def _Reset_selected( self ):
		global LOGGED_IN

		if( LOGGED_IN ):
			self._master.switch_frame( Choiceframe( self._master ) )

	def _Exit_selected( self ):
		# log out for consistancy
		global LOGGED_IN
		LOGGED_IN = False

		self._master.destroy()
		self._master = None
		# this exits the program


if __name__ == "__main__":
	app = Application()
	app.mainloop()
