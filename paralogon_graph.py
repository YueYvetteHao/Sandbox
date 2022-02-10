#!/usr/bin/python

# Scaffolds graph and find most probable synteny assignment
# Yue Hao
# 02/2021

# python paralogon_graph.py nodefile.txt edgefile.txt

import sys
import networkx as nx #version 2.5
#import matplotlib.pyplot as plt
from parse_ortho_gene_tree import get_species

def main():

#	Build graph
	Nodes = read_nodefile(sys.argv[1])
	Edges = read_edgefile(sys.argv[2])
	global G
	G = nx.DiGraph()
	G.add_nodes_from(Nodes)
	G.add_weighted_edges_from(Edges)
	global species
	species = get_species(str(sys.argv[3])) 
	
	
#	Outfiles
	orthofile = "Orthologous_blocks.txt"
	numgenefile = "Number_of_genes.txt"
	orphanfile = "Leftover_blocks.txt"
	global orthoFH
	global numgeneFH
	orthoFH = open(orthofile, "w")
	numgeneFH = open(numgenefile, "w")
	
		
# starting from the heaviest pair, elongate to a path 
# until path ends or path self connects
# remove path from graph
	i = 0
	while G.number_of_edges() > 0:
#	while i != 1:  # for testing
		print ('Path',i)
		
		
		if get_heaviest_close_edge(G) != 'None':
			curr_edge = get_heaviest_close_edge(G)
		else:
			curr_edge = get_heaviest_edge(G)
	#	for node in curr_edge:
	#		print (node, G.nodes[node]['length'])
	#	print (G.edges[curr_edge[0], curr_edge[1]])
		
		
		''' Initiating Path... '''
		Path = nx.DiGraph()
		Path.add_edge(curr_edge[0], curr_edge[1])		
		
		''' Extending Path... '''
		j = 0
		extended = extend_path(curr_edge[0], curr_edge[1], Path)
		pathstart = extended[0]
		pathend = extended[1]
		Path = extended[2]
		print_path(Path)
	#	print (pathstart)
	#	print (pathend)
	
		''' Initiating Paralog Path... '''
		para_edge = []
		for edge in Path.edges:
			if (get_paralog_node(edge[0]) in G.nodes) and (get_paralog_node(edge[1]) in G.nodes) and ((get_paralog_node(edge[0]), get_paralog_node(edge[1])) in G.edges):
				para_edge = get_paralog_edge(edge)
				break
		
		# Write to file, remove traversed nodes
		write_to_outfile(i, j, pathstart, pathend, Path)
		remove_empty_node(Path)

	#	i += 1  # for testing
		
		Para_Path = nx.DiGraph()
		
	#	if G.edges[] != {}:
				
		
		if (para_edge != []):
			''' Extending Paralog Path... '''
			Para_Path.add_edge(para_edge[0], para_edge[1])
			j = 1
			extended = extend_path(para_edge[0], para_edge[1], Para_Path)
			pathstart = extended[0]
			pathend = extended[1]
			Para_Path = extended[2]
			print_path(Para_Path)
		#	print (pathstart)
		#	print (pathend)
			write_to_outfile(i, j, pathstart, pathend, Para_Path)
			remove_empty_node(Para_Path)
		
		
		i += 1
		
	#	if i == 1: # for testing
	#		break
	
	#	print ('Orphan nodes')
	orphanFH = open(orphanfile, "w")
	for node in G.nodes:
	#	print (node)
		if G.nodes[node]['length'] == G.nodes[node]['total']:
			orphanFH.write(node+"\t"+str(G.nodes[node]['length'])+"\n")
	orphanFH.close()	
		
		
	orthoFH.close()
	numgeneFH.close()
	




def write_to_outfile(i, j, pathstart, pathend, Path):
	orthoFH.write("Path_"+str(i)+'_'+str(j)+"\t")
	numgeneFH.write("Path_"+str(i)+'_'+str(j)+"\n")
	Pathspp = {}
	for each in list(Path.nodes):
		Pathspp[each[0:4]] = each
	for spp in species:
		if spp in Pathspp:
			orthoFH.write(Pathspp[spp]+"\t")
		else:
			orthoFH.write("-\t")
	orthoFH.write("\n")
	node = pathstart
	while node != pathend:
	#	print (node, G.nodes[node]['length'], end = '\t')
		if node == pathstart:
			numgeneFH.write(node+"\t"+str(G.nodes[node]['total'])+"\t") # +str(G.nodes[node]['length'])+"\t"
		else:
			numgeneFH.write(node+"\t"+"\t"+"\t")
		for nbr in Path.successors(node):
			successor = nbr
	#	print (successor, G.nodes[successor]['length'], end = "\t")
	#	print (G.edges[node, successor]['weight'])
		numgeneFH.write(successor+"\t"+str(G.nodes[successor]['total'])+"\t"+str(G.edges[node, successor]['weight'])+"\n") # +str(G.nodes[successor]['length'])+"\t"
		# Ortho assign with the most gene trees as support
		G.nodes[node]['length'] = int(G.nodes[node]['length']) - 10000
		# Allow for fission and fusion
	#	G.nodes[node]['length'] = int(G.nodes[node]['length']) - int(G.edges[node, successor]['weight'])	
	#	print (node, G.nodes[node]['length'], end = '\n')
		G.nodes[successor]['length'] = int(G.nodes[successor]['length']) - 10000
	#	G.nodes[successor]['length'] = int(G.nodes[successor]['length']) - int(G.edges[node, successor]['weight'])
		G.remove_edge(node, successor)
		node = successor



def remove_empty_node(Path):
	for node in Path.nodes:
		if G.nodes[node]['length'] <= 0:
		#	print (node, G.nodes[node]['length'])
			G.remove_node(node)
			print ("Removing", node)
	
	print ("Number of nodes:" ,G.number_of_nodes())
	print ("Number of edges:" ,G.number_of_edges())




