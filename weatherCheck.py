import requests, json


def windSpeed(lat,lon):
	base_url = "http://api.openweathermap.org/data/2.5/weather?"
	api_key="fb839b2b2f7c0848153a3ed54abd99fc"
	api_name="Default"

	#lat="42.045"
	# lon="-87.688"

	complete_url = base_url + "appid=" + api_key + "&lat=" + str(lat) + "&lon=" + str(lon) 
	response = requests.get(complete_url)

	x = response.json()

	'''
	if x["cod"] != "404": 
	  
	    # store the value of "main" 
	    # key in variable y 
	    y = x["main"] 
	  
	    # store the value corresponding 
	    # to the "temp" key of y 
	    current_temperature = y["temp"] 
	  
	    # store the value corresponding 
	    # to the "pressure" key of y 
	    current_pressure = y["pressure"] 
	  
	    # store the value corresponding 
	    # to the "humidity" key of y 
	    current_humidiy = y["humidity"] 
	  
	    # store the value of "weather" 
	    # key in variable z 
	    z = x["weather"] 
	  
	    # store the value corresponding  
	    # to the "description" key at  
	    # the 0th index of z 
	    weather_description = z[0]["description"] 
	  
	    # print following values 
	    
	    print(" Temperature (in kelvin unit) = " +
	                    str(current_temperature) + 
	          "\n atmospheric pressure (in hPa unit) = " +
	                    str(current_pressure) +
	          "\n humidity (in percentage) = " +
	                    str(current_humidiy) +
	          "\n description = " +
	                    str(weather_description)) 
	    
	  
	else: 
	    print(" City Not Found ") 

	'''
	print("Success")
	return x
	