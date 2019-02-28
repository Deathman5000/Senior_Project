
# statistical functions

from typing import Iterable
from math import sqrt
from statistics import median
from scipy import fftpack
from scipy import signal


""" pages 5 - 7
TP = true positives
TN = true negatives
FP = false positives
FN = false negatives

Accuracy = ( TP + TN )/( TP + TN + FP + FN )
Precision = TP/( TP + FP )
Recall = TP/( TP + FN )
F1-Score = ( 2 * Recall * Precision )/( Recall + Precision )
"""


def Statistical_Features( input_list: Iterable[ float ], time_start: float, time_end: float ):

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
	durration = time_end - time_start

	# initial error catch
	if durration == 0 or Length == 0:
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


	return [ Maximum_Value,
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