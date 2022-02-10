#!/usr/bin/perl
use strict;


my ( $infile, $readfh, $line, %length, @Len, $mean_len,
	 $id
);

$infile = $ARGV[0]; # seq.fasta




=for comment
open $readfh,'<',$infile or die "$!";
while (!eof($readfh)) {
    $line = <$readfh>;
    $line =~ s/\r?\n*//g;
    if ($line !~ /^>/) {
    	$length = length($line);
    	
    #	print qq($length\n);
    	}
   
}
close $readfh;
=cut


open $readfh,'<',$infile or die "$!";

while (!eof($readfh)) {
      $line = <$readfh>;
      $line =~ s/\r?\n*//g;
      
      if($line =~ /^>/){
      		$id = $line;
      	#	print qq{$id\n};
      		$length{$id} = 0;
      } else {
            $line =~ s/\Q*\E//g;
            $length{$id} = $length{$id} + length($line); 
         #   print qq{$length{$id}\n};           
            next;
      }   
}

close $readfh;

foreach $id (sort keys %length) {
	push(@Len, $length{$id});
}





$mean_len = Average(@Len);

#print qq($mean_len\n);

sub Average {
   # get total number of arguments passed.
   my $n = scalar(@_);
   my $sum = 0;

   foreach my $item (@_) {
      $sum += $item;
   }
   my $average = $sum / $n;

   print "Average seq length : $average\n";
}