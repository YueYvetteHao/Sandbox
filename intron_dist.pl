#!/usr/bin/perl
use strict;


my ( $infile, $readfh, $line, @array, @Index, $id,
#	 %utr3, %utr5, 
	 $key, @utr3, @utr5, @exon_len,
	 $mean_utr3, $mean_utr5, @intron_len, @num_intron, @all_intron

);

$infile = $ARGV[0]; # annotation.gff3



open $readfh,'<',$infile or die "$!";
$id = -1;
while (!eof($readfh)) {
      $line = <$readfh>;
      $line =~ s/\r?\n*//g;
      if ($line !~ /^#/){
      	@array = split /\t/, $line;
      	if ($array[2] =~ /gene/) {
      		$id++;
      		@{$Index[$id]}=();
      		push(@exon_len, 0);
      	} else {
      		if ($array[2] =~ /exon/) {
      			push(@{$Index[$id]}, int($array[3]));
      			push(@{$Index[$id]}, int($array[4]));  
      			$exon_len[$id] = $exon_len[$id] + int($array[4]) - int($array[3]) + 1;
      			    			
      		}
      		elsif ($array[2] =~ /three_prime_UTR/) {
      		#	$utr3{$id} = int($array[4]) - int($array[3]) + 1;
      			push(@utr3, int($array[4]) - int($array[3]) + 1);
      		}
      		elsif ($array[2] =~ /five_prime_UTR/) {
      		#	$utr5{$id} = int($array[4]) - int($array[3]) + 1;
      			push(@utr5, int($array[4]) - int($array[3]) + 1);
      		}
      		next;
      	}
      }
}

close $readfh;
print qq{Number of genes: };
print (scalar(@exon_len));
print qq{\n};
print qq{Average cds length: };
print Average(@exon_len);
print qq{\n};

foreach (@Index) {
#	print qq{Exon: @{$_}\n};
	@array = Exon2Intron(@{$_});
#	print qq{Intron: @array\n};
	@intron_len = IntronLen(@array);
#	print qq{Intron length: @intron_len\n};
	push(@num_intron, scalar(@intron_len));
	push(@all_intron, @intron_len);
	
}


print qq{Mean number of introns per gene: };
print Average(@num_intron);
print qq{\n};
print qq{Average intron length: };
print Average(@all_intron);
print qq{\n};
=for comment
foreach $key (keys %utr3) {
	print qq{$utr3{$key}\t};
}
print qq{\n};
=cut

#print qq{3UTR: @utr3\n};


if (scalar(@utr3) >0) {
	$mean_utr3 = Average(@utr3);
	print qq{3UTR avg: $mean_utr3\n};
}
if (scalar(@utr5) >0) {
	$mean_utr5 = Average(@utr5);
	print qq{5UTR avg: $mean_utr5\n};
}
#print qq($mean_len\n);

sub Exon2Intron {
	my @exon = @_;
	my @intron = ();
	for (my $i = 1; $i < scalar(@exon)-1; $i++) {
		if ($i % 2 == 1) {
			push(@intron, $exon[$i]+1);
		} elsif ($i % 2 == 0){
			push(@intron, $exon[$i]-1);
		}
	}
	return (@intron);
}

sub IntronLen {
	my @intron = @_;
	my @len = ();
	my $i = 0;
	while($i < scalar(@intron)) {
		push(@len, $intron[$i+1] - $intron[$i] + 1);
		$i = $i + 2;
	}
	return (@len);
	
}

sub Average {
   # get total number of arguments passed.
   my $n = scalar(@_);
   my $sum = 0;

   foreach my $item (@_) {
      $sum += $item;
   }
   my $average = $sum / $n;
   return ($average);
#   print "Average seq length : $average\n";
}

sub Sum {
   my $n = scalar(@_);
   my $sum = 0;
   foreach my $item (@_) {
      $sum += $item;
   }
   return ($sum);
}