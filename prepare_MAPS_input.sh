#!/bin/bash 

cd /Users/yhao38/Google_Drive/@ASU2020/Paramecium/Parse_tree/Param_ortho
line=$1
#input=$1
#while IFS= read -r line
#do
	echo $line
	python reroot_tree.py $line
	sed 's/\[&R\] /(/g' rerooted_${line} > root_${line}
	sed 's/;/,RRRR);/g' root_${line} > input_${line}
	rm root_${line}
	mv input_${line} rerooted_${line}
	python prune_tree.py rerooted_${line}
	perl clean_tree.pl pruned_rerooted_${line}
#done < $input