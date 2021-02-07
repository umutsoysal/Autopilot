
import pandas as pd
from scipy import interpolate
import numpy as np


def BoatSpeedFromPolar(windAng,windSpeed):
	
	df=pd.read_csv("PolarDiagrams/Book1.csv")
	closest_row_index = df['twa/tws'].sub(windAng).abs().idxmin()
	print(closest_row_index)
	closest_value=df.iloc[closest_row_index]['twa/tws']
	print(closest_value)

	if (windAng==closest_value):
	    secondcloserRowInd=closest_row_index
	elif (windAng>closest_value):
	    secondcloserRowInd=closest_row_index+1  
	else:
	    secondcloserRowInd=closest_row_index-1

	print(df.iloc[secondcloserRowInd]['twa/tws'])


	angles=df['twa/tws']
	angles
	df.columns[1:]
	test_list=df.columns[1:].tolist()
	for i in range(0, len(test_list)): 
	    test_list[i] = int(test_list[i]) 

	speed=9

	def closest(lst, K):       
	    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))] 

	closestColValue=closest(test_list,speed)

	closestColIndex = test_list.index(closestColValue)

	if (closestColValue==speed):
	    secondColindex=closestColIndex
	elif (closestColValue<speed):
	    secondColindex=closestColIndex+1
	else:
	    secondColindex=closestColIndex-1


	estimatedBoatSpeed=(df.iloc[closest_row_index][closestColIndex]+df.iloc[secondcloserRowInd][closestColIndex]+df.iloc[closest_row_index][secondColindex]+df.iloc[secondcloserRowInd][secondColindex])/4
	return estimatedBoatSpeed


print("test function")
BoatSpeedFromPolar(88,9)
print("test completed")



		