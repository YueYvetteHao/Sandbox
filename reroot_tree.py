#!/usr/bin/python

# Rerooting tree

import sys
import dendropy # DendroPy-4.4.0

treefile = str(sys.argv[1])
tree = dendropy.Tree.get(path=treefile, schema="newick", rooting='force-rooted')
for node in tree.preorder_node_iter():
    if node.parent_node is None:
         root = node


#print("Before:")
#print(tree.as_string(schema='newick'))
#print(tree.as_ascii_plot(plot_metric='length'))

#tree.reroot_at_midpoint(update_bipartitions=False)

#print("After:")
#print(tree.as_string(schema='newick'))
#print(tree.as_ascii_plot(plot_metric='length'))


subspp = ["PSON", "PJEN", "PSEX"]
taxons = []

for taxon in tree.taxon_namespace:
	if taxon.label[0:4] in subspp:
	#	print (taxon.label)
		taxons.append(taxon.label)

if len(taxons) > 1:
	mrca = tree.mrca(taxon_labels=taxons)
	if mrca != root:
		tree.reroot_at_edge(mrca.edge, length1=0.5 * mrca.edge_length, length2=0.5 * mrca.edge_length, update_bipartitions=True)		
elif len(taxons) == 1:
	node = tree.find_node_with_taxon_label(taxons[0])
	tree.reroot_at_edge(node.edge, length1=0.5 * node.edge_length, length2=0.5 * node.edge_length, update_bipartitions=True)
else:
	tree.reroot_at_midpoint(update_bipartitions=True)

	
tree.resolve_polytomies(limit=2, update_bipartitions=True)
tree.ladderize(ascending=True)
outtree = 'rerooted_'+treefile
tree.write(path=outtree, schema="newick")



