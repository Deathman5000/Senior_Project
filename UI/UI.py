#!/usr/bin/python

import tkinter

WIDTH = 312
HEIGHT = 324

def nothing():
	True

main_window = tkinter.Tk()
# Code to add widgets will go here...
main_window.title( "Test UI for AI" )
main_window.geometry("312x324") # size of the window width:- 500, height:- 375
main_window.resizable(0, 0) # this prevents from resizing the window
#main_window.width( 1000 )
#main_window.height( 600 )

frame = tkinter.Frame( main_window, width = WIDTH, height = 50, bd = 0, bg = "grey" )
frame.pack()

tkinter.Label( frame, text = "Test Label" ).place()
tkinter.Button( frame, text = "test button 1", command = nothing ).place()
tkinter.Button( main_window, text = "test button 2", command = nothing ).pack()

main_window.mainloop()
