
import numpy as np 
import matplotlib.pyplot as plt 
import math 
from weatherCheck import *   
from utils import *


#The main class for boat object
class boat:
	# constant parameters
	LOA=60 # imoca 60


	def __init__(self,state):
		self.state=state

	class state:
		
		def __init__(self, lat=55, lon=34):
			self.lat=lat
			self.lon=lon
			self.boatSpeed=12
			self.heading=150
			self.TWS=13
			self.TWA=13

		def showState(self):
			print("Initial Boat State")
			print('latitude: {} \t'.format(self.lat),'longitude: {} \t'.format(self.lon),'boat speed: {} \t'.format(self.boatSpeed),'heading: {} \t'.format(self.heading),'TWS: {} \t'.format(self.TWS),'TWA: {} \t'.format(self.TWA))

	def showState(self):
		self.state.showState()

	# Polar Diagram of the Boat	
	def polarDiagram(self):
		# setting the axes 
		# projection as polar 
		plt.axes(projection = 'polar') 
		# setting the length of  
		# axis of cardioid 
		a=4
		  
		# creating an array 
		# containing the radian values 
		rads = np.arange(0, (2 * np.pi), 0.01) 
		   
		# plotting the cardioid 
		for rad in rads: 
		    r = +a + (a*-np.cos(rad))  
		    plt.polar(rad,r,'g.')  
		  
		# display the polar plot 
		plt.show(block=False)
		plt.title("polar diagram of the boat(test)")
		plt.pause(5)
		plt.close()


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





