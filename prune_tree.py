#!/usr/bin/python
import dendropy
import sys

treefile = str(sys.argv[1])
tree = dendropy.Tree.get(path=treefile, schema="newick")

#print("Before:")
#print(tree.as_string(schema='newick'))
#print(tree.as_ascii_plot())


subspp = ["RRRR","PSEX", "PJEN", "PBIA", "PTET", "PQUA"]
#, "PTET", "PQUA"
taxons = []
for taxon in tree.taxon_namespace:
	if taxon.label[0:4] in subspp:
	#	print (taxon.label)
		taxons.append(taxon.label)

tree.retain_taxa_with_labels(taxons)
#tree.prune_taxa_with_labels(["PBIA.V1 4.1.P00220009","PDEC.223.1.P00070048","PSEX.AZ8 4.1.P0470047","PNOV.TE.1.P03730028"])
#print("After:")
#print(tree.as_string(schema='newick'))
print(tree.as_ascii_plot())

outtree = 'pruned_'+treefile
tree.write(path=outtree, schema="newick")