from sklearn.ensemble import RandomForestClassifier
from matplotlib import style
style.use("ggplot")
from sklearn import svm
from sklearn.svm import SVC
import sys
import os.path
import pickle
from typing import List
from sklearn.model_selection import train_test_split
from sklearn import preprocessing	
# import warnings filter
from warnings import simplefilter
# ignore all future warnings
simplefilter(action='ignore', category=FutureWarning)

class Support_Vector_Machine:

    __SAVED_AI_FILE__ = "Support_Vector_Machine.data"

    def __init__(self, new_file_path=None, Load=True):

        self.file = None

        if new_file_path:
            self.file = new_file_path
        elif self.__SAVED_AI_FILE__:
            self.file = self.__SAVED_AI_FILE__

        self.SVM = None

        if Load and self.file and os.path.isfile(self.file):
            self.load_SVM(self.file)

    def is_loaded(self):
        return True if self.SVM else False

    def train(self, input_list, input_result):
        """ CAUTION this function WILL destroy the existing Supprot Vector Mechine Data"""
        """This code coverts that data and makes a Supprot Vector Mechine then saves the Data"""
        # encode results to 0, 1, 2, 3 to work with sklearn
        lab_enc = preprocessing.LabelEncoder()
        encoded = lab_enc.fit_transform(input_result)
        # make vectors
        X_train, X_test, y_train, y_test = train_test_split(input_list, encoded, test_size = 0.01, train_size = 0.99, shuffle=False)
        self.SVM = SVC(kernel ='linear')
        self.SVM.fit(X_train, y_train)
        # save vectors
        self.save_SVM(self.file)

    def classify(self, input_list: List[float]):
        """this code will test the data given against the tree"""
        # check if SVM Data is loaded
        if not self.SVM:
            print("Fatal Error: No Tree Loaded")
            sys.exit(1)

        # convert input into 2d numpy array and predict result
        return_value = self.SVM.predict([input_list])

        # undo the encode earlier
        return_value = tuple(return_value*1.5)


        # return result
        if isinstance(return_value, dict):
            return tuple(return_value.keys())  # [ 0 ]
        if hasattr(return_value, '__getitem__'):
            return tuple(return_value)
        else:
            return return_value

    def load_SVM(self, input_file):
        """load model"""
        self.SVM = pickle.load(open(input_file, 'rb'))

    def save_SVM(self, input_file):
        """save model for later"""
        pickle.dump(self.SVM, open(input_file, 'wb'))
