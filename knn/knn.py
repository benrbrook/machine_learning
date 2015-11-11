import csv
from random import randint
import math
import operator
import sys
import geocoder
from time import sleep
from sklearn.metrics import mean_squared_error
from math import sqrt

# Load in houses and split into training and test sets
def load_dataset(filename, training_set=[], validation_set = [], test_set=[]):
	with open(filename, 'rt') as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
		for x in range(1, len(dataset) - 1):
			# Grab address and price
			data_point = dataset[x]
			r = randint(1, 3)
			if r == 1:
				training_set.append(data_point)
			elif r == 2:
				validation_set.append(data_point)
			else:
				test_set.append(data_point)

# Calculate euclidean between two points
def euclidean_distance(instance1, instance2, length):
	distance = 0
	for x in range(length):
		distance += pow((float(instance1[x]) - float(instance2[x])), 2)
	return math.sqrt(distance)


# Get euclidean distance to k nearest houses
def get_neighbors(training_set, test_instance, k):
	distances = []
	length = len(test_instance) - 1
	for x in range(len(training_set)):
		dist = euclidean_distance(test_instance, training_set[x], length)
		distances.append((training_set[x], dist))
	distances.sort(key=operator.itemgetter(1))
	neighbors = []
	for x in range(k):
		neighbors.append(distances[x][0])
	return neighbors

# Average k nearest neighbors
def average_neighbors(neighbors):
	sum = 0
	for data_point in neighbors:
		# Add in value
		sum += int(data_point[-1])
	return sum/len(neighbors)

# Compare test set to the prediction within margin of error
def get_rmse(validation_set, predictions):
	if len(validation_set) != len(predictions):
		print("Sets of different lengths")
		exit(1)
	rmse = sqrt(mean_squared_error(validation_set, predictions))
	return rmse

def get_accuracy(test_set, predictions, rmse):
	print(test_set)
	print(predictions)
	correct = 0
	for i in range(len(test_set)):
		if (test_set[i] - rmse) >= predictions[i] or (test_set[i] + rmse) <= predictions[i]:
			correct += 1
	return correct / len(test_set)
	

training_set = []
validation_set = []
test_set = []
load_dataset(sys.argv[1], training_set, validation_set, test_set)

# Main
rmse = []
for k in range(1, 2):
	print("K: " + str(k))
	nearest_k_neighbors = []
	neighbor_average = 0
	predictions = []
	for x in range(len(validation_set)):
		nearest_k_neighbors = get_neighbors(training_set, validation_set[x], k)
		neighbor_average = average_neighbors(nearest_k_neighbors)
		predictions.append(neighbor_average)
	rmse.append((k, get_rmse([int(x[-1]) for x in validation_set], predictions)))
optimal_model = sorted(rmse, key=operator.itemgetter(1))[0]
optimal_k = optimal_model[0]
optimal_rmse = optimal_model[1]
print("Optimal k: %d, rmse: %.3f" % (optimal_k, optimal_rmse))

final_rmse = 0
final_predictions = []
for x in range(len(test_set)):
	final_nearest_k_neighbors = get_neighbors(validation_set, test_set[x], optimal_k)
	final_neighbor_average = average_neighbors(final_nearest_k_neighbors)
	final_predictions.append(final_neighbor_average)
final_rmse = get_rmse([int(x[-1]) for x in test_set], final_predictions)
acccuracy = get_accuracy([int(x[-1]) for x in test_set], final_predictions, final_rmse)
print("Final rmse: %.3f" % final_rmse)
print("Accuracy: %.1f" % acccuracy)





