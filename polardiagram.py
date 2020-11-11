import numpy as np 
import matplotlib.pyplot as plt 
import math 
  
  
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
plt.show()
sleep(5)
plt.close()