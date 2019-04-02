from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import pandas as pd
from matplotlib import style
style.use("ggplot")
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
clf = RandomForestClassifier(n_estimators=10,max_depth=None, min_samples_split=2,random_state=0)

file = "Training_Data4.csv"
counter = 1
colnames = ['Crack']
while(counter <= 4990):
    y = 'var' + str(counter)
    colnames.append(y)
    counter = counter + 1

data = pd.read_csv(file, names=colnames)
X = data.drop('Crack', axis=1)
y = data['Crack']
clf = clf.fit(X,y)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.80)

dtclassifier = tree.ExtraTreeClassifier()
dtclassifier.fit(X_train, y_train)

y_pred = dtclassifier.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
scores = cross_val_score(clf, X, y, cv=5)
print(scores.mean())