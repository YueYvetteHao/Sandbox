#!/usr/bin/perl
use strict;

#combine two lists


my ( $infile1, $infile2, $readfh, $outfh, $outfile, $line, @array, @IDs, %Proteins,
%Intensity, %Annote
);

$infile1 = $ARGV[0]; #proteome with intensity #stentor_intensity.txt
$infile2 = $ARGV[1]; #annotation file  #stentor_annotation_uniprot.txt
#$outfile = 'Annotated_'.$infile1;

open $readfh,'<',$infile2 or die "$!";
#headline
$line = <$readfh>; #ID	Name	GO	Comment|SubcellularLocation
while (!eof($readfh)) {
	$line = <$readfh>; 
    $line =~ s/\r?\n*//g;
    @array = split /\t/, $line;
    $Annote{$array[0]} = $line;
}
close $readfh;

open $readfh,'<',$infile1 or die "$!";
#headline
$line = <$readfh>;
while (!eof($readfh)) {
	$line = <$readfh>; #12	A0A060BQW6	7.5903E+11	Stentor coeruleus
    $line =~ s/\r?\n*//g;
    @array = split /\t/, $line;
    @IDs = split /;/, $array[1];
    print qq{$line\t};
    foreach (@IDs) {
    	if (exists $Annote{$_}) {
    		print qq{$Annote{$_}\t};
    	}
    }
    print qq{\n};
     

}
close $readfh;






#open $outfh,'>',$outfile or die "$!";
#close $outfh;


