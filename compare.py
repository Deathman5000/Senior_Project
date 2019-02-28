#! /usr/bin/env python
import binascii
#imports for database access
"""
import sqlite3
import os
"""

"""
This code is to checks the username and password
author: Timothy Moore
Version: 02/07/2019
"""
def compare(username, password):
  f = open('users', "r")#find the user information
  u = f.readline().rstrip()
  p = f.readline().rstrip()
  f.close
  if(username==u):#compair user name
    return binascii.hexlify(password).decode("utf-8") == p#compair password
  else:
    return False

#code to access the database and check username/password
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
"""

