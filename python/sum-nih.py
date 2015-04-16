import csv
import sys

f = open(sys.argv[1], 'rt')
w = open(sys.argv[2], 'wt')

reader = csv.DictReader(f)

list_all_orgs = []
list_org_names = []
list_summed_orgs = []

for row in reader:
	list_all_orgs.append(row)

for i, v in enumerate(list_all_orgs):
	list_org_names.append(v['ORG_NAME'])

set_org_names = set(list_org_names)

for i, v in enumerate(set_org_names):
	my_dict = {'ORG_NAME':v, "PROJECT_COUNT":0}
	list_summed_orgs.append(my_dict)

for i, v in enumerate(list_summed_orgs):
	for y, x in enumerate(list_all_orgs):
		if x['ORG_NAME'] == v['ORG_NAME']:
			print "We got a match"
			v['PROJECT_COUNT'] += 1

fieldnames = ('ORG_NAME', 'PROJECT_COUNT')

writer = csv.DictWriter(w, fieldnames=fieldnames)

headers = dict( (n,n) for n in fieldnames )

writer.writerow(headers)

for y, x in enumerate(list_summed_orgs):
	writer.writerow({ 'ORG_NAME':x['ORG_NAME'], 'PROJECT_COUNT':x['PROJECT_COUNT']})

print "finished"