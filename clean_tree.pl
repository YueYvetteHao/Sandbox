#!/usr/bin/perl
use strict;

#Removing gene names and leaving only species identifies in the Paramecium gene tree.

my ( $infile, $readfh, $outfh, $outfile, $line, @array
);

$infile = $ARGV[0];
$outfile = 'clean_'.$infile.'.tre';
#$outfile =~ s/\.nt_ali\.fasta\.treefile//g;
$outfile =~ s/\.nt_ali\.fasta\.tre//g;
open $readfh,'<',$infile or die "$!";
open $outfh,'>',$outfile or die "$!";
while (!eof($readfh)) {
    $line = <$readfh>;
    $line =~ s/\r?\n*//g;
    $line =~ s/_//g;
    $line =~ s/(P[A-Z]+)\.[A-Za-z0-9]+\.[A-Z0-9]+\.[A-Z0-9]+:/$1:/g;
    $line =~ s/(P[A-Z]+)[0-9]{0,5}:/$1:/g;
    $line =~ s/:[0-9]+\.[0-9]+,/,/g;
    $line =~ s/:[0-9]+\.[0-9]+\)/\)/g;
    print $outfh qq{$line\n};
}

close $readfh;
close $outfh;

