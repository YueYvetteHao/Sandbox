#!/usr/bin/perl
use strict;

#Nodefile with number of genes in each paralogon as paralogon length

my ( $infile, $edgefile, $readfh, $outfh, $outfile, $line, @array,
	 %Paralogon, $scaffold, %Node
);

$infile = $ARGV[0]; # merged_WGD1_genelist.txt
$edgefile = $ARGV[1]; # filtered_Edgeweight_paralogons_orthofilelist.txt
$outfile = 'filtered_Nodefile_'.$infile;


open $readfh,'<',$edgefile or die "$!";

while (!eof($readfh)) {
    $line = <$readfh>;
    $line =~ s/\r?\n*//g;
    @array = split /\t/, $line;
    $Node{$array[0]} = 1;
    $Node{$array[1]} = 1;
}

close $readfh;




open $readfh,'<',$infile or die "$!";

while (!eof($readfh)) {
# PBIA.V1_4.1.P01010024	PBIA_1_1
    $line = <$readfh>;
    $line =~ s/\r?\n*//g;
    @array = split /\t/, $line;
    if ($Paralogon{$array[1]} =~ m/NA/) {
    	print qq{$Paralogon{$array[1]}\n};
    
    
    } else {
		if (!exists $Paralogon{$array[1]}) {
			$Paralogon{$array[1]} = 1;
		} else {
			$Paralogon{$array[1]}++;
		}
    }
    
}

close $readfh;



open $outfh,'>',$outfile or die "$!";
foreach $scaffold (sort(keys %Paralogon)) {
	if (exists $Node{$scaffold}) {	
		print $outfh qq{$scaffold\t$Paralogon{$scaffold}\n}
	}
}


close $outfh;


