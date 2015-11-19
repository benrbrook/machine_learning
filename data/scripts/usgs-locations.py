import csv
import sys
import os

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# Load in station locations
stations = {}
station_list = open(sys.argv[2], 'r')
for station in station_list:
	station = station.split('\t')
	id = station[0]
	lat = station[1]
	lon = station[2]
	if id in stations:
		continue
	else:
		stations[id] = (lat, lon)

f = open(sys.argv[1], 'r')
for line in f:
	if line[0] == '#':
		continue
	line = line.split('\t')
	file_name = line[2].replace(' ', '-').replace(':', '-')
	id = line[1]
	data = line[4]
	if not is_number(data):
		continue
	split_f = open("location-value/usgs/" + file_name, 'a')
	if id in stations:
		latlon = stations[id]
	else:
		continue
	csv_line = latlon[0] + "," + latlon[1] + "," + data + "\n"
	split_f.write(csv_line)