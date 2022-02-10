#!/usr/bin/python

# Counting edges from orthogroups
# Yue Hao
# 10/2020

import sys
from parse_ortho_gene_tree import get_species
from paralogon_graph import spp_order

Filenames = []
namefile = sys.argv[1]
file = open(namefile, 'r')
for line in file:
	line = line.rstrip("\n")
	Filenames.append(line)
file.close()

global species
# species-names_order_by_tre.tab
species = get_species(str(sys.argv[2])) 




def sort_ortho_by_spp(orthogroup):
	sort_by_spp = {}
	sorted_ortho = []
	for x in orthogroup:
		sort_by_spp[spp_order(x)] = x
	for i in sorted (sort_by_spp.keys()) :  
		sorted_ortho.append(sort_by_spp[i])
	return sorted_ortho


Edge = {}


for orthofile in Filenames:
	Orthogroup = {}
	with open(orthofile, 'r') as file:
	#	print (orthofile)
		for line in file:
			line = line.rstrip("\n")
			array = line.split("\t")
			if array[0] not in Orthogroup:
				Orthogroup[array[0]] = []
				Orthogroup[array[0]].append(array[2])
			else: 
				Orthogroup[array[0]].append(array[2])
	for ortho in Orthogroup:
		#sort
		Orthogroup[ortho] = sort_ortho_by_spp(Orthogroup[ortho])
		for x in range(len(Orthogroup[ortho]) - 1):
			y = x + 1
			if ('NA' not in Orthogroup[ortho][x]) and ('NA' not in Orthogroup[ortho][y]):
				if Orthogroup[ortho][x] not in Edge:
					Edge[Orthogroup[ortho][x]] = {}
					Edge[Orthogroup[ortho][x]][Orthogroup[ortho][y]] = 1
				elif Orthogroup[ortho][y] not in Edge[Orthogroup[ortho][x]]:
					Edge[Orthogroup[ortho][x]][Orthogroup[ortho][y]] = 1
				else:
					Edge[Orthogroup[ortho][x]][Orthogroup[ortho][y]] += 1			
						
"""
	for ortho in Orthogroup:
		for x in range(len(Orthogroup[ortho])):
			for y in range(len(Orthogroup[ortho])):
				if (x < y) and (Orthogroup[ortho][x] != 'NA') and (Orthogroup[ortho][y] != 'NA'):
				#	print (Orthogroup[ortho][x], Orthogroup[ortho][y])
					if Orthogroup[ortho][x] not in Edge:
						Edge[Orthogroup[ortho][x]] = {}
						Edge[Orthogroup[ortho][x]][Orthogroup[ortho][y]] = 1
					elif Orthogroup[ortho][y] not in Edge[Orthogroup[ortho][x]]:
						Edge[Orthogroup[ortho][x]][Orthogroup[ortho][y]] = 1
					else:
						Edge[Orthogroup[ortho][x]][Orthogroup[ortho][y]] += 1
"""
outfile = "Edgeweight_paralogons_"+str(namefile)
outF = open(outfile, "w")
for source in Edge:
	for target in Edge[source]:
	#	print (source, target, Edge[source][target])
		outF.write(source+"\t"+target+"\t"+str(Edge[source][target])+"\n")
outF.close()



