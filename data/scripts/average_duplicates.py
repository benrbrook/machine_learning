import csv
import random
import math
import operator
import sys
import geocoder
from time import sleep
import sys
import numpy as np

f = open(sys.argv[2], 'w')

locations = {}

with open(sys.argv[1], 'rt') as csvfile:
	lines = csv.reader(csvfile)
	dataset = list(lines)
	for x in range(1, len(dataset) - 1):
		# Grab address and value
		latlng = (dataset[x][0], dataset[x][1])
		value = dataset[x][2]
		if latlng not in locations:
			locations[latlng] = [int(value)]
		else:
			locations[latlng].append(int(value))

for key in locations:
	locations[key] = int(np.mean(locations[key]))
	f.write(key[0] + "," + key[1] + "," + str(locations[key]) + "\n");