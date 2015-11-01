import csv
import random
import math
import operator
import sys
import geocoder
from time import sleep

# Load in houses and split into training and test sets
def loadDataset(filename, split, trainingSet=[], testSet=[]):
	with open(filename, 'rt') as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
		for x in range(1, len(dataset) - 1):
			# Grab address and price
			house = dataset[x]
			if random.random() < split:
				trainingSet.append(house)
			else:
				testSet.append(house)

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
def getAccuracy(testSet, predictions):
	correct = 0
	error_margin = .4
	for x in range(len(testSet)):
		if (1 - error_margin) * int(testSet[x][-1]) <= int(predictions[x]) <= (1 + error_margin) * int(testSet[x][-1]):
			correct += 1
	return (correct/float(len(testSet))) * 100.0

trainingSet = []
testSet = []
loadDataset('locations', 0.67, trainingSet, testSet)
predictions = []
accuracy = 0
k = int(sys.argv[1])
print("Averaging 10 runs\n")
for n in range(10):
	for x in range(len(testSet)):
		neighbors = getNeighbors(trainingSet, testSet[x], k)
		result = getResponse(neighbors)
		predictions.append(result)
		# print('> predicted = ' + repr(result) + ', actual = ' + repr(testSet[x][-1]))
	accuracy += getAccuracy(testSet, predictions)
accuracy = (accuracy / 10)
print('Accuracy: ' + repr(accuracy) + '%')






