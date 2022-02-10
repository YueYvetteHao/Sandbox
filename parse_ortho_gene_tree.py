#!/usr/bin/python

# Parse paramecium gene trees for PoFF ortho families.
# Yue Hao
# 09/2020

# python parse_ortho_gene_tree.py species-names.tab test_90.nt_ali.fasta.tre merged_WGD1_genelist.txt 


import sys
import copy
import collections
import Bio.Phylo as Phylo


def main():	
	global species
	# species-names.tab
	species = get_species(str(sys.argv[1])) 
	global synteny
	synteny = read_synteny(str(sys.argv[3]))
	global tree
	tree = Phylo.read(str(sys.argv[2]), 'newick')
	tree.ladderize()
	global parents
	parents = all_parents(tree)
	
#	print ("======Checking for gene duplication======")
	if gene_dupl(tree, species) == 'True':
		Ortho_groups={}
	#	print ("======Finding ABAB subtrees======")
		dupl_pairs=find_dupl_pairs(tree)
		# Store initial dupl pairs to ortho group
		i = 0
		for pair in dupl_pairs:
		#	print ("((A,B),(A\',B\')) subtree ",i)
			for j in dupl_pairs[pair]:		
				Ortho_groups[i] = [term.name for term in dupl_pairs[pair][j].get_terminals()]
				dupl_pairs[pair][j].name = str(i)
				tree = collapse_clade(dupl_pairs[pair][j], tree)
				i += 1
			#	tree = copy.deepcopy(tree)
	#	print (tree) 
	
	#	print ("======Merging ortholog groups======")	
		prev_term = tree.count_terminals()
		curr_term = 1
		i = 1
		global trifurcate
		trifurcate=[]
		while(curr_term > 0):
		#	print ("Iteration", i)
			if num_terms(tree) == 1:
				break
			Ortho_groups = merge_ortho(Ortho_groups, tree)
		#	print (tree)
			curr_term = tree.count_terminals()
			i += 1
			if curr_term == prev_term:
				break
			else:
				prev_term = curr_term
	
	#	print ("======Printing ortholog groups to file======")	
		outfile = "Ortho_groups_" + str(sys.argv[2]) + ".txt"
		outF = open(outfile, "w")
		i = 0
		for ortho in Ortho_groups:
			for gene in Ortho_groups[ortho]:
			#	print (i, end = "\t")
			#	print (gene, synteny[gene], sep='\t', end = "")
				outF.write(str(i)+"\t"+gene+"\t"+synteny[gene])
			i += 1
		#	print (ortho, Ortho_groups[ortho])	
	
	#	print ("======Lefover tips======")
		for term in tree.get_terminals():
			if (term.name[0:4] in species):
			#	print (i, term.name, synteny[term.name], sep='\t', end = "")
				outF.write(str(i)+"\t"+term.name+"\t"+synteny[term.name])
				i += 1
		#print (tree)
		outF.close()
	
	else:
		outfile = "Ortho_groups_" + str(sys.argv[2]) + ".txt"
		outF = open(outfile, "w")	
		i = 0	
		for term in tree.get_terminals():
			if (term.name[0:4] in species):
			#	print (i, term.name, synteny[term.name], sep='\t', end = "")
				outF.write(str(i)+"\t"+term.name+"\t"+synteny[term.name])
			#	i += 1
		#print (tree)
		outF.close()	
	
	
def merge_ortho(Ortho_groups, tree):	
	# merging ortho groups
	ortho_to_remove=[]
	for ortho in Ortho_groups:
		if (ortho not in trifurcate) and (ortho not in ortho_to_remove):
			sisters = find_sister(ortho)
		#	print (ortho, Ortho_groups[ortho])
		#	print (sisters)	
			if (len(sisters) == 1):
				# Is a terminal
				if (sisters[0][0:4] in species) and (sisters[0][0:4] not in list(gene[0:4] for gene in Ortho_groups[ortho])):
					Ortho_groups[ortho].append(sisters[0])	
					parent = parents[clade_by_name(sisters[0])]
					if parent.is_bifurcating() == True:
						parent.name = str(ortho)
						for term in parent.get_terminals():	
							tree.collapse(term)
					else:
						tree.collapse(clade_by_name(sisters[0])) 
						tree.collapse(clade_by_name(str(ortho)))
						trifurcate.append(ortho)	
			#		print (ortho, Ortho_groups[ortho])
			#		print (tree)
				# Is an internal node
				elif (sisters[0][0:4] not in species) and (int(sisters[0]) > ortho) and (int(sisters[0]) in Ortho_groups) and (overlap(bitstring_from_list(Ortho_groups[int(sisters[0])]), bitstring_from_list(Ortho_groups[ortho])) == 'False'):
					for gene in Ortho_groups[int(sisters[0])]:
						Ortho_groups[ortho].append(gene)
					ortho_to_remove.append(int(sisters[0]))
					parent = parents[clade_by_name(sisters[0])]
					clade = clade_by_name(sisters[0])
					tree.collapse(clade) 
					clade = clade_by_name(str(ortho))
					tree.collapse(clade) 
					"""
					for clade in parent.find_clades():
						if clade != parent:
							print ("Found clade: ", clade)
							tree.collapse(clade)
					"""
					parent.name = str(ortho)
			#		print (ortho, Ortho_groups[ortho])
			#		print (tree)
			
	for ortho in ortho_to_remove:
		del Ortho_groups[ortho]
