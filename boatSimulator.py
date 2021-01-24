
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

		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		
		df= pd.read_csv("coordinates.csv",delimiter=",", index_col=0)
		#log the position 


		

		R = 6378.1 #Radius of the Earth
		brng = math.radians(myboat.state.heading) #Bearing is 90 degrees converted to radians.
		d = myboat.state.boatSpeed #Distance in km

		#lat2  52.20444 - the lat result I'm hoping for
		#lon2  0.36056 - the long result I'm hoping for.

		lat1 = math.radians(myboat.state.lat) #Current lat point converted to radians
		lon1 = math.radians(myboat.state.lon) #Current long point converted to radians

		lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
		     math.cos(lat1)*math.sin(d/R)*math.cos(brng))

		lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
		             math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

		lat2 = math.degrees(lat2)
		lon2 = math.degrees(lon2)

		print(lat2)
		print(lon2)


		myboat.state.lat=lat2
		myboat.state.lon=lon2

		dfLatest=pd.DataFrame([[current_time,myboat.state.lat, myboat.state.lon]], columns=["timestamp","latitude","longitude"])
		dfLatest=dfLatest.set_index("timestamp")
		df=df.append(dfLatest)
















		time.sleep(dt)

		print("Logging")
		df.to_csv("coordinates.csv", encoding='utf-8', index=True)

