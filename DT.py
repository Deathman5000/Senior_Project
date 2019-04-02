import pandas as pd
from matplotlib import style
style.use("ggplot")
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
import pickle
clf = tree.DecisionTreeClassifier()

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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.80)

dtclassifier = tree.DecisionTreeClassifier()
dtclassifier.fit(X_train, y_train)

y_pred = dtclassifier.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

model = LogisticRegression()
model.fit(X_train, y_train)
# save the model to disk
filename = 'finalized_model.sav'
pickle.dump(dtclassifier, open(filename, 'wb'))

"""vect = CountVectorizer(analyzer='number')
vect_representation= vect.fit_transform(file)

bag_of_words = CountVectorizer(tokenizer=lambda doc: doc, lowercase=False).fit_transform(splited_labels_from_corpus)"""


#https://stackoverflow.com/questions/27673527/how-should-i-vectorize-the-following-list-of-lists-with-scikit-learn