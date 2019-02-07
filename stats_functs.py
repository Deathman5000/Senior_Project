#! /usr/bin/env python

# prototype statistical functions

from math import sqrt
from statistics import median

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

data_set = sorted([
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
-42.5081669594 ])


# If a datapoint is within OUTLIER_CRITERIA * IQR of the median
# then it is not an outlier
OUTLIER_CRITERIA = 1.5; # lower excludes more

# F0
# Maximum value
# max x(n)

# F1
# Minimum value
# min x(n)

# F2
def Mean( input_list ):
	return sum( input_list ) / len( input_list )

# F3
# F0 - F1
def Peak_to_peak( input_list ):
	return max( input_list ) - min( input_list )

# F4
def Harmonic_mean( input_list ):
	return 1 / Mean( [ 1 / value for value in input_list ] )

# F5
# Mean excluding outliers
def Trimmed_mean( input_list ):
	l   = len( data_set )
	mid = median( data_set )
	q1  = median( data_set[ :l // 2 ] )
	q3  = median( data_set[ l // 2 + 1: ] )
	iqr = q3 - q1
	return Mean( [ val for val in input_list if not abs( val - mid ) > OUTLIER_CRITERIA * iqr ] )

# F6
def Variance( input_list ):
	ave = Mean( input_list )
	return Mean( [ (value - ave)**2 for value in input_list ] )

# F7
def Standard_deviation( input_list ):
	return sqrt( Variance( input_list ) )

# F8
def Mean_absolute_deviation( input_list ):
	ave = Mean( input_list )
	return Mean( [ abs( value - ave ) for value in input_list ] )

# F9
def Median_absolute_deviation( input_list ):
	mid = median( input_list )
	return Mean( [ abs( value - mid ) for value in input_list ] )

# F10
def Crest_Factor( input_list ):
	return max( input_list ) / RMS( input_list )

# F11
def Peak2RMS( input_list ):
	return max( abs( value ) for value in input_list ) / RMS( input_list )

# F12
def Skewness( input_list ):
	ave = Mean( input_list )
	return sum( [ (value - ave)**3 for value in input_list ] ) \
         / sum( [ (value - ave)**2 for value in input_list ] )

# F13
def Kurtosis( input_list ):
	ave = Mean( input_list )
	return Mean( [ (value - ave)**4 for value in input_list ] ) \
           / ( Variance( input_list )**2 )

# F14
def Shape_Factor( input_list ):
	return RMS( input_list ) / Mean( [ abs( value ) for value in input_list ] )

# F15
def RMS( input_list ):
	return sqrt( Mean( [ value * value for value in input_list ] ) )

# F16
def Mean_Frequency( input_list ):
	pass

# F17
def Frequency_Center( input_list ):
	pass

# F18
def RMS_Frequency( input_list ):
	pass

# F19
# (FM0)
def Figure_of_merit( input_list ):
	pass
	#return Peak_to_peak( input_list ) / sum( input_list )

function_list = [
max,
min,
Mean,
Peak_to_peak,
Harmonic_mean,
Trimmed_mean,
Variance,
Standard_deviation,
Mean_absolute_deviation,
Median_absolute_deviation,
Crest_Factor,
Peak2RMS,
Skewness,
Kurtosis,
Shape_Factor,
RMS,
Mean_Frequency,
Frequency_Center,
RMS_Frequency,
Figure_of_merit ]

max_string = max( len( funct.__name__ ) for funct in function_list )

for count, funct in enumerate( function_list ):
	output = "F{:<2} {:" + str( max_string ) + "}\t {}"
	print( output.format( count, funct.__name__, funct( data_set ) ) )
