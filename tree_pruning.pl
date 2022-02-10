#!/usr/bin/perl
use strict;

#prune a tree, remove unwanted branches

my($readfh, $treefile, $line, $num_group, @remove,
   @sistergroup,@singlebranch, $remove,
    @array, $before, $after, $pos,
   $i,$j, $num_left, $num_right, $outfh, $outfile,
   $speciesfile, $sppfh
   );
#tree file
$treefile = $ARGV[0];
#list of species need to be removed
$speciesfile = $ARGV[1];
$outfile = $speciesfile;
$outfile =~ s/^[\w\W]+([0-9]+_[0-9]+)[\w\W]+/$1/g;
$outfile = 'pruned_'.$outfile.".tre";


open $readfh,'<',$treefile or die "$!";
open $outfh,'>',$outfile or die "$!";
open $sppfh,'<',$speciesfile or die "$!";

$line = <$readfh>;
$line =~ s/\r?\n*//g;
print qq{$line\n};
close $readfh;

if (scalar(@ARGV) >1) {

	while (!eof($sppfh)) {
	   $remove = <$sppfh>;
		$remove =~ s/\r?\n*//g;
	    
   # print qq{$line\n};


 @sistergroup = $line =~ /\($remove\,[\w\_]+\)|\([\w\_]+\,$remove\)/g;

   if (@sistergroup) {
    print qq{Pruning $remove.\n};
	    if ($line =~ /\($remove\,[\w\_]*\)/g) {
     	 $line =~ s/\($remove\,([\w\_]*)\)/$1/g;
     }   if ($line =~ /\([\w\_]*\,$remove\)/g) {
         $line =~ s/\(([\w\_]*)\,$remove\)/$1/g;
     }
    
    print qq{$line\n};
    } 

 @singlebranch = $line =~ /\($remove\,\(|\)\,$remove\)/g;
  if (@singlebranch) {
   	if ($line =~ /\($remove\,\(/g) {
    	print qq{Pruning $remove.\n};
        $before = $line;
        $before =~ s/^([\S]*)\($remove[\S]+/$1/g;
        $after = $line;
        $after =~ s/^([\S]*\()$remove\,([\S]+)$/$2/g;
      # print qq{$before\n$after\n};
        @array = split //, $after;
        $num_left = 0;  #num left bracket
        $num_right = 0;  #num right bracket
        for ($i=0; $i<scalar(@array); $i++) {
            if ($num_left ==0 || $num_right ==0 || $num_left != $num_right) {
        	 if ($array[$i] eq '(') {
        	    $num_left++; 
       # 	    print qq{Left brackets $num_left\n};
        	 } elsif ($array[$i] eq ')') {
        		$num_right++;
        #		print qq{Right brackets $num_right\n};
        	 } 
        	} elsif ($num_left > 0 && $num_right >0 && $num_left == $num_right) {
        	       $pos = $i;
        	       last;
        	}
        } 
        #print qq{$pos\t$array[$pos]\n};  
        splice @array, $pos, 1; #remove right bracket
        $after = join( '' , @array );
        $line = $before.$after;
        
        print qq{$line\n};
        
    } 
    if ($line =~ /\)\,$remove\)/g) {
       print qq{Pruning $remove.\n};
         $before = $line;
        $before =~ s/^([\S]*\))\,$remove[\S]+/$1/g;
        $after = $line;
        $after =~ s/^([\S]*\))\,$remove\)([\S]+)$/$2/g;
       # print qq{$before\n$after\n};
      
       
        @array = split //, $before;
        $num_left = 0;  #num left bracket
        $num_right = 0;  #num right bracket
        for ($i=scalar(@array)-1; $i>=0; $i--) {
            if ($num_left ==0 || $num_right ==0 || $num_left != $num_right) {
        	 if ($array[$i] eq '(') {
        	    $num_left++;
        	 } elsif ($array[$i] eq ')') {
        		$num_right++;
        	 } 
        	} elsif ($num_left > 0 && $num_right >0 && $num_left == $num_right) {
        	       $pos = $i;
        	       last;
        	}
        } 
        #print qq{$pos\t$array[$pos]\n};  
        splice @array, $pos, 1; #remove right bracket
        $before = join( '' , @array );
        $line = $before.$after;
        
        print qq{$line\n};
       }    	
    

   }

  #$line = $line;


}
} else {
	print qq{Usage: ./tree_pruning.pl <tree.tre> <specieslist.txt> \n} ;
} 

print $outfh qq{$line\n};
close $outfh;

