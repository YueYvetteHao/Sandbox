#!/usr/bin/python

# Check copy number

import sys


Copynumber = {}
filename = sys.argv[1]
file = open(filename, 'r')
for line in file:
	line = line.rstrip("\n")
	array = line.split("\t")
	if array[1][0:4] not in Copynumber:
		Copynumber[array[1][0:4]] = 1
	else:
		Copynumber[array[1][0:4]] += 1		
file.close()
cn = 0
for spp in Copynumber:
#	if (Copynumber[spp] == 1) or (Copynumber[spp] > 2):
	if Copynumber[spp] > cn:
		cn = Copynumber[spp]
if cn > 0:
	print (filename, cn)

