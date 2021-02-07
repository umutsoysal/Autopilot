
import numpy as np 
import matplotlib.pyplot as plt 
import math 
from weatherCheck import *   
from utils import *
from datetime import datetime
import time
import pandas as pd
from boat import *


## This starts the simulation.
if __name__ == "__main__":

	myboat=boat(boat.state(lat=22,lon=32))
	myboat.polarDiagram()

	print("test")
	print(myboat.state.showState())

	x=windSpeed(myboat.state.lat,myboat.state.lon)

	#myboat.state.TWS=x['wind']['speed']
	#print(myx)

	myboat.state.TWS=meterpersecond2knot(x['wind']['speed'])
	myboat.state.TWA=(x['wind']['deg'])

	myboat.showState()


	## TIME STEP (THS IS IMPORTANT CURRENTLY IT IS IN SECONDS)
	dt=5

	while True:

		#check the current time
		now = datetime.now()
		#format it, subject to change
		current_time = now.strftime("%H:%M:%S")
		#read the dataset
		df= pd.read_csv("coordinates.csv",delimiter=",", index_col=0)
		#log the position 


		
		bearing = math.radians(myboat.state.heading) #Bearing is 90 degrees converted to radians.
		
		# This should be detailed.
		distanceCovered = myboat.state.boatSpeed #Distance in km
		

		currentLat = myboat.state.lat #Current lat point converted to radians
		currentLong = myboat.state.lon #Current long point converted to radians


		nextLat,nextLong=calcNextPosition(bearing,distanceCovered,currentLat,currentLong)

		print(nextLat)
		print(nextLong)


		myboat.state.lat=nextLat
		myboat.state.lon=nextLong

		dfLatest=pd.DataFrame([[current_time,myboat.state.lat, myboat.state.lon]], columns=["timestamp","latitude","longitude"])
		dfLatest=dfLatest.set_index("timestamp")
		df=df.append(dfLatest)


		time.sleep(dt)

		print("Logging")
		df.to_csv("coordinates.csv", encoding='utf-8', index=True)

