# UI.py

import openpyxl
from typing import List
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
import threading
import hashlib
import binascii
import compare
import AI_Manager

WIDTH = 350
HEIGHT = 460
LOGGED_IN = False

"""
The window manager of the program
Every frame will exist inside this one
"""
class Application(Tk):
	def __init__(self):
		super().__init__()
		self.title("GeLP")
		# self.geometry( '{}x{}'.format( WIDTH, HEIGHT) )
		# self.resizable( 0, 0 ) # this prevents from resizing the window

		self.menu = TopMenu(self)
		self.frame = None
		self.switch_frame(LoginFrame(self))

	def switch_frame(self, new_frame: Frame):
		# Destroys current frame and replaces it with a new one.
		if self.frame is not None:
			self.frame.destroy()

		self.frame = new_frame
		self.update()

"""
The first frame shown.
This frame has fields to enter a user name and password
	and a button to login.
"""
class LoginFrame(Frame):
	def __init__(self, input_master: Tk):

		self.master = input_master
		super().__init__(input_master)

		self.label_username = Label(self, text="Username:")
		self.label_password = Label(self, text="Password:")

		self.entry_username = Entry(self)
		self.entry_password = Entry(self, show="*")

		self.label_username.grid(row=0, sticky=E)
		self.label_password.grid(row=1, sticky=E)
		self.entry_username.grid(row=0, column=1)
		self.entry_password.grid(row=1, column=1)

		self.login_button = Button(self, text="Login", command=self._login_clicked)
		self.login_button.grid(columnspan=2)

		self.pack( anchor = "nw", fill = BOTH, expand = YES )
		self.master.bind('<Return>', self.return_key_pressed)

	def return_key_pressed( self, event ):
		self._login_clicked()

	def encrypt(self, password):
		password = binascii.a2b_qp(password)
		en = hashlib.pbkdf2_hmac('sha1', password, b'kYt20AgK9e3MdRGivNqT', 100000)
		return en

	def _login_clicked(self):
		username = self.entry_username.get()
		password = self.entry_password.get()

		password = self.encrypt(password)
		if (compare.compare(username, password)):
			messagebox.showinfo("Login info", "logged in ")
			global LOGGED_IN
			LOGGED_IN = True
			self.master.unbind('<Return>')
			self.master.switch_frame(ChoiceFrame(self.master))
		else:
			messagebox.showinfo("Login info", "failed.")

"""
Displayed after the user logs in.
Two buttons; to enter data manually, or to import from a file
"""
class ChoiceFrame(Frame):
	def __init__(self, input_master: Tk):

		self.master = input_master
		super().__init__(input_master)

		self.enter_button = Button(self, text="Enter Data", command=self._enter_clicked)
		self.import_button = Button(self, text="Import File", command=self._import_clicked)

		self.enter_button.grid( row = 0, sticky = E )
		self.import_button.grid( row = 0, column = 1 )

		self.pack( anchor = "nw" , fill = BOTH, expand = YES)

	def _enter_clicked(self):
		self.master.switch_frame(EnterDataFrame(self.master))

	def _import_clicked(self):
		file_path = filedialog.askopenfilename()

		if file_path:  # if a file was selected
			try:
				# Open file and load workbook
				workbook = openpyxl.load_workbook(file_path, read_only=True)

			except openpyxl.utils.exceptions.InvalidFileException:
				messagebox.showerror("File error", "Unable to open file as XLSX file")
				return

			## pass workbook to loading frame
			self.master.switch_frame(LoadingFrame(self.master, "Loading File.", subprocess_workbook, [workbook]))

