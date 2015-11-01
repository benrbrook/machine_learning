import sys
import csv
import os

# Import a dictionary of stations and lat/lng
stations = open("source-data/ghcnd-stations.txt", 'r')
station_lookup = {}
for station in stations:
	station = station[:31].split(' ')
	station = [x for x in station if x]

	station_id = station[0]
	lat = station[1]
	lng = station[2]

	station_lookup[station_id] = (lat, lng)

# Write each value out to a seperate file
# Ex. locaion-value/weather/20150101/prcp
with open(sys.argv[1]) as csvfile:
	directory = "location-value/weather/" + sys.argv[1][-8:] + "/"
	if not os.path.exists(directory):
		os.makedirs(directory)
	reader = csv.reader(csvfile)
	for row in reader:
		file_name = row[2].lower()
		f = open(directory + file_name, 'a+')
		value = row[3]
		station_id = row[0]
		latlng = station_lookup[station_id]
		f.write(latlng[0] + "," + latlng[1] + "," + value + "\n")