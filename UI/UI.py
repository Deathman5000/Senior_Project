#!/usr/bin/python

import tkinter
#from tkinter import LEFT, RIGHT
from tkinter import FLAT

WIDTH = 350
HEIGHT = 460
TITLE_COLOR = "grey70"

def nothing():
	True

main_window = tkinter.Tk()

# Code to add widgets will go here...
main_window.title( "Test UI for AI" )
main_window.geometry( '{}x{}'.format( WIDTH, HEIGHT) )
main_window.resizable( 0, 0 ) # this prevents from resizing the window

main_window.grid_rowconfigure(1, weight=1)
main_window.grid_columnconfigure(0, weight=1)

#frame = tkinter.Frame( main_window, pady = 3, background = "grey" )
#tkinter.Label( frame, text = "Test Label", bg = "grey", font = ( "Courier", 20 )  ).pack( side = LEFT )
#frame.grid(row=0, sticky="ew")


top_button = tkinter.Button( main_window, text = "Test Label Button", background = TITLE_COLOR, font = ( "Courier", 20 ), anchor="w", relief=FLAT, takefocus = False, bd = 0, command = nothing )
top_button.grid( row = 0, sticky="ew" )
#top_button.pack( side = LEFT )
#tkinter.Button( main_window, text = "test button 2", command = nothing ).pack()

main_window.mainloop()