"""
This frame is where the user can enter in data
It has two fields for data and two button;
	to enter more data, or to process what is already entered
"""
class EnterDataFrame(Frame):
	def __init__(self, input_master: Tk):

		self.master = input_master
		super().__init__(input_master)

		self.default_label_1 = Label(self, text="Type in the values into each box and")
		self.default_label_2 = Label(self, text="then click Next Data Point or Continue.")

		self.time_entry = Entry(self)
		self.value_entry = Entry(self)

		self.next_button = Button(self, text="Next Data Point", command=self._next_clicked)
		self.continue_button = Button(self, text="Continue", command=self._continue_clicked)

		self.default_label_1.grid(row=0, sticky=W, columnspan=2)
		self.default_label_2.grid(row=1, sticky=W, columnspan=2)
		self.time_entry.grid(row=2, sticky=E)
		self.value_entry.grid(row=2, column=1)
		self.next_button.grid(row=3, sticky=E)
		self.continue_button.grid(row=3, column=1)

		self.data = {}

		self.pack( anchor = "nw", fill = BOTH, expand = YES )

	def _next_clicked(self):
		time_text = self.time_entry.get()
		value_text = self.value_entry.get()

		if time_text or value_text:  # if the entries are not empty
			try:
				time_ = float(time_text)
				value_ = float(value_text)
			except ValueError:
				messagebox.showinfo("Input Error", "Invalid entry")
				return

			# append data to data collected
			self.data.update({time_: value_})

			# clear entrys
			self.time_entry.delete(0, END)
			self.value_entry.delete(0, END)

	def _continue_clicked(self):
		time_text = self.time_entry.get()
		value_text = self.value_entry.get()

		if time_text or value_text:  # if the entries are not empty
			try:
				time_ = float(time_text)
				value_ = float(value_text)
			except ValueError:
				messagebox.showinfo("Input Error", "Invalid entry")
				return

			# append data to data collected
			self.data.update({time_: value_})

		# continue only if data is not empty
		if self.data == {}:
			return

		keys = list( self.data.keys() )
		keys.sort()

		# organize time and value into two ordered lists
		data_array = [keys, [self.data[index] for index in keys]]

		## pass data to AI algorithm
		self.master.switch_frame(LoadingFrame(self.master, "Classifying Data", subprocess_AI, [data_array]))

class FolderFrame(Frame):
	def __init__(self, input_master: Tk):

		self.master = input_master
		super().__init__(input_master)

		self.text = Label( self, text = \
			"Only files containing \"CRACK_X.Xmm\" will be considered\n" +
			"where X.X is the crack size of that file.")
		self.import_button = Button( self, text = "Import Folder", command = self._import_clicked )

		self.text.grid(row=0)
		self.import_button.grid(row=1)

		self.pack( anchor = "nw", fill = BOTH, expand = YES )

	def _import_clicked(self):
		folder = filedialog.askdirectory()

		if folder:  # if a folder was selected
			self.master.switch_frame( LoadingFrame( self.master, "Loading Files.", subprocess_folder, [ folder ] ) )

"""
This function passes a workbook to process_workbook and receives a 2D list
It then merges threads back to the UI
"""
def subprocess_workbook( input_workbook: openpyxl.Workbook, caller: Frame ):
	data_array = AI_Manager.process_workbook( input_workbook )

	# waits until the loading frame that called this is completely loaded
	while not caller.master.frame == caller:
		pass

	caller.master.switch_frame( LoadingFrame( caller.master, "Classifying Data", subprocess_AI, [ data_array ] ) )

"""
This function loads and runs the AI, passing the results to the next frame
"""
def subprocess_AI( data_array, caller: Frame ):
	def get_result( data_set ):
		manager.set_features( data_set, time_start, time_end )
		AI_data.append( manager.GetAllResults() )

	time_start = min( data_array[ 0 ] )
	time_end = max( data_array[ 0 ] )
	AI_data = []

	#load AIs
	manager = AI_Manager.AI_Manager()

	#get data
	ai_threads = [ threading.Thread( target = get_result, args = ( data, ) ) for data in data_array[ 1: ] ]

	for ai_thread in ai_threads:
		ai_thread.start()

	for ai_thread in ai_threads:
		ai_thread.join()

	for ai in manager.is_not_loaded():
		messagebox.showinfo( "AI Error", "{} is not loaded\nIt will not be displayed".format( ai.title() ) )

	# waits until the loading frame that called this is completely loaded
	while not caller.master.frame == caller:
		pass

	if manager.is_loaded():		# if any AIs are loaded to give an answer
		caller.master.switch_frame( ResultFrame( caller.master, AI_data ) )
	else:
		messagebox.showinfo( "AI Error", "No data to be displayed" )
		caller.master.switch_frame( ChoiceFrame( caller.master ) )

"""
This function returns the data from each file in the given folder 
"""
def subprocess_folder( input_folder, caller: Frame ):
	files = [ '/'.join( [ input_folder, file ] ) for file in os.listdir( input_folder ) ]
	data_array, results_array = AI_Manager.read_files( files )

	# waits until the loading frame that called this is completely loaded
	while not caller.master.frame == caller:
		pass

	if data_array and results_array:
		caller.master.switch_frame( LoadingFrame( caller.master, "Classifying Data", subprocess_AI_with_expected, [ data_array, results_array ] ) )
	else:
		messagebox.showinfo( "AI Error", "No data to be displayed" )
		caller.master.switch_frame( ChoiceFrame( caller.master ) )

