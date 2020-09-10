# import statements
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import requests
import math

def main():

	# ask for city
	address = raw_input('Would you like find resataurants near you (Y) or in a specific city (N): ')
	if address == 'Y' or address == 'y':
		city = raw_input('Enter an address to find nearby restaurants: ')
	else:
		city = raw_input('Enter a city to find restaurants in: ')

	# find latitutde and longitude
	locator = Nominatim(user_agent="FindLocalRestaurants")
	location = locator.geocode(city)
	lat = location.latitude
	lon = location.longitude

	# find distance, address, name
	print('Searching for restaurants near ' + location.address + "...")
	restaurants = []
	baseurl = 'https://developers.zomato.com/api/v2.1/geocode?lat=%f&lon=%f' %(lat,lon)
	header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": "609d0c2ed70925b2b7d2d7f963c41a82"}
	response = requests.get(baseurl, headers = header)
	results = response.json()
	places = {}
	
	for x in range(len(results['nearby_restaurants'])):
		places[results['nearby_restaurants'][x]['restaurant']['name']] = results['nearby_restaurants'][x]['restaurant']
	
	# ask the distance they would like to travel
	if(len(results['nearby_restaurants']) > 5):
		print('There are ' + str(len(results['nearby_restaurants'])) + ' options.')
		simplify = raw_input('Would you like to narrow them down (Y/N): ')
	
	# find locations, print options
	if(simplify == 'y' or simplify == 'Y'):
		exhausted = False
		cuisine = ""
		dist = 0.0
		rating = 0.0
		
		while(not exhausted):
			case = raw_input("You can choose...\n	0) Cuisine\n	1) Location\n	2) Rating\nWhat would you like to specify (0, 1, 2): ")
			
			if(int(case) < 0 or int(case) > 2):
				print "Invalid selection, please try again."
				continue
			elif(int(case) == 0 and cuisine == ""):
				options = []
				for x in range(len(places)):
					type_cui = places.values()[x]["cuisines"].split(",")
					for y in range(len(type_cui)):
						if(type_cui[y] not in options):
							options.append(type_cui[y])
				
				print("There are " + str(len(options)) + " types of cuisines to choose from.")
				selected = False
				while(not selected):
					print(options)
					input = raw_input("What cuisine have you chosen?: ")
				  	if(input not in options):
						print("Invalid selection, please try again.")
					else:
						cuisine = str(input)
						selected = True

				# remove non-selected cuisine
                                for place in places.keys():
                                        if(cuisine not in places.get(place)["cuisines"].split(",")):
                                                del places[place]
			elif(int(case) == 1 and dist == 0.0):
				# ask distance willing to travel
        			dist = raw_input('F.Y.I Most are less than 1 km away.\nHow far are you willing to travel (in kilometers): ')
				for place in places.keys():
					R = 6373.0
					lat1 = math.radians(lat)
					lon1 = math.radians(lon)
					lat2 = math.radians(float(places.get(place)["location"]["latitude"]))
					lon2 = math.radians(float(places.get(place)["location"]["longitude"]))
					dlon = lon2 - lon1
					dlat = lat2 - lat1
					a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
					c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
					d = R * c
					if(float(d) > float(dist)):
						del places[place]
			elif(int(case) == 2 and rating == 0.0):
				rating = float(raw_input("On a scale from 1 to 5, AT LEAST what rating should the restaurant have: "))
				if(rating < 1):
					rating = 1.0
				elif(rating > 5):
					rating = 5.0

				# remove ratings below selected input
				for place in places.keys():
                                        if(float(places.get(place)["user_rating"]["aggregate_rating"]) < rating):
						del places[place]
			else:
				# You have already chosen this option
				print "You have already chosen this option previously, please try again."
				continue

			if(len(places.keys()) == 0):
				print "Oh no! There are no places left."
				return
			if(rating != 0.0 and dist != 0.0 and cuisine != ""):
				exhausted = True
			else:
				print("There are now " + str(len(places.keys())) + " restaurants to choose from.")
				go = raw_input("Would you like to keep narrowing down (Y/N): ")
				if go == "N" or go == "n":
					exhausted = True
	
	print("----------------------------------------------------")
	print("Hope you found the perfect nearby restaurant. Enjoy!")
	print("----------------------------------------------------")

	# print options
	for place in places.keys():
		print("Name: " + place)
		print("Address: " + places.get(place)["location"]["address"])
		print("Cuisine(s): " + places.get(place)["cuisines"]) 
		print("Rating: " + str(places.get(place)["user_rating"]["aggregate_rating"]))
		print("Menu: " + places.get(place)["menu_url"])
		print("----------------------------------------------")

if __name__ == '__main__':
	main()
