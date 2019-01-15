#!/bin/bash

################################################################################
# This script will install the needed files for running the project.
# It will also run the project afterwards.
################################################################################

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
