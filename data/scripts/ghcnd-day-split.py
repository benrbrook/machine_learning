import csv
import sys
import os

# Split up large csv into serperate ones for each day
directory = sys.argv[1][:-4] + "/"
if not os.path.exists(directory):
	os.makedirs(directory)
with open(sys.argv[1], 'r') as csvfile:

	reader = csv.reader(csvfile)
	for i, row in enumerate(reader):
		print(i)
		file_name = row[1]
		f = open(directory + file_name, 'a')
		wr = csv.writer(f)
		wr.writerow(row)