#!/bin/bash 

# cd /Users/yhao38/Google_Drive/@ASU2020/Paramecium/Parse_tree/Param_ortho/trees
# for file in *.treefile
# do
# 	mv -- "$file" "${file%.treefile}.tre"
# done
# ls *.tre > treefilelist.txt
# cp treefilelist.txt /Users/yhao38/Google_Drive/@ASU2020/Paramecium/Parse_tree/Param_ortho

# cd /Users/yhao38/Google_Drive/@ASU2020/Paramecium/Parse_tree/WGD1
# ./merge_WGD1_files.sh
# cp merged_WGD1_genelist.txt /Users/yhao38/Google_Drive/@ASU2020/Paramecium/Parse_tree/Param_ortho

cd /Users/yhao38/Google_Drive/@ASU2020/Paramecium/Parse_tree/Param_ortho
#file=$1
input='treefilelist.txt'
while IFS= read -r line
do
	echo $line
	sed 's/;/:0.0;/g' ${line} > rootbranch_${line}
	mv rootbranch_${line} $line
	python reroot_tree.py $line
	sed 's/\[&R\] //g' rerooted_${line} > input_${line}
	mv input_${line} rerooted_${line}
	python parse_ortho_gene_tree.py species-names.tab rerooted_${line} merged_WGD1_genelist.txt
	python merge_ortho_groups.py species-names.tab Ortho_groups_rerooted_${line}.txt
done < $input

ls Merged_Ortho* > orthofilelist.txt

python prepare_edgefile.py orthofilelist.txt

./prepare_nodefile.pl merged_WGD1_genelist.txt

python paralogon_graph.py Nodefile_merged_WGD1_genelist.txt Edgeweight_paralogons_orthofilelist.txt species-names.tab


