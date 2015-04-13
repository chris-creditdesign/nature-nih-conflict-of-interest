import csv
import sys

reader = csv.reader(open(sys.argv[1], 'rU'), delimiter=',')

count = 0

for row in reader:
	if row[8] != "":
		count += 1

print count