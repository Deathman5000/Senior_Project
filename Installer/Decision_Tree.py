import sys
import os.path
import pickle
from typing import List
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn import tree as dTree


class Decision_Tree:

    __SAVED_AI_FILE__ = "decision_tree.data"

    def __init__(self, new_file_path=None, Load=True):

        self.file = None

        if new_file_path:
            self.file = new_file_path
        elif self.__SAVED_AI_FILE__:
            self.file = self.__SAVED_AI_FILE__

        self.tree = None

        if Load and self.file and os.path.isfile(self.file):
            self.load_tree(self.file)

    def is_loaded(self):
        return True if self.tree else False

    def train(self, input_list, input_result):
        """ CAUTION this function WILL destroy the existing tree """
        """This code coverts that data and makes a tree then saves the tree"""
        # encode results to 0, 1, 2, 3 to work with sklearn
        lab_enc = preprocessing.LabelEncoder() 
        encoded = lab_enc.fit_transform(input_result)
        # make tree
        X_train, X_test, y_train, y_test = train_test_split(input_list, encoded, test_size = 0.01, train_size = 0.99)
        self.tree = dTree.DecisionTreeClassifier()
        self.tree.fit(X_train, y_train)
        # save tree
        self.save_tree(self.file)

    def classify(self, input_list: List[float]):
        """this code will test the data given against the tree"""
        # check if tree is loaded
        if not self.tree:
            print("Fatal Error: No Tree Loaded")
            sys.exit(1)

        # convert input into 2d numpy array and predict result
        return_value = self.tree.predict([input_list])

        # undo the encode earlier
        return_value = tuple(return_value*1.5)


        # return result
        if isinstance(return_value, dict):
            return tuple(return_value.keys())  # [ 0 ]
        if hasattr(return_value, '__getitem__'):
            return tuple(return_value)
        else:
            return return_value

    def load_tree(self, input_file):
        """load model"""
        self.tree = pickle.load(open(input_file, 'rb'))

    def save_tree(self, input_file):
        """save model for later"""
        pickle.dump(self.tree, open(input_file, 'wb'))
