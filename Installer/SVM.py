import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn import utils
from matplotlib import style
style.use("ggplot")
from sklearn import svm
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
clf = SVC(kernel = 'linear')

file = "Training_Data4.csv"
counter = 1
colnames = ['Crack']
while(counter <= 4990):
    y = 'var' + str(counter)
    colnames.append(y)
    counter = counter + 1

#print (colnames)
data = pd.read_csv(file, names=colnames)
X = data.drop('Crack', axis=1)
y = data['Crack']
#X = X.as_matrix().astype(np.float)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.50)
#Polynomial Kernel

svclassifier = SVC(kernel='poly', degree=4)
svclassifier.fit(X_train, y_train)
y_pred = svclassifier.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

'''
#Gaussian Kernel
svclassifier = SVC(kernel='rbf')
svclassifier.fit(X_train, y_train)

#print(y)
#print(X_train)
#print(X_test)
y_pred = svclassifier.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

'''
