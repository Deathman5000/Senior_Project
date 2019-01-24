﻿##[Ps1 To Exe]
##
##Kd3HDZOFADWE8uK1
##Nc3NCtDXThU=
##Kd3HFJGZHWLWoLaVvnQnhQ==
##LM/RF4eFHHGZ7/K1
##K8rLFtDXTiW5
##OsHQCZGeTiiZ4tI=
##OcrLFtDXTiW5
##LM/BD5WYTiiZ4tI=
##McvWDJ+OTiiZ4tI=
##OMvOC56PFnzN8u+Vs1Q=
##M9jHFoeYB2Hc8u+Vs1Q=
##PdrWFpmIG2HcofKIo2QX
##OMfRFJyLFzWE8uK1
##KsfMAp/KUzWJ0g==
##OsfOAYaPHGbQvbyVvnQX
##LNzNAIWJGmPcoKHc7Do3uAuO
##LNzNAIWJGnvYv7eVvnQX
##M9zLA5mED3nfu77Q7TV64AuzAgg=
##NcDWAYKED3nfu77Q7TV64AuzAgg=
##OMvRB4KDHmHQvbyVvnQX
##P8HPFJGEFzWE8tI=
##KNzDAJWHD2fS8u+Vgw==
##P8HSHYKDCX3N8u+Vgw==
##LNzLEpGeC3fMu77Ro2k3hQ==
##L97HB5mLAnfMu77Ro2k3hQ==
##P8HPCZWEGmaZ7/K1
##L8/UAdDXTlaDjofG5iZk2WHvT204UuGeqr2zy5GA2O/AixrQR4kASFh72CzkASs=
##Kc/BRM3KXxU=
##
##
##fd6a9f26a06ea3bc99616d4851b372ba
################################################################################
# This script will install the needed files for running the project.
# It will also run the project afterwards.
################################################################################
#if (!([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) { Start-Process powershell.exe "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs; exit }
# install python
$Location = gci C:\ -recurse -include AI_Project.py -erroraction SilentlyContinue | select -Expand Directory -First 1 | select -Expand FullName
#Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
choco install python3 pip -y
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
#Set-Location "C:\Users\James\Documents\CS4391\Senior_Project\AI"
#Start-Process 'C:\Users\James\Documents\CS4391\Senior_Project\AI\python-3.7.2.exe' -NoNewWindow -Wait
#$name = "$env:UserName"
#$PythonPath = "C:\Users\$name\AppData\Local\Programs\Python\Python37-32"
#[System.Environment]::SetEnvironmentVariable("PATH", $Env:Path + ";$PythonPath")
#$PythonPath = gci C:\ -recurse -include python.exe -erroraction SilentlyContinue | select -Expand Directory -First 1 | select -Expand FullName
# [System.Environment]::SetEnvironmentVariable("PATH", $Env:Path + ";$PythonPath", "user")
#python-3.7.2.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
# install pip.
#python get-pip.py
#$PipPath = "C:\Users\$name\AppData\Local\Programs\Python\Python37-32\Scripts"
#[System.Environment]::SetEnvironmentVariable("PATH", $Env:Path + ";$PipPath")
# install openpyxl
pip install openpyxl

# install numpy
pip install numpy

# install the python plotter
python -m pip install -U matplotlib

# run the program
Set-Location "$Location"
python AI_Project.py
