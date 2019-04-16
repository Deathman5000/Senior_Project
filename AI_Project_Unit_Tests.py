# AI_Project_Unit_Tests.py

import unittest
import sys
from unittest import TestCase
import AI_Manager

from math import sqrt
from statistics import median
from scipy import fftpack
from scipy import signal

# Stat_Features sample data
data_set = [
696.8987182985,
471.1350598647,
324.054671594,
227.3596287053,
162.8743598915,
119.0172373712,
88.2980104025,
65.9385616958,
48.9297979596,
35.3218339926,
23.8612602652,
13.7750123874,
4.5675360336,
-4.0660776852,
-12.3194050616,
-20.3109362611,
-28.1080348301,
-35.7466911449,
-43.2445664624,
-43.2445664624,
-918.0927253654,
-603.8019188541,
-403.9345119291,
-276.9929769909,
-196.7915469687,
-146.4100514973,
-115.103477139,
-95.9043688976,
-84.3831135399,
-77.7238281059,
-74.0826582225,
-72.3001896803,
-71.642478235,
-71.6468291374,
-71.9975479675,
-72.4954960352,
-73.0283564505,
-73.5261703518,
-73.9379638073,
-73.9379638073,
-379.5969524832,
-266.6337665525,
-193.8157746761,
-146.5443261248,
-115.6529939904,
-95.1454830897,
-81.2594703983,
-71.5814256426,
-64.5280069567,
-59.1024276608,
-54.6923367551,
-50.8978648814,
-47.4512228877,
-44.1878748671,
-41.0178818281,
-37.8862538845,
-34.7550485943,
-31.6033181794,
-28.4163639159,
-28.4163639159,
854.5084041241,
525.0924501367,
314.1456803127,
178.9895393744,
92.435738477,
37.052354996,
1.630494746,
-20.9521921253,
-35.3348596582,
-44.4316441753,
-50.106614209,
-53.5795451432,
-55.6187368412,
-56.6961786132,
-57.1205521382,
-57.0840880217,
-56.7280214307,
-56.126694454,
-55.3234504655,
-55.3234504655,
156.9135427158,
78.5538497047,
28.5809081132,
-3.295738291,
-23.5029282433,
-36.1846065899,
-44.0257035087,
-48.7115579424,
-51.3127582339,
-52.5586400426,
-52.8972176089,
-52.6014567944,
-51.8568837232,
-50.7816516961,
-49.4636231137,
-47.9515884621,
-46.2746073532,
-44.4549146406,
-42.5081669594,
-42.5081669594 ]

time_values = (0.02, 0.0201371704001396)

function_list = [
"Max",
"Min",
"Mean",
"Peak_to_Peak",
"Harmonic_Mean",
"Trimmed_Mean",
"Variance",
"Standard_Deviation",
"Mean_Absolute_Deviation",
"Median_Absolute_Deviation",
"Crest_Factor",
"Peak2RMS",
"Skewness",
"Kurtosis",
"Shape_Factor",
"Root_Mean_Square",
"Mean_Frequency",
"Frequency_Center",
"Root_Mean_Square_Frequency",
"Figure_of_Merit" ]