#	for ortho in Ortho_groups:
	#	print (ortho)
#		for gene in Ortho_groups[ortho]:
	#		print (gene, synteny[gene])
		#	print (ortho, Ortho_groups[ortho])	
#	print (tree)
#	print ("Number of terminals: ", tree.count_terminals())
	return (Ortho_groups)
	

	#Repeat:
	# prune clade
	#Find sister, add sister to ortho group
	
	# Save the leftover tree to file

def overlap(A, B):
	"""True if A and B are overlapping, otherwise False"""
	Arg = 'False'
	for i in range(len(species)):
		if (int(A[i]) == 1) and (int(A[i]) == int(B[i])):
			Arg = 'True'
	return (Arg)




def find_sister(ortho):
	clade = clade_by_name(str(ortho))
	sister=[]
	parent = parents[clade]
	if parent.is_bifurcating() == True:
		for term in parent.get_terminals():
			if term not in clade.get_terminals():
				sister.append(term.name)
	else: #trifurcating clade (probably at root): Need to fix this
		for sis_clade in parent:
			if (sis_clade != clade) and (num_terms(sis_clade) <= 2):
				for term in sis_clade.get_terminals():
					sister.append(term.name)
	return sister


def collapse_clade(clade, tree):
#	tree = copy.deepcopy(tree)
#	for child in clade:	
	for child in clade.get_terminals():	
		tree.collapse(child)
#	global parents 
#	parents = all_parents(tree)
	return tree


def clade_by_name(string):
	for clade in tree.find_clades():
		if clade.name == str(string):
			return clade
	
def get_parent(tree, child_clade):
    node_path = tree.get_path(child_clade)
    return node_path[-2]


def clade_depth(clade):
	clade_path = tree.get_path(clade)
	return (len(clade_path))


def find_dupl_pairs(tree):
	dupl_pairs= {}
	for clade in tree.find_clades(terminal=False):
		if num_terms(clade) == 2:
			terms = []
			for term in clade.get_terminals():
				terms.append(term.name)
			if terms[0][0:4] != terms[1][0:4]:
				bitstr = bitstring(clade)
				if bitstr in dupl_pairs:
					j = len(dupl_pairs[bitstr])
					dupl_pairs[bitstr][j] = clade
				else: 
					dupl_pairs[bitstr] = {}
					dupl_pairs[bitstr][0] = clade
	return dupl_pairs

		
def num_terms(clade):
    """Count the number of terminal nodes within a clade."""	
    return sum(1 for term in clade.get_terminals())
	
def bitstring(clade):
	"""Convert tips in a clade to bitstring."""	
	terms = []
	boolean = ''
	for term in clade.get_terminals():
		terms.append(term.name[0:4] )
	for spp in species:
		if spp in terms:
			boolean += '1'
		else:
			boolean += '0'
	return(boolean)	

def bitstring_from_list(array):
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


def gene_dupl(tree, species):
	Arg = 'False'
	gene_count = {}
	for term in tree.get_terminals():
		if term.name[0:4] in species:
			if term.name[0:4] not in gene_count:
				gene_count[term.name[0:4]] = 1
			else:
				gene_count[term.name[0:4]] += 1
	for spp in gene_count:
		if gene_count[spp] > 1:
			Arg = 'True'
	return Arg
			

def get_species(sppfile):
	"""Read species list from a file, store four-letter boolean for each species."""
	file = open(sppfile, 'r')
	spp = []
	#headline
	next(file)
	for line in file:
		spp.append(line[0:4])
	file.close()
	return(spp) 

	
def all_parents(tree):
    parents = {}
    for clade in tree.find_clades(order="level"):
        for child in clade:
            parents[child] = clade
    return parents

def read_synteny(syntenyfile):
	file = open(syntenyfile, 'r')
	synteny = {}
	array = []
	for line in file:
		array = line.split("\t")
		synteny[array[0]] = array[1]
	file.close()
	return(synteny) 

if __name__ == '__main__':
	main()
