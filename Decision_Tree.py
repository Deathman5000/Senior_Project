
import sys
import os.path
import pickle
from typing import List

class Decision_Tree:

	__SAVED_AI_FILE__ = "decision_tree.data"

	def __init__( self, new_file_path = None, Load = True ):

		self.file = None

		if new_file_path:
			self.file = new_file_path
		elif self.__SAVED_AI_FILE__:
			self.file = self.__SAVED_AI_FILE__

		self.tree = None

		if Load and self.file and os.path.isfile( self.file ):
			self.load_tree( self.file )

	def is_loaded( self ):
		return True if self.tree else False

	@staticmethod
	def class_counts( rows ):
		"""Counts the number of each type of example in a dataset."""
		counts = {}  # a dictionary of label -> count.
		for row in rows:
			# in our dataset format, the label is always the last column
			label = row[-1]
			if label not in counts:
				counts[label] = 0
			counts[label] += 1
		return counts

	class Leaf:
		"""A Leaf node classifies data.
		This holds a dictionary of class (e.g., "Apple") -> number of times
		it appears in the rows from the training data that reach this leaf.
		"""

		def __init__(self, rows, rebuild=False):
			if rebuild:
				self.predictions = rows
			else:
				self.predictions = Decision_Tree.class_counts(rows)

	class Decision_Node:
		"""A Decision Node asks a question.
		This holds a reference to the question, and to the two child nodes.
		"""

		def __init__(self,
					 question,
					 true_branch,
					 false_branch):
			self.question = question
			self.true_branch = true_branch
			self.false_branch = false_branch

	class Question:
		"""A Question is used to partition a dataset.
		This class just records a 'column number' (e.g., 0 for Color) and a
		'column value' (e.g., Green). The 'match' method is used to compare
		the feature value in an example to the feature value stored in the
		question. See the demo below.
		"""

		def __init__(self, column, value):
			self.column = column
			self.value = value

		def match(self, example):
			# Compare the feature value in an example to the
			# feature value in this question.
			val = example[self.column]
			if self.is_numeric(val):
				return val <= self.value
			else:
				return val == self.value

		def is_numeric( self, value):
			"""Test if a value is numeric."""
			return isinstance(value, int) or isinstance(value, float)

	def partition( self, rows, question ):
		"""Partitions a dataset.
		For each row in the dataset, check if it matches the question. If
		so, add it to 'true rows', otherwise, add it to 'false rows'.
		"""
		true_rows, false_rows = [], []
		for row in rows:
			if question.match(row):
				true_rows.append(row)
			else:
				false_rows.append(row)
		return true_rows, false_rows

	def gini( self, rows ):
		"""Calculate the Gini Impurity for a list of rows.
		There are a few different ways to do this, I thought this one was
		the most concise. See:
		https://en.wikipedia.org/wiki/Decision_tree_learning#Gini_impurity
		"""
		counts = self.class_counts(rows)
		impurity = 1
		for lbl in counts:
			prob_of_lbl = counts[lbl] / float(len(rows))
			impurity -= prob_of_lbl ** 2
		return impurity

	def info_gain( self, left, right, current_uncertainty ):
		"""Information Gain.
		The uncertainty of the starting node, minus the weighted impurity of
		two child nodes.
		"""
		p = float(len(left)) / (len(left) + len(right))
		return current_uncertainty - p * self.gini(left) - (1 - p) * self.gini(right)

	def find_best_split( self, rows ):
		"""Find the best question to ask by iterating over every feature / value
		and calculating the information gain."""
		best_gain = 0  # keep track of the best information gain
		best_question = None  # keep train of the feature / value that produced it
		current_uncertainty = self.gini(rows)
		n_features = len(rows[0]) - 1  # number of columns

		for col in range(n_features):  # for each feature

			values = set([row[col] for row in rows])  # unique values in the column

			for val in values:  # for each value

				question = self.Question(col, val)

				# try splitting the dataset
				true_rows, false_rows = self.partition(rows, question)

				# Skip this split if it doesn't divide the
				# dataset.
				if len(true_rows) == 0 or len(false_rows) == 0:
					continue

				# Calculate the information gain from this split
				gain = self.info_gain(true_rows, false_rows, current_uncertainty)

				# You actually can use '>' instead of '>=' here
				# but I wanted the tree to look a certain way for our
				# toy dataset.
				if gain >= best_gain:
					best_gain, best_question = gain, question

		return best_gain, best_question

	def build_tree( self, rows ):
		"""Builds the tree.
		Rules of recursion: 1) Believe that it works. 2) Start by checking
		for the base case (no further information gain). 3) Prepare for
		giant stack traces.
		"""

		# Try partitioing the dataset on each of the unique attribute,
		# calculate the information gain,
		# and return the question that produces the highest gain.
		gain, question = self.find_best_split(rows)

		# Base case: no further info gain
		# Since we can ask no further questions,
		# we'll return a leaf.
		if gain == 0:
			return self.Leaf(rows)

		# If we reach here, we have found a useful feature / value
		# to partition on.
		true_rows, false_rows = self.partition(rows, question)

		# Recursively build the true branch.
		true_branch = self.build_tree(true_rows)

		# Recursively build the false branch.
		false_branch = self.build_tree(false_rows)

		# Return a Question node.
		# This records the best feature / value to ask at this point,
		# as well as the branches to follow
		# dependingo on the answer.
		return self.Decision_Node(question, true_branch, false_branch)


	def train( self, input_list: List[ List[ float ] ], input_result: List[ float ] ):
		""" CAUTION this function WILL destroy the existing tree """
		self.tree = self.build_tree( [ data + [ result ] for data, result in zip( input_list, input_result ) ] )
		self.save_tree( self.file )

	def classify( self, input_list: List[ float ] ):
		if not self.tree:
			print( "Fatal Error: No Tree Loaded" )
			sys.exit( 1 )

		return_value = self._classify( input_list, self.tree )

		if isinstance( return_value, dict ):
			return tuple( return_value.keys() )#[ 0 ]
		if hasattr( return_value, '__getitem__' ):
			return tuple( return_value )
		else:
			return return_value

	def _classify( self, row, node ):
		"""See the 'rules of recursion' above."""

		# Base case: we've reached a leaf
		if isinstance(node, self.Leaf):
			return node.predictions

		# Decide whether to follow the true-branch or the false-branch.
		# Compare the feature / value stored in the node,
		# to the example we're considering.
		if node.question.match(row):
			return self._classify(row, node.true_branch)
		else:
			return self._classify(row, node.false_branch)

	def rebuild_tree( self, input_blueprint ):

		if len( input_blueprint ) == 1:
			return self.Leaf( input_blueprint[ 0 ], rebuild = True )
		elif len( input_blueprint ) == 3:
		#					[question, true_set, false_set]
		# [question, [question, [leaf], ...], [question, ..., [leaf]]]
			return self.Decision_Node( input_blueprint[ 0 ],
				self.rebuild_tree( input_blueprint[ 1 ] ),
				self.rebuild_tree( input_blueprint[ 2 ] ) )
		else:
			print( "Error in reconstructing tree" )
			sys.exit( 1 )

	def deconstruct_tree( self, input_tree ):
		if isinstance( input_tree, self.Leaf ):
			return [ input_tree.predictions ]

		return [ input_tree.question,
			self.deconstruct_tree( input_tree.true_branch ),
			self.deconstruct_tree( input_tree.false_branch ) ]

	def load_tree( self, input_file ):
		with open( input_file, 'rb' ) as tree_file:
			tree_blueprint =  pickle.load( tree_file )

		self.tree = self.rebuild_tree( tree_blueprint )

	def save_tree( self, input_file ):
		tree_list = self.deconstruct_tree( self.tree )

		with open( input_file, 'wb' ) as tree_file:
			pickle.dump( tree_list, tree_file )