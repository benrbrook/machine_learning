import csv
import random
import math
import operator
import sys
import geocoder
from time import sleep
import sys
from urllib.request import urlopen
import json
from unidecode import unidecode

f = open(sys.argv[2], 'w')
key_f = open('key.txt', 'r')
key = key_f.readline()

with open(sys.argv[1], encoding = "ISO-8859-1") as csvfile:
	lines = csv.reader(csvfile)
	dataset = list(lines)
	for x in range(1, len(dataset) - 1):
		# Grab address and price
		house = [dataset[x][11], dataset[x][5]]
		address = house[0].split(',', 1)[0]
		address = address.split(' ')
		for i, s in enumerate(address):
			address[i] = unidecode(s)
		formatted_address = "+".join(address) + ",New+Haven,CT&key="
		url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + formatted_address + key
		print(url)
		response = urlopen(url)
		str_response = response.read().decode('utf-8')
		obj = json.loads(str_response)
		if obj['status'] != "OK":
			continue
		lat = obj['results'][0]['geometry']['location']['lat']
		lng = obj['results'][0]['geometry']['location']['lng']

		# Format price
		price = house[1].replace("$", "").replace(" ", "").replace(",", "")[:-3]
		print(price)
		if int(price) == 0:
			continue
		house_info = str(lat) + "," + str(lng) + "," + price + "\n"

		print(house_info)
		f.write(house_info)