def print_path(Path):
	print ('Edges in path:')
	for edge in Path.edges:
		print (edge)
		n = edge[0]
		nbr = edge[1]
		print (n, G.nodes[n]['length'], nbr, G.nodes[nbr]['length'], G.edges[n, nbr]['weight'], end = '\t')
		print ('\n')


def sort_path_by_weight(Path):
	return


def extend_path(node_left, node_right, Path):
#	right = extend_right(curr_edge[1], Path)
	right = extend_right(node_right, Path)
	Path = right[1]
	pathend = right[0]		
#	print (list(Path))
#	left = extend_left(curr_edge[0], Path)
	left = extend_left(node_left, Path)
	Path = left[1]
	pathstart = left[0]		
#	print (list(Path))
	return pathstart, pathend, Path


def extend_right(node, Path):
	while has_successor(node) == 'True':
		if find_best_close_successor(node) != 'None':
			best_successor = find_best_close_successor(node)
		else:
			best_successor = find_best_successor(node)
	#	print ('Successor:', best_successor)
		if best_successor not in Path.nodes:
		#	Path.add_node(best_successor)
			Path.add_edge(node, best_successor)
		#	print (node, best_successor)
			node = best_successor
		else:
			break
	pathend = node
	return pathend, Path

def extend_left(node, Path):
	while has_predecessor(node) == 'True':
		if find_best_close_predecessor(node) != 'None':
			best_predecessor = find_best_close_predecessor(node)
		else:
			best_predecessor = find_best_predecessor(node)
	#	print ('Predecessor:',best_predecessor)
		if best_predecessor not in Path.nodes:
		#	Path.add_node(best_predecessor)
			Path.add_edge(best_predecessor, node)
		#	print (best_predecessor, node)
			node = best_predecessor
		else:
			break
	pathstart = node	
	return pathstart, Path
	

def get_paralog_edge(edge):
	para_edge = []
	para_edge.append(get_paralog_node(edge[0]))
	para_edge.append(get_paralog_node(edge[1]))
	return para_edge

def get_paralog_node(node):
	if node[-1] == '1':
		para_node = node[:-1] + '2'
	elif node[-1] == '2':
		para_node = node[:-1] + '1'
	return para_node

	
		
def has_successor(node):
	if len(list(G.successors(node))) > 0:
		return ('True')
	else:
		return ('False')

def has_predecessor(node):
	if len(list(G.predecessors(node))) > 0:
		return ('True')
	else:
		return ('False')	

def find_best_successor(node):
#	successors with heaviest edge
	max_weight = 0
	best_successor = ''
	for successor in G.successors(node):
		if G.edges[node, successor]['weight'] > max_weight:
			max_weight = G.edges[node, successor]['weight']
			best_successor = successor
	return (best_successor)

def find_best_close_successor(node):
#	successors with heaviest edge
	max_weight = 0
	best_successor = 'None'
	for successor in G.successors(node):
		if (spp_order(successor[0:4]) == (spp_order(node[0:4]) + 1)) and (G.edges[node, successor]['weight'] > max_weight):
			max_weight = G.edges[node, successor]['weight']
			best_successor = successor
	return (best_successor)
	
def find_best_predecessor(node):
#	predecessors with heaviest edge
	max_weight = 0
	best_predecessor = ''
	for predecessor in G.predecessors(node):
		if G.edges[predecessor, node]['weight'] > max_weight:
			max_weight = G.edges[predecessor, node]['weight']
			best_predecessor = predecessor
	return (best_predecessor)

def find_best_close_predecessor(node):
#	predecessors with heaviest edge
	max_weight = 0
	best_predecessor = 'None'
	for predecessor in G.predecessors(node):
		if (spp_order(node[0:4]) == (spp_order(predecessor[0:4]) + 1)) and (G.edges[predecessor, node]['weight'] > max_weight):
			max_weight = G.edges[predecessor, node]['weight']
			best_predecessor = predecessor
	return (best_predecessor)
	
def get_heaviest_edge(G):
	max_weight = 0
	for edge in G.edges:
	#	print (edge, G.edges[edge]['weight'])
		if ('NA' not in edge[0]) and ('NA' not in edge[1]):
			if G.edges[edge]['weight'] > max_weight:
				max_weight = G.edges[edge]['weight']
				heaviest_edge = edge
	return (heaviest_edge)
	
def get_heaviest_close_edge(G):
	max_weight = 0
	heaviest_edge = 'None'
	for edge in G.edges:
	#	print (edge, G.edges[edge]['weight'])
		if ('NA' not in edge[0]) and ('NA' not in edge[1]):
			if (spp_order(edge[1][0:4]) == (spp_order(edge[0][0:4]) + 1)) and (G.edges[edge]['weight'] > max_weight):
				max_weight = G.edges[edge]['weight']
				heaviest_edge = edge
	return (heaviest_edge)
	
def spp_order(string):
	for i in range(len(species)):
		if (species[i] == string[0:4]):
			return i	

def read_nodefile(filename):
	Nodes = []
	file = open(filename, 'r')
	for line in file:
		line = line.rstrip("\n")
		array = line.split("\t")
		# node attribute: paralogon length = number of genes in the paralogon
		node = (array[0], {'total': array[1], 'length': array[1]})
		Nodes.append(node)		
	file.close()
	return Nodes

def read_edgefile(filename):
	Edges = []
	file = open(filename, 'r')
	for line in file:
		line = line.rstrip("\n")
		array = line.split("\t")
		edge = (array[0], array[1], int(array[2]))
		Edges.append(edge)
	file.close()
	return Edges

if __name__ == '__main__':
	main()
