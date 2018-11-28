#!/usr/bin/python
import openpyxl

sample=openpyxl.load_workbook('crack.xlsx') 

sheet = sample.active

a1 = sheet['A1']
a2 = sheet['A2']
a3 = sheet.cell(row=3, column=1)

print(a1.value)
print(a2.value) 
print(a3.value)
