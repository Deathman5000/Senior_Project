#!/usr/bin/python
import openpyxl
import os
import time

begin = time.ctime()
current = os.getcwd()
file = os.path.join(current, 'DATA', 'acceleration_data_1_CRACK_0.0mm.xlsx')
#sample=openpyxl.load_workbook('acceleration_data_1_CRACK_0mm.xlsx')
sample = openpyxl.load_workbook(file)
sheet = sample.active
m_row = sheet.max_row

alist = []
blist = []

for i in range(1,m_row + 1):
    cell = sheet.cell(row = i, column = 2)
    alist.append(cell.value)
print "********************************************************************"
for i in range(1,m_row + 1):
    cell = sheet.cell(row = i, column = 3)
    blist.append(cell.value)
#a1 = sheet('A1')
""""for i in range(1,m_row + 1):
    cell = sheet.cell(row = i, column = 2)
    print(cell.value)
print "********************************************************************"
for i in range(1,m_row + 1):
    cell = sheet.cell(row = i, column = 3)
    print(cell.value)"""
#a1 = sheet['A1']
#a2 = sheet['A2']
#a3 = sheet.cell(row=3, column=1)

#print(a1.value)
#print(a2.value)
#print(a3.value)
#print a1.value
end = time.ctime()
print(alist)
print(blist)
print(begin)
print(end)
