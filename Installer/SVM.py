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
clf = SVC(kernel = 'linear')


X = [[0, 0], [1, 1]]
y = [0, 1]
clf = svm.SVC(gamma='scale')
clf.fit(X, y)
print(clf.predict([[2., 2.]]))
'''
x = pd.read_csv("Training_Data.csv")
a = np.array(x)
y = a[0,1,2,3]

x = np.column_stack((x.var1, x.var2, x.var3, x.var4))
x.shape
#lab_enc = preprocessing.LabelEncoder()
#encoded = lab_enc.fit_transform(x)
clf.fit(x, y)
#clf.predict([[696.898718298454, 471.135059864695]])
print (y)
'''
'''
X = np.array([[1,2],
             [5,8],
             [1.5,1.8],
             [8,8],
             [1,0.6],
             [9,11]])

y = [0,1,0,1,0,1]
#y = np.array(y)
clf = svm.SVC(kernel='linear', C = 1.0)
X = X.reshape(len(X), -1)
clf.fit(X,y)
print(clf.predict([0.58,0.76]))
'''
