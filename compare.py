#! /usr/bin/env python
import binascii
import sqlite3
import os

"""
This code is to check if the username and password are in the database
author: Timothy Moore
Version: 02/07/2019
"""
def compare(username, password):
  connection = sqlite3.connect(os.path.join(os.getcwd(), 'DataBase', 'Users.db'))
  cursor = connection.cursor() #The past 2 lines connect to database
  cursor.execute("SELECT password FROM user WHERE user.id = \"" +username+ "\";") #gets password from username
  p = str(cursor.fetchone())
  if("('"+password+"',)" == p):#compares password entered to the users password
    return True
  else:
    return False

