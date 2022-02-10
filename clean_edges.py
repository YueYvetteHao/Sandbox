#!/usr/bin/python

# Resolve conflicting paralogon connection

import sys
from paralogon_graph import get_paralog_node

edgefile = sys.argv[1]

global Edges
Edges = {}
file = open(edgefile, 'r')
for line in file:
	line = line.rstrip("\n")
	array = line.split("\t")
	if int(array[2]) > 1:
		if array[0] not in Edges:
			Edges[array[0]] = {}
			Edges[array[0]][array[1]] = int(array[2])
		else:
			Edges[array[0]][array[1]] = int(array[2])
file.close()

global to_remove
to_remove = {}

def sort_quartet(quartet):
	max_tie = 'False'
	max_weight = 0
	
	for x in quartet:
		for y in quartet[x]:
			if quartet[x][y] > max_weight:   #if tie, remove a random pair?
				max_weight = quartet[x][y]
				max_node1 = x
				max_node2 = y	
#	print (max_node1, max_node2,quartet[max_node1][max_node2], "max!!!")
	for x in quartet:
		for y in quartet[x]:						
			if quartet[x][y] == max_weight and (x != max_node1) and (y == max_node2):  
				max_tie = 'True'
				print (quartet)
			#	print (max_node1, max_node2,quartet[max_node1][max_node2], "max!!!")
				print (x, y,quartet[x][y], "tie!!!")
				
			elif quartet[x][y] == max_weight and (x == max_node1) and (y != max_node2):  
				max_tie = 'True'
				print (quartet)
			#	print (max_node1, max_node2,quartet[max_node1][max_node2], "max!!!")
				print (x, y,quartet[x][y], "tie!!!")
	
	
	if max_tie == 'True':
		min_weight = 10000
		for x in quartet:
		#	if (len(quartet) == 2) and 
			for y in quartet[x]:
				if (quartet[x][y] < min_weight) and (len(quartet[x]) > 1):   #if tie, remove a random pair?
					min_weight = quartet[x][y]
					min_node1 = x
					min_node2 = y	
	#	print (min_node1, min_node2,quartet[min_node1][min_node2], "min!!!")
	
	else:	
		for x in quartet:
			for y in quartet[x]:
				if (x == max_node1) and (y != max_node2):
					if x not in to_remove:
						to_remove[x] = {}
					to_remove[x][y] = quartet[x][y]
				elif (x != max_node1) and (y == max_node2):
					if x not in to_remove:
						to_remove[x] = {}
					to_remove[x][y] = quartet[x][y]
				
	return to_remove
			

edge_to_remove = {}
for node1 in Edges:
	dupl = {}	
	for node2 in Edges[node1]:
		if node2[:-1] not in dupl:
			dupl[node2[:-1]] = {}
			dupl[node2[:-1]][node2] = Edges[node1][node2]
		#	print (node1, node2, Edges[node1][node2])
		else:
			dupl[node2[:-1]][node2] = Edges[node1][node2]
	for i in dupl:
		if	len(dupl[i]) > 1:
			para_node1 = get_paralog_node(node1)
			quartet = {}
			for node in dupl[i]:
				if node1 in Edges:
					if node in Edges[node1]:
						if node1 not in quartet:
							quartet[node1] = {}
						quartet[node1][node] = Edges[node1][node]
				if para_node1 in Edges:
					if node in Edges[para_node1]:
						if para_node1 not in quartet:
							quartet[para_node1] = {}
						quartet[para_node1][node] = Edges[para_node1][node]
		#	print (quartet)
			to_remove = sort_quartet(quartet)
		#	print (to_remove)
			'''
			for x in to_remove:
				for y in to_remove[x]:
					if x not in edge_to_remove:
						edge_to_remove[x] = {}
					edge_to_remove[x][y] = Edges[x][y]
			
			
			min_weight = 100000
			for node in dupl[i]:
			#	print (node1, node, Edges[node1][node])
				if Edges[node1][node] < min_weight: #tie?
					min_weight = Edges[node1][node]
			
			for node in dupl[i]:
				if Edges[node1][node] == min_weight:
					if node1 not in edge_to_remove:
						edge_to_remove[node1] = {}
						edge_to_remove[node1][node] = Edges[node1][node]
					#	print (node1, node, Edges[node1][node])
					else:
						edge_to_remove[node1][node] = Edges[node1][node]
					#	print (node1, node, Edges[node1][node])

			'''
for node1 in to_remove:	
	for node2 in to_remove[node1]:
	#	if to_remove[node1][node2] > 1:
	#	print (node1, node2, Edges[node1][node2])
		del Edges[node1][node2]


outfile = 'filtered_'+str(edgefile)

outFH = open(outfile, "w")

for node1 in Edges:
	for node2 in Edges[node1]:
	#	if Edges[node1][node2] > 1:
		outFH.write(node1+"\t"+node2+"\t"+str(Edges[node1][node2])+"\n")
		
outFH.close()
			

					
					
				

		


		