import numpy
import math

# Unit converter for wind and boat speed
def meterpersecond2knot(ms):
	return 1.94384449*ms




def calcNextPosition(bearing,distance,currentLat,currentLong):
	## source: https://stackoverflow.com/questions/7222382/get-lat-long-given-current-point-distance-and-bearing
	currentLat = math.radians(currentLat) #Current lat point converted to radians
	currentLong = math.radians(currentLong) #Current long point converted to radians

	R = 6378.1 #Radius of the Earth
	brng = bearing #Bearing is 90 degrees converted to radians.
	d = distance #Distance i

	lat1=currentLat
	lon1=currentLong

	lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
		     math.cos(lat1)*math.sin(d/R)*math.cos(brng))

	lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
	             math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

	lat2 = math.degrees(lat2)
	lon2 = math.degrees(lon2)
	print("next position is calculated")
	return lat2,lon2


