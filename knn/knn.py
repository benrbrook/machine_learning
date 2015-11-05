import csv
import random
import math
import operator
import sys
import geocoder
from time import sleep
from sklearn.metrics import mean_squared_error
from math import sqrt

# Load in houses and split into training and test sets
def loadDataset(filename, split, trainingSet=[], test_set=[]):
	with open(filename, 'rt') as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
		for x in range(1, len(dataset) - 1):
			# Grab address and price
			house = dataset[x]
			if random.random() < split:
				trainingSet.append(house)
			else:
				test_set.append(house)

# Calculate euclidean between two points
def euclideanDistance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((float(instance1[x]) - float(instance2[x])), 2)
	return math.sqrt(distance)


# Get euclidean distance to every other house
def getNeighbors(trainingSet, testInstance, k):
	distances = []
	length = len(testInstance) - 1
	for x in range(len(trainingSet)):
		dist = euclideanDistance(testInstance, trainingSet[x], length)
		distances.append((trainingSet[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

# Poll neighbors and arrange from lowet value to highest value
def getResponse(neighbors):
	classVotes = {}
	for x in range(len(neighbors)):
		response = neighbors[x][-1]
		if response in classVotes:
			classVotes[response] += 1
		else:
			classVotes[response] = 1
	sortedVotes = sorted(list(classVotes.items()), key=operator.itemgetter(1), reverse=True)
	return sortedVotes[0][0]

# Compare test set to the prediction within margin of error
def getAccuracy(test_set, predictions):
	rmse = sqrt(mean_squared_error(test_set, predictions));
	return rmse

trainingSet = []
test_set = []
loadDataset(sys.argv[1], 0.67, trainingSet, test_set)
predictions = []
rmse = 0
k = int(sys.argv[2])
for x in range(len(test_set)):
	neighbors = getNeighbors(trainingSet, test_set[x], k)
	result = getResponse(neighbors)
	predictions.append(result)
rmse = getAccuracy(test_set, predictions)
print("k: " + k + " rmse: " + k)






