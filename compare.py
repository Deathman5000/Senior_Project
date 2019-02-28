#! /usr/bin/env python
import binascii
def compare(username, password):
  f = open('users', "r")#find the user information
  u = f.readline().rstrip()
  p = f.readline().rstrip()
  f.close
  if(username==u):#compair user name
    return binascii.hexlify(password).decode("utf-8") == p#compair password
  else:
    return False
  
