
import numpy as np 
import matplotlib.pyplot as plt 
import math 
  


# A visualization of the boat's polar diagram
def polarDiagram():
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
	    r = +a + (a*np.cos(-rad))  
	    plt.polar(rad,r,'g.')  
	  
	# display the polar plot 
	plt.show(block=False)
	plt.pause(5)
	plt.close()


def boatSpeed():

	speed=10

	return speed

#The main class for boat object
class boat:
	# parameters
	LOA=60 # imoca 60


	def __init__(self,state):
		self.state=state

	class state:
		lat=50
		lon=55


		def __init__(self, lat=55, lon=34):
			self.lat=lat
			self.lon=lon
			self.boatSpeed=12
			self.heading=150

		def showState(self):
			print("Initial Boat State")
			print('lat: {} \t'.format(self.lat),'long: {} \t'.format(self.lon),"boat speed:",str(self.boatSpeed), "heading:",str(self.heading))

	def showState(self):
		self.state.showState()


if __name__ == "__main__":

	myboat=boat(boat.state(lat=22,lon=32))

	print("yes")
	print(myboat.state.showState())