"""
This function returns a set of results to be analyzed based on the data and results arrays
"""
def subprocess_AI_with_expected( data_array, results_array, caller: Frame ):
	manager = AI_Manager.AI_Manager()
	confusion_matrix_set = manager.Test_AIs( data_array, results_array )

	# waits until the loading frame that called this is completely loaded
	while not caller.master.frame == caller:
		pass

	if manager.is_loaded():
		caller.master.switch_frame( AnalysisFrame( caller.master, confusion_matrix_set ) )
	else:
		messagebox.showinfo( "AI Error", "No data to be displayed" )
		caller.master.switch_frame( ChoiceFrame( caller.master ) )

"""
This special frame only displays a given string while
	an important process is working in the background.
"""
class LoadingFrame(Frame):
	def __init__(self, input_master: Tk, loading_text: str, todo_function, todo_arguments):
		self.master = input_master

		workbook_thread = threading.Thread(target=todo_function, args=todo_arguments + [ self ])
		workbook_thread.start()

		super().__init__(self.master)

		self.default_label = Label(self, text=loading_text)
		self.default_label.pack(anchor="nw")

		self.pack( anchor = "nw", fill = BOTH, expand = YES )

"""
A prototype frame. In this frame a scroll bar is implemented
"""
class ScrollingFrame( Frame ):
	def __init__( self, input_master: Tk ):
		self.master = input_master
		super().__init__( input_master )

		self.canvas = Canvas( self )
		self.inner_frame = Frame( self.canvas )
		self.Y_scrollbar = Scrollbar( self, orient = "vertical", command = self.canvas.yview )
		self.X_scrollbar = Scrollbar( self, orient = "horizontal", command = self.canvas.xview )

		self.canvas.configure( yscrollcommand = self.Y_scrollbar.set, xscrollcommand = self.X_scrollbar.set )
		self.Y_scrollbar.pack( side= "right", fill= "y", anchor = 'e' )
		self.X_scrollbar.pack( side= "bottom", fill= "x", anchor = 's' )
		self.canvas.pack( side="left", anchor = 'nw', fill = 'both', expand = True )

		self.canvas.create_window( ( 0, 0 ), window = self.inner_frame, anchor = 'nw' )
		self.inner_frame.bind( "<Configure>", lambda event:\
			self.canvas.configure( scrollregion = self.canvas.bbox( "all" ) ) )

		#windows
		self.master.bind("<MouseWheel>", self._on_mousewheel)
		#linux
		self.master.bind("<Button-4>", self._on_mousewheel)
		self.master.bind("<Button-5>", self._on_mousewheel)

	def _on_mousewheel( self, event ):
	# respond to Linux or Windows wheel event
		if event.num == 5 or event.delta == -120:
			self.canvas.yview_scroll( 1, "units" )
		elif event.num == 4 or event.delta == 120:
			self.canvas.yview_scroll( -1, "units" )

"""
This is were the result is displayed after the AI has calculated it.
	>>>It has not been implemented yet<<<
"""
class ResultFrame( ScrollingFrame ):
	def __init__( self, input_master: Tk, AI_data ):
		super().__init__( input_master )

		self.info_frames = []

		ai_threads = [threading.Thread(target = lambda:
			self.info_frames.append(self.AnswerFrame(self.inner_frame, data)))
				for data in AI_data ]

		for ai_thread in ai_threads:
			ai_thread.start()

		for ai_thread in ai_threads:
			ai_thread.join()

		self.info_frames = [self.AnswerFrame(self.inner_frame, data) for data in AI_data]

		for row_index, sub_frame in enumerate( self.info_frames ):
			sub_frame.grid( row = row_index )

		self.pack( anchor = "nw", fill = BOTH, expand = YES )

	class AnswerFrame(Frame):
		def __init__( self, input_master: Frame, ai_data ):
			self.master = input_master
			super().__init__( input_master )

			self.name_labels = [ Label( self, text = name + ":" ) for name in sorted( ai_data ) ]
			self.result_labels = [ Label( self, text = ai_data[ name ] ) for name in sorted( ai_data ) ]

			for row_index, ( name_label, result_label ) in enumerate( zip( self.name_labels, self.result_labels ) ):
				name_label.grid( row = row_index, column = 0 )
				result_label.grid( row = row_index, column = 1 )

