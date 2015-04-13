import csv
import sys

reader = csv.reader(open(sys.argv[1], 'rU'), delimiter=',')
writer = csv.writer(open(sys.argv[2], 'w'), delimiter=',')
x = int(sys.argv[3])

entries = set()

for row in reader:
	if row[x] not in entries:
		writer.writerow(row)
		entries.add(row[x])
	elif row[x] == "":
		writer.writerow(row)

print "Finished"
