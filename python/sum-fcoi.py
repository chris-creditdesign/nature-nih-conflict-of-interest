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
	list_org_names.append(v['SUBMITTING INSTITUTION'])

set_org_names = set(list_org_names)

for i, v in enumerate(set_org_names):
	my_dict = {'SUBMITTING INSTITUTION':v, "FCOI_COUNT":0}
	list_summed_orgs.append(my_dict)

for i, v in enumerate(list_summed_orgs):
	for y, x in enumerate(list_all_orgs):
		if x['SUBMITTING INSTITUTION'] == v['SUBMITTING INSTITUTION']:
			print x['SUBMITTING INSTITUTION']
			v['FCOI_COUNT'] += 1

fieldnames = ('SUBMITTING INSTITUTION', 'FCOI_COUNT')

writer = csv.DictWriter(w, fieldnames=fieldnames)

headers = dict( (n,n) for n in fieldnames )

writer.writerow(headers)

for y, x in enumerate(list_summed_orgs):
	writer.writerow({ 'SUBMITTING INSTITUTION':x['SUBMITTING INSTITUTION'], 'FCOI_COUNT':x['FCOI_COUNT']})

print "finished"