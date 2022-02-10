#!/usr/bin/python

# Merge orthology groups
# Yue Hao
# 10/2020

# python merge_ortho_groups.py species-names.tab Ortho_groups_test_90.nt_ali.fasta.tre.txt

import sys
from parse_ortho_gene_tree import get_species

def main():
	global species
	species = get_species(str(sys.argv[1])) 
	Ortho_groups = read_ortho_group(str(sys.argv[2]))
	longest_group = find_longest_group(Ortho_groups)
	bts_longest = bitstring(list(gene for gene in longest_group))
	to_remove = []
	merge_group = {}
	bts_merge = bitstring(list(gene for gene in merge_group))	
	for group in Ortho_groups:
		bitstr = bitstring(list(gene for gene in Ortho_groups[group]))
		if (Ortho_groups[group] == longest_group):
	#	if (bitstr == bts_longest):
			to_remove.append(group)
	#	elif (is_subset(bitstr, bts_longest) == 'True') and (overlap(bitstr, bts_merge) == 'False'):
		elif (overlap(bitstr, bts_longest) == 'True') and (overlap(bitstr, bts_merge) == 'False'):
			for gene in Ortho_groups[group]:
				merge_group[gene] = Ortho_groups[group][gene]
			bts_merge = bitstring(list(gene for gene in merge_group))
			to_remove.append(group)		
	for ortho in to_remove:
		del Ortho_groups[ortho]
		
	outfile = "Merged_" + str(sys.argv[2])
	outF = open(outfile, "w")
	i = 0
	for gene in dict(sorted(longest_group.items(), key=lambda x: x[0].lower())):
		outF.write(str(i)+"\t"+gene+"\t"+longest_group[gene]+"\n")
	if len(merge_group) > 0:
		i = 1
		for gene in dict(sorted(merge_group.items(), key=lambda x: x[0].lower())):
			outF.write(str(i)+"\t"+gene+"\t"+merge_group[gene]+"\n")
	else:
		i = 0
	for group in Ortho_groups:
		i += 1
		for gene in dict(sorted(Ortho_groups[group].items(), key=lambda x: x[0].lower())):
			outF.write(str(i)+"\t"+gene+"\t"+Ortho_groups[group][gene]+"\n")
	outF.close()



def find_longest_group(Ortho_groups):
	longest_group = {}
	longest_len = 0
	for group in Ortho_groups:
		bitstr = bitstring(list(gene for gene in Ortho_groups[group]))
		bitstr_len = bitstring_length(bitstr)
		if bitstr_len > longest_len:
			longest_len = bitstr_len
			longest_group = Ortho_groups[group]
	return (longest_group)

def read_ortho_group(orthofile):
	file = open(orthofile, 'r')
	Ortho_groups = {}
	for line in file:
		line = line.rstrip("\n")
		array = line.split("\t")
		if array[0] not in Ortho_groups:
			Ortho_groups[array[0]] = {}
			Ortho_groups[array[0]][array[1]] = array[2]
		else:
			Ortho_groups[array[0]][array[1]] = array[2]
	file.close()
	return(Ortho_groups) 
	
	
# A bunch of bitstring functions

def overlap(A, B):
	"""True if A and B are overlapping, otherwise False"""
	Arg = 'False'
	for i in range(len(species)):
		if (int(A[i]) == 1) and (int(A[i]) == int(B[i])):
			Arg = 'True'
	return (Arg)
	
def is_subset(A, B):
	"""True if A is a subset of B, otherwise False"""
	Arg = 'True'
	for i in range(len(species)):
		if int(A[i]) > int(B[i]):
			Arg = 'False'
	return (Arg)

def bitstring_length(bitstr):
	length = 0
	for i in bitstr:
		if int(i) > 0:
			length += 1
	return (length)

def bitstring(array):
	"""Convert an array to bitstring."""	
	terms = []
	boolean = ''
	for term in array:
		terms.append(term[0:4])
	for spp in species:
		if spp in terms:
			boolean += '1'
		else:
			boolean += '0'
	return(boolean)	







if __name__ == '__main__':
	main()