"""
Old version of Stat_Features
Only used to test the validity of Stat_Features
"""
def Stat_Features_uncondensed( input_list, time_start, time_end ):
	Length   = len( input_list )


	frequency_length = ( 1 + Length ) // 2

	sampling_frequency = Length / ( time_end - time_start )
	Y = fftpack.fft( input_list )
	P2 = [ abs( value / Length ) for value in Y ]
	P1 = P2[ : frequency_length ]

	for index in range( 1, len( P1 ) - 1 ):
		P1[ index ] *= 2

	frequencies_list = [ sampling_frequency * value / Length for value in range( frequency_length ) ]

	ft = frequencies_list


	input_list = sorted( input_list )

	# If a data point is within OUTLIER_CRITERIA * IQR of the median
	# then it is not an outlier
	OUTLIER_CRITERIA = 1.5 # lower excludes more

	# F0
	Maximum_Value = max( input_list )

	# F1
	Minimum_Value = min( input_list )

	# F2
	def mean( input_list_ ):
		return sum( input_list_ ) / len( input_list_ )

	Mean = mean( input_list )

	# F3
		# F0 - F1
	Peak_to_Peak = Maximum_Value - Minimum_Value

	# F4
	Harmonic_Mean = 1 / mean( [ 1 / value for value in input_list ] )

	# F5
	# Mean excluding outliers (10% trimmed mean)
	Length   = len( input_list )
	Median = median( input_list )
	q1  = median( input_list[ :Length // 2 ] )
	q3  = median( input_list[ Length // 2 + 1: ] )
	iqr = q3 - q1

	Trimmed_Mean = mean( [ value for value in input_list \
		if not abs( value - Median ) > OUTLIER_CRITERIA * iqr ] )

	# F6
	Variance = mean( [ ( value - Mean )**2 for value in input_list ] )

	# F7
	Standard_Deviation = sqrt( Variance )

	# F8
	Mean_Absolute_Deviation = mean( [ abs( value - Mean ) for value in input_list ] )

	# F9
	Median_Absolute_Deviation = mean( [ abs( value - Median ) for value in input_list ] )


	# F15
	Root_Mean_Square = sqrt( mean( [ value * value for value in input_list ] ) )


	# F10
	Crest_Factor = max( input_list ) / Root_Mean_Square

	# F11
	Peak2RMS = max( abs( value ) for value in input_list ) / Root_Mean_Square

	# F12
	Skewness = sum( [ ( value - Mean )**3 for value in input_list ] ) \
		     / sum( [ ( value - Mean )**2 for value in input_list ] )

	# F13
	Kurtosis = mean( [ ( value - Mean )**4 for value in input_list ] ) \
		       / ( Variance**2 )

	# F14
	Shape_Factor = Root_Mean_Square / mean( [ abs( value ) for value in input_list ] )



	# F17
	Mean_Frequency = mean( P1 )

	# F18
	Frequency_Center = sum( [ f * p for f, p in zip( ft, P1 ) ] ) / sum( P1 )

	# F19
	Root_Mean_Square_Frequency = sqrt( sum( [ f * f * p for f, p in zip( ft, P1 ) ] ) / sum( P1 ) )

	# F20
	Figure_of_Merit = ( max( input_list ) - mean( input_list ) )\
					  / sum( [ P1[ index ] for index in signal.find_peaks( P1 )[ 0 ] ] )

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

class Test_Stat_Features( TestCase ):
	#SFec
	# These handle edge cases and still return a list
	def test_Stat_Features_edge_cases( self ):
		self.assertEqual( AI_Manager.AI_Manager.__Statistical_Features__( [ 1, 1, 1, 1, 1 ], 1, 2 ),
			[ 1.0, 0.0, 1.0, 0, 0.3333333333333333, 1, 0, 0.0, 0.0, 1.0, 1.0, 0, 1.0, 1.0, 1.0, 0.0, 1, 0.0, 0.0, float( 'inf' ) ] )
		self.assertEqual( AI_Manager.AI_Manager.__Statistical_Features__( [-2, -1, 0, 1, 2], 1, 2 ),
			[ 1.414213562373095, 1.3069827590673755, 1.414213562373095, 0.0, 0.742344242941071, -2, 1.7, 1.2360679774997896, 1.2, 0.0, 1.1785113019775793, 4, -0.5, 1.4142135623730951, 0, 2.0, 2, 1.2, 1.4142135623730951, 1.1755705045849463 ] )
		self.assertEqual( AI_Manager.AI_Manager.__Statistical_Features__( [ 0, 0, 0, 0, 0 ], 1, 2 ),
			[ 0, float( 'inf' ), 0, 0, 0.0, 0, 0, float( 'inf' ), 0.0, 0.0, 0, 0, 0.0, 0.0, 0, 0.0, 0, 0.0, 0.0, float( 'inf' ) ] )

	#SFdz
	# These handle error cases and give a default return list
	def test_Stat_Features_defaults_to_zero( self ):
		self.assertEqual( AI_Manager.AI_Manager.__Statistical_Features__( [               ], 1, 2 ), [ 0 ] * 20 )
		self.assertEqual( AI_Manager.AI_Manager.__Statistical_Features__( [ 1, 2, 3, 4, 5 ], 1, 1 ), [ 0 ] * 20 )

	#SFse
	# This is a test of equality
	def test_Stat_Features_sample_equality( self ):
		self.assertEqual( AI_Manager.AI_Manager.__Statistical_Features__( data_set, *time_values ),
			[ 4.217859220861402, 161718.15876906496, 4.531711857483196, 105.49371009257484, 33.06237446295676, -918.0927253654, 11.369530753041849, 125187.81450014132, 98.28811051347202, -25.533411949161984, 1.7385158991395402, 1772.6011294895002, -36.65873373114751, 202.5929172547362, -119.05115994984546, 40391.93499601878, 854.5084041241, 104.119126400414, 200.97744897380596, 1.1181565898434476 ] )



if __name__ == '__main__':
	unittest.main()
