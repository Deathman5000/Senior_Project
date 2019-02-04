#!/bin/bash

################################################################################
# This script will install the needed files for running the project.
# It will also run the project afterwards.
################################################################################

# install python
cd \
cd c
cd Users
cd James
cd Documents
cd CS4391
cd Senior_Project
cd AI
python-3.7.2.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
# install pip.
python get-pip.py

# install openpyxl
pip install openpyxl

# install numpy
pip install numpy

# install the python plotter
python -m pip install -U matplotlib

# run the program
python test.py
cmd /k