"""
This frame displays the confusion matrices in the same way that the AI_Manager would.
"""
class AnalysisFrame( ScrollingFrame ):
	def __init__( self, input_master: Tk, AI_data ):
		super().__init__( input_master )

		self.confusion_matrix_frames = {}

		ai_threads = [ threading.Thread( target = lambda: \
			self.confusion_matrix_frames.update( { name : self.confusion_matrix( self.inner_frame, name, data ) } ) ) \
				for name, data in AI_data.items() ]

		for ai_thread in ai_threads:
			ai_thread.start()

		for ai_thread in ai_threads:
			ai_thread.join()

		for row_index, ai_name in enumerate( sorted( self.confusion_matrix_frames ) ):
			self.confusion_matrix_frames[ ai_name ].grid( row = row_index )

		self.pack( anchor = "nw", fill = BOTH, expand = YES )

	class confusion_matrix( Frame ):
		def __init__( self, input_master: Frame, ai_name: str, ai_data ):
			self.master = input_master
			super().__init__( input_master )

			# extract a set of keys
			classified_values = sorted( set( [ item for sublist in [ list( ai_data[ key ].keys() ) for key in ai_data ] for item in sublist ] ) )

			# keys each as a string
			classified_value_strings = [ ", ".join( str( item ) for item in sublist ) for sublist in classified_values ]

			matrix_height = len( ai_data ) + 1
			matrix_width = len( classified_value_strings ) + 1

			self.name_label = Label( self, text = ai_name)
			self.name_label.grid( row = 0, column = 0, columnspan = max( matrix_width, 1 ) )

			self.header1_label = Label( self, text = "Actual Label" )
			self.header1_label.grid( row = 1, column = 0 )

			self.header2_label = Label( self, text = "Classified Label" )
			self.header2_label.grid( row = 1, column = 1, columnspan = max( matrix_width - 1, 1 ), sticky = E )

			self.classified_labels = [ Label( self, text = classified_value_text ) for classified_value_text in classified_value_strings ]

			for column_index, label in enumerate( self.classified_labels ):
				label.grid( row = 2, column = 1 + column_index )

			self.expected_labels = [ Label( self, text = expected_result) for expected_result in sorted( ai_data ) ]
			self.result_labels = [ [] for _ in ai_data ]

			for row_index, expected_label in enumerate( self.expected_labels ):
				expected_label.grid( row = 3 + row_index, column = 0, sticky = E  )

			for row_index, expected_result in enumerate( sorted( ai_data ) ):

				given_sum = sum( ai_data[ expected_result ].values() )

				if not given_sum:
					given_sum = 1

				self.result_labels[ row_index ] = [ Label( self, text = "{:.3g}".format(
					ai_data[expected_result][given_result] / given_sum
						if given_result in ai_data[ expected_result ].keys() else 0 ) )
							for given_result in classified_values ]

				for column_index, result_label in enumerate( self.result_labels[ row_index ] ):
					result_label.grid( row = 3 + row_index, column = 1 + column_index )

			#self.vertical_separators = [ ttk.Separator( self, orient = VERTICAL ) for _ in classified_value_strings ]
			#self.horizontal_separators = [ ttk.Separator( self, orient = HORIZONTAL ) for _ in ai_data ]

			#for column_index, separator in enumerate( self.vertical_separators ):
			#	separator.grid( column = 1 + column_index, row = 2, columnspan = matrix_height, sticky = 'ns' )

			#for row_index, separator in enumerate( self.horizontal_separators ):
			#	separator.grid( column = 0, row = 1 + row_index, rowspan = matrix_width, sticky = 'ew' )
			"""
			print( "DEBUG: {}, {}".format( matrix_height, matrix_width ) )

			confusion_matrix = ai_data
			classified_lables = classified_values
			classified_lable_strings = classified_value_strings

			expected_values = sorted( confusion_matrix )

			# maximum lengths for table setup
			max_left_string = max(max(len(str(value)) for value in expected_values), 11)
			max_string = max(len(lable) for lable in classified_lable_strings)
			separator = (max_string + 3) * len(classified_lables)

			printing_string = "\n{:" + str(max_left_string + 1) + "}\n{}{:>" + str(separator - 1) + "}\n{:" + str(
				max_left_string) + "}{}"
			printing_lables_string = " | {:" + str(max_string) + "}"

			# print top lables
			print(printing_string.format( ai_name.title(), "Actual Label", "Classified Label", "", "".join(
				[printing_lables_string.format(lable) for lable in classified_lable_strings])))

			printing_string = "{}\n{:" + str(max_left_string) + "}{}"
			printing_results_string = " | {:." + str(max_string - 2) + "f}"
			separator += max_left_string

			for expected_result in expected_values:
				given_sum = sum(confusion_matrix[expected_result].values())

				if not given_sum:
					given_sum = 1

				# a set of each result
				result_set = [
					confusion_matrix[expected_result][given_result] / given_sum if given_result in confusion_matrix[
						expected_result].keys() else 0 for given_result in classified_lables]

				print(printing_string.format('-' * separator, expected_result, "".join(
					printing_results_string.format(printed_result) for printed_result in result_set)))
			"""


