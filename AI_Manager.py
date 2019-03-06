# AI_Manager.py

import sys
import openpyxl
from typing import List
from math import sqrt
from statistics import median
from scipy import fftpack
from scipy import signal
import threading


def process_workbook( input_workbook: openpyxl.Workbook ):

	sheet = input_workbook.active

	intermediate_array = [ column for column in sheet.iter_rows( min_row = 1, max_col = sheet.max_column, max_row = sheet.max_row, values_only = True ) ]

	return_data = []

	for column in range( sheet.max_column ):
		line = [ row[ column ] for row in intermediate_array if isinstance( row[ column ], float ) ]

		if line:
			return_data.append( line )

	return return_data

class AI_Manager:

	def __init__( self ):
		self.__feature_list__ = None
		self.__restraint__ = 20
		self.__AIs__ = [] ## none thus far

	def set_restraint( self, input_value: int ):
		if 0 < input_value <= 20:
			self.__restraint__ = input_value

	def set_features( self, input_list: List[ float ], time_start: float, time_end: float ):
		self.__feature_list__ = self.__Statistical_Features__( input_list, time_start, time_end )

	def Test_AIs( self, input_list: List[ List[ List[ float ] ] ], expected_result_list: List[ List[ float ] ] ):

		Precision_Stats = {}

		for ai in self.__AIs__:
			Precision_Stats.update( { ai.__class__.__name__: { 0: { 0: 0, 1.5: 0, 3: 0, 4.5: 0 },
															1.5: { 0: 0, 1.5: 0, 3: 0, 4.5: 0 },
															3:   { 0: 0, 1.5: 0, 3: 0, 4.5: 0 },
															4.5: { 0: 0, 1.5: 0, 3: 0, 4.5: 0 } } } )

		for _2D_gear_list, _2D_expected_result in zip( input_list, expected_result_list ):
			test_time_start = min( _2D_gear_list[ 0 ] )
			test_time_end = max( _2D_gear_list[ 0 ] )

			for gear_list, expected_result in zip( _2D_gear_list[ 1 : ], _2D_expected_result ):
				test_feature_list = self.__Statistical_Features__( gear_list, test_time_start, test_time_end )[ : self.__restraint__ ]

				for ai in self.__AIs__:
					test_result = ai.AI_result_function( test_feature_list )

					Precision_Stats[ ai.__class__.__name__ ][ expected_result ][ test_result ] += 1

		return Precision_Stats

	def Train_AIs( self, input_list: List[ List[ List[ float ] ] ], expected_result_list: List[ List[ float ] ]  ):

		for _2D_gear_list, _2D_expected_result in zip( input_list, expected_result_list ):
			test_time_start = min( _2D_gear_list[ 0 ] )
			test_time_end = max( _2D_gear_list[ 0 ] )

			test_feature_list = [ self.__Statistical_Features__( gear_list, test_time_start, test_time_end )[ : self.__restraint__ ] for gear_list in _2D_gear_list[ 1 : ] ]

			ai_threads = [ threading.Thread( target = ai.AI_training_function, args = ( test_feature_list, _2D_expected_result ) ) for ai in self.__AIs__ ]

			for ai_thread in ai_threads:
				ai_thread.start()

			for ai_thread in ai_threads:
				ai_thread.join()


	def Setup_AI( self, AI_class ):
		#AI_class.__init__()
		pass

	def Get_Result( self, AI_function ):
		# determine AI to use

		# get result from AI
		return AI_function( self.__feature_list__[ : self.__restraint__ ] )

	@staticmethod
	def __Statistical_Features__( input_list: List[ float ], time_start: float, time_end: float ):

		"""
		div-zero liabilities
			Length
			1 / value for any value in input_list
			Sums[ 0 ]
			Sums[ 1 ]
			Sums[ 2 ]
			Sums[ 5 ]
			Frequency_Sums[ 0 ]
			sum( [ P1[ index ] for index in signal.find_peaks( P1 )[ 0 ] ] )
		"""

		Length = len( input_list )
		duration = time_end - time_start

		# initial error catch
		if duration == 0 or Length == 0:
			return [ 0 ] * 20

		frequency_length = ( 1 + Length ) // 2

		sampling_frequency = Length / ( time_end - time_start )
		P1 = [ abs( value / Length ) for value in fftpack.fft( input_list )[ : frequency_length ] ]

		for index in range( 1, len( P1 ) - 1 ):
			P1[ index ] *= 2

		frequencies_list = [ sampling_frequency * value / Length for value in range( frequency_length ) ]


		input_list = sorted( input_list )

		Median = median( input_list )

		# F2
		def mean( input_list_ ):
			length_ = len( input_list_ )

			if length_ == 0:
				return 0

			return sum( input_list_ ) / length_

		Mean = mean( input_list )

		Sums = [ 0 ] * 8

		Harmonic_Zero = False

		# combined sum loops									Used in:
		for value in input_list:
			temp_difference = value - Mean

			Sums[ 0 ] += value * value						# Root_Mean_Square, ( Crest_Factor, Peak2RMS, Shape_Factor )

			if value == 0:
				Harmonic_Zero = True
			else:
				Sums[ 1 ] += 1 / value						# Harmonic_Mean

			Sums[ 2 ] += abs( value )						# Shape_Factor
			Sums[ 3 ] += abs( temp_difference )				# Mean_Absolute_Deviation
			Sums[ 4 ] += abs( value - Median )				# Median_Absolute_Deviation

			temp_value = temp_difference * temp_difference

			Sums[ 5 ] += temp_value							# Variance, Skewness, ( Kurtosis, Standard_Deviation )

			temp_value *= temp_difference

			Sums[ 6 ] += temp_value							# Skewness
			Sums[ 7 ] += temp_value * temp_difference		# Kurtosis


		# F0
		Maximum_Value = input_list[ -1 ]

		# F1
		Minimum_Value = input_list[ 0 ]


		# F3
			# F0 - F1
		Peak_to_Peak = Maximum_Value - Minimum_Value

		# F4
		if Harmonic_Zero:
			Harmonic_Mean = 0
		elif Sums[ 1 ] == 0:
			Harmonic_Mean = float( 'inf' )
		else:
			Harmonic_Mean = Length / Sums[ 1 ]

		# F5
			# Mean excluding outliers (10% trimmed mean)

			# If a data point is within OUTLIER_CRITERIA * IQR of the median
			# then it is not an outlier
		OUTLIER_CRITERIA = 1.5 # lower excludes more

		first_quartile = median( input_list[ :Length // 2 ] )
		last_quartile = median( input_list[ Length // 2 + 1: ] )
		inter_quartile_range = last_quartile - first_quartile

		Trimmed_Mean = mean( [ value for value in input_list \
			if not abs( value - Median ) > OUTLIER_CRITERIA * inter_quartile_range ] )

		# F6
		Variance = Sums[ 5 ] / Length

		# F7
		Standard_Deviation = sqrt( Variance )

		# F8
		Mean_Absolute_Deviation = Sums[ 3 ] / Length

		# F9
		Median_Absolute_Deviation = Sums[ 4 ] / Length


		# F15
		Root_Mean_Square = sqrt( Sums[ 0 ] / Length )


		# F10
		if Root_Mean_Square == 0:
			Crest_Factor = float( 'inf' )
		else:
			Crest_Factor = Maximum_Value / Root_Mean_Square

		# F11
			# Peak_to_Peak_Root_Mean_Square
		if Root_Mean_Square == 0:
			Peak2RMS = float( 'inf' )
		else:
			Peak2RMS = max( abs( Minimum_Value ), abs( Maximum_Value ) ) / Root_Mean_Square

		# F12
		if Sums[ 5 ] == 0:
			Skewness = 0
		else:
			Skewness = Sums[ 6 ] / Sums[ 5 ]

		# F13
		if Sums[ 5 ] == 0:
			Kurtosis = float( 'inf' )
		else:
			Kurtosis = Sums[ 7 ] / ( Length * Variance ** 2 )

		# F14
		if Sums[ 2 ] == 0:
			Shape_Factor = float( 'inf' )
		else:
			Shape_Factor = Root_Mean_Square * Length / Sums[ 2 ]


		Frequency_Sums = [ 0 ] * 3

		for value, frequency in zip( P1, frequencies_list ):
			temp_value = value * frequency
			Frequency_Sums[ 0 ] += value
			Frequency_Sums[ 1 ] += temp_value
			Frequency_Sums[ 2 ] += temp_value * frequency

		# F17
		Mean_Frequency = Frequency_Sums[ 0 ] / frequency_length

		# F18
		if Frequency_Sums[ 0 ] == 0:
			Frequency_Center = float( 'inf' )
		else:
			Frequency_Center = Frequency_Sums[ 1 ] / Frequency_Sums[ 0 ]

		# F19
		if Frequency_Sums[ 0 ] == 0:
			Root_Mean_Square_Frequency = float( 'inf' )
		else:
			Root_Mean_Square_Frequency = sqrt( Frequency_Sums[ 2 ] / Frequency_Sums[ 0 ] )

		# F20
		peaks_sum = sum( [ P1[ index ] for index in signal.find_peaks( P1 )[ 0 ] ] )

		if peaks_sum == 0:
			Figure_of_Merit = float( 'inf' )
		else:
			Figure_of_Merit = ( Maximum_Value - Mean ) / peaks_sum


		features = [ Maximum_Value,
				Minimum_Value,
				Mean,
				Peak_to_Peak,
				Harmonic_Mean,
				Trimmed_Mean,
				Variance,
				Standard_Deviation,
				Mean_Absolute_Deviation,
				Median_Absolute_Deviation,
				Crest_Factor,
				Peak2RMS,
				Skewness,
				Kurtosis,
				Shape_Factor,
				Root_Mean_Square,
				Mean_Frequency,
				Frequency_Center,
				Root_Mean_Square_Frequency,
				Figure_of_Merit ]

		return [ features[ index ] for index in
			( 10, 18, 11, 12, 16, 1, 13, 17, 9, 2, 14, 3, 5, 15, 4, 6, 0, 8, 7, 19 ) ]

class Result_Stats:
	def __init__(self):
		self.true_positive  = 0
		self.true_negative  = 0
		self.false_positive = 0
		self.false_negative = 0

	def Accuracy( self ):
		return ( self.true_positive + self.true_negative ) \
			/ (self. true_positive + self.true_negative + self.false_positive + self.false_negative )

	def Precision( self ):
		return self.true_positive/( self.true_positive + self.false_positive )

	def Recall( self ):
		return self.true_positive/( self.true_positive + self.false_negative )

	def F1_Score( self ):
		return ( 2 * self.Recall() * self.Precision() )\
			   /( self.Recall() + self.Precision() )


def main( arguments: List ):
	prompt = input( "Menu:\n\t1)\tTraining\n\t2)\tTesting\n\tOther)\tQuit\n" )

	if prompt == '1' or prompt == '2':

		verbose = False

		if "-v" in arguments:
			arguments.remove( "-v" )
			verbose = True
		elif "-verbose" in arguments:
			arguments.remove( "-verbose" )
			verbose = True

		if not arguments:
			print( "No file given" )
			return

		data_array = []
		results_array = []

		for arg in arguments:
			if verbose: print( "Loading from", arg )

			try:
				# Open file and load workbook
				workbook = openpyxl.load_workbook( arg, read_only = True )
				workbook_data = process_workbook( workbook )

				wb_length = len( workbook_data )

				if wb_length > 1:
					expected_crack_size = 0

					try:
						expected_crack_size = float( arg.split( 'CRACK_' )[ 1 ].split( 'mm' )[ 0 ] )
					except Exception:
						pass

					data_array.append( [ workbook_data ] )
					results_array.append( [ [ expected_crack_size ] * ( wb_length - 1 ) ] )

			except openpyxl.utils.exceptions.InvalidFileException:
				if verbose: print( "Error: cannot load from", arg )

		if not data_array:
			print( "Files not usable" )
			return

		if verbose:
			print( "Loading AIs" )

		manager = AI_Manager()

		if not manager.__AIs__:
			print( "Error: No AIs loaded" )
			return

		if prompt == '1':
			if verbose: print( "Starting Training" )

			manager.Train_AIs( data_array, results_array )

			if verbose: print( "Finished" )
		else:
			if verbose: print( "Starting Testing" )

			confusion_matrix_set = manager.Test_AIs( data_array, results_array )

			# print the confusion matrix
			for ai in manager.__AIs__:
				confusion_matrix = confusion_matrix_set[ ai.__class__.__name__ ]
				cm_keys = sorted( confusion_matrix )

				print( "{}\n{}{:>27}\n{:11} | {:4} | {:4} | {:4} | {:4}"
					   .format( ai.__class__.__name__.title(), "Actual Label", "Classified Label", "", *cm_keys ) )

				for expected_result in cm_keys:
					given_sum = sum( confusion_matrix[ expected_result ].values() )

					if not given_sum:
						given_sum = 1
					print( "{}\n{:11}".format( '-' * 39, expected_result ), end = '' )

					for given_result in sorted( confusion_matrix[ expected_result ].items() ):
						print( " | {:.2f}".format( confusion_matrix[ expected_result ][given_result] / given_sum ),  end = '')

					print()
				print()


if __name__ == "__main__":
	main( sys.argv[ 1: ] )