class Old_ResultFrame(Frame):
	def __init__( self, input_master: Tk, input_data: List[ float ] ):

		self.master = input_master
		super().__init__( input_master )

		self.canvas = Canvas( self )
		self.scrollbar = Scrollbar( self, orient = "vertical", command = self.canvas.yview )
		self.inner_frame = Frame( self.canvas )

		self.canvas.configure( yscrollcommand = self.scrollbar.set )
		self.scrollbar.pack( side="right", fill="y", anchor = 'e' )
		self.canvas.pack( side="left", anchor = 'nw', fill = 'both', expand = True )

		self.canvas.create_window( ( 0, 0 ), window = self.inner_frame, anchor = 'nw' )
		self.inner_frame.bind( "<Configure>", lambda event:\
			self.canvas.configure( scrollregion = self.canvas.bbox( "all" ) ) )

		#windows
		self.master.bind("<MouseWheel>", self._on_mousewheel)
		#linux
		self.master.bind("<Button-4>", self._on_mousewheel)
		self.master.bind("<Button-5>", self._on_mousewheel)

		for column_index, column in enumerate( input_data ):
			for row_index, value in enumerate( column ):
				default_label = Label( self.inner_frame, text = value )
				default_label.grid( row = row_index, column = column_index )

		# self.default_label_1.grid( row = 0, sticky = E )

		self.pack( anchor = "nw", fill = BOTH, expand = YES )

	def _on_mousewheel( self, event ):
	# respond to Linux or Windows wheel event
		if event.num == 5 or event.delta == -120:
			self.canvas.yview_scroll( 1, "units" )
		elif event.num == 4 or event.delta == 120:
			self.canvas.yview_scroll( -1, "units" )

class AboutFrame( ScrollingFrame ):
	paragraph = \
"""This program uses AI algorithms to assume crack sizes in a gear.
It is the 2019 senior project of Nathan Bradley, James Hund, T.J. Moore.
			
Copyright (c) 2019
Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE."""

	def __init__( self, input_master: Tk ):
		super().__init__( input_master )

		self.text = Label( self.inner_frame, text = self.paragraph )
		self.text.pack( anchor = "nw" )

		self.pack( anchor = "nw", fill = BOTH, expand = YES )
"""
A drop down menu that is always at the top
Used to reset, logout, or exit.
"""
class TopMenu(Menu):
	def __init__(self, input_master: Tk):

		self.master = input_master
		super().__init__(input_master)

		self.master.configure(menu=self)

		self.file_menu = Menu(self.master, tearoff=0)
		self.add_cascade(menu=self.file_menu, label="File")
		self.file_menu.add_command(label="Log out", command=self._Log_out_selected)
		self.file_menu.add_command(label="Reset", command=self._Reset_selected)
		self.file_menu.add_command(label="Exit", command=self._Exit_selected)

		self.other_menu = Menu(self.master, tearoff=0)
		self.add_cascade(menu=self.other_menu, label="Other")
		self.other_menu.add_command(label="Confusion Matrix Analysis", command=self._CMA_selected)
		self.other_menu.add_command(label="About", command=self._About_selected)

	def _Log_out_selected(self):
		global LOGGED_IN

		if LOGGED_IN:
			LOGGED_IN = False
			self.master.switch_frame(LoginFrame(self.master))

	def _Reset_selected(self):
		global LOGGED_IN

		if LOGGED_IN:
			self.master.switch_frame(ChoiceFrame(self.master))
		else:
			self.master.switch_frame(LoginFrame(self.master))

	def _Exit_selected(self):
		# log out for consistancy
		global LOGGED_IN
		LOGGED_IN = False

		self.master.destroy()
		self.master = None
		# this exits the program

	def _CMA_selected(self):
		global LOGGED_IN

		if LOGGED_IN:
			self.master.switch_frame( FolderFrame( self.master ) )
		else:
			messagebox.showinfo( "Error", "Login first" )

	def _About_selected(self):
		self.master.switch_frame( AboutFrame( self.master ) )


if __name__ == "__main__":
	app = Application()
	app.mainloop()
