#
# ScriptName: goslimviewer_standalone.pl
# Author:  Cathy Gresham
# Date:  02/20/2014
#  **************************************************
# Desc:
# This script will use Gene Ontology (GO Slim files)
#   to slim GO ids from an input file
#  **************************************************
#
# Modification Log:
#   02/20/2014  v1.0 create script
#   02/24/2014  v1.1 add error output and trim input
#
#   03/28/2014  v2.0 Change the count of ids from   
#         slimmed unique GO ids to slimmed 
#           unique Accessions ids
#
#  **************************************************
#  Script arguments:
#    -i input file
#    -s slim set (generic,goa,pir,plant,tigr or yeast)
#    -o output prefix (optional)
#    -h  help with script arguments
#  **************************************************
#
#  **************************************************
#  Input file format 
# 
#  2 column tab delimited file
#      there can be more than 2 columns in the input
#      file but only the first 2 are processed
#
#    col1 - input_accession_id, col2 - GO_ID  (1 per line)
# Sample Input:
# A0JNB7	GO:0005381
# A0JNB7	GO:0006826
# A0JNB7	GO:0008021
# A0M8U2	GO:0004871
# A0M8U2	GO:0005576
# A2Q127	GO:0003746
# A2VDL1	GO:0003677
# A2VDL1	GO:0005515
# A2VDL1	GO:0005622
#  **************************************************
#
#  **************************************************
#  Output file format 
#     4 output files. 1 for each ontology domain
#     (biological_process, molecular_function and
#       cellular_component) and 1 file for detail 
#       overview).
# 1)  Sample domain (cc.txt, mf.txt, bp.txt) output.
#   contains the slim_id, slim_term_name and accession_count
#  e.g.
#  GO:0005575      cellular_component      257
#  GO:0005576      extracellular region    104
#
# 2) detail file 
#   GO_Type Slim_ID GO_Name Input_Accession Input_GOID
#   C       GO:0005575      cellular_component      A8AUG9  GO:0005581      collagen
#   C       GO:0005575      cellular_component      A8AVS2  GO:0016020      membrane
#   F       GO:0003674      molecular_function      A8AVS2  GO:0016787      hydrolase activity
#   F       GO:0003674      molecular_function      A8AWM6  GO:0005518      collagen binding
#   P       GO:0008150      biological_process      B3WLE9  GO:0008152      metabolic process
#   P       GO:0008150      biological_process      B3WLE9  GO:0009405      pathogenesis
#
#  **************************************************
 
use strict;
use warnings;

use File::stat;
use File::Basename;
use Getopt::Std;

use constant SLIMDATA_DIR => 'slimdata/';

our ($opt_i, $opt_s, $opt_h, $opt_o);
getopts('i:s:o:h'); 

##########################
# subroutine definitions
##########################
sub checkOpts;
sub readGOdef();
sub readTerm2slim();
sub readGOslim();
sub readInput();
sub generateOutput();
sub trimSpace($);

my ( $printhelp, %unq_gos, %go_def, %term2slim, %go_slim,%errors );

$printhelp = defined($opt_h);

&checkOpts;

%go_def = %term2slim = %go_slim = %unq_gos = %errors = ();
&readGOdef();

&readTerm2slim();

&readGOslim();

&readInput();

&generateOutput();


#################################################################
#
# generate_output
#
# Desc: generate the output files
#
#################################################################
sub generateOutput() { 
my ( $output_file, $slim_set,
    $detail_fh, $cc_fh, $mf_fh, $bp_fh, $err_fh,
    $cc_file, $mf_file, $bp_file, $detail_file, $err_file,
    %C, %F, %P, @c_detail, @p_detail, @f_detail, 
    $datafound, $datafound1, $datafound2, %seen_gouid
); 
  $err_file = $output_file = $detail_file = $cc_file = $mf_file = $bp_file = '';
  %C = %F = %P =  ();
  $datafound = $datafound1 = $datafound2 =  0;
   @c_detail = @p_detail = @f_detail = ();

 $slim_set=$opt_s;

 if (defined $opt_o && $opt_o ne '' and $opt_o ne ' ') { $output_file = $opt_o; }
 else {
     my ($path,$suffix );
     ($output_file,$path,$suffix) = fileparse($opt_i);
    if ($output_file =~ m/(.*)\.(.*)/) { $output_file = $1; }
 }

   $detail_file = $output_file .'.' .$slim_set . '.s2p2g.txt';
   $cc_file     = $output_file . '.' .$slim_set . '.cc.txt';
   $mf_file     = $output_file . '.' .$slim_set . '.mf.txt';
   $bp_file     = $output_file . '.' .$slim_set . '.bp.txt';
   $err_file     = $output_file . '.' .$slim_set . '.errors.txt';

  open($err_fh, ">",$err_file) || die "cannot open detail file $!\n"; 
   foreach my $e ( sort keys %errors) {
       my $uid = $errors{$e};
      print $err_fh "$e\t$uid\tInvalid GO\n";
   }
   undef(%errors);

  foreach my $goid (keys %unq_gos) {
     my ($gtype, $orig_gname, $slim_def_type, $slim_type, $gname, $slim_str, @slims,$slim_id, $uids_str);
     $gtype = $orig_gname = $slim_def_type = $slim_type = $gname = $slim_id = '';
     $uids_str = $unq_gos{$goid};
     if (exists $term2slim{$goid}) { 
        if (exists $go_def{$goid}{'go_type'})  {
              $gtype = $go_def{$goid}{'go_type'};
              $orig_gname = $go_def{$goid}{'name'};
        }
       else {
           print $err_fh "$goid\t$uids_str\tGO not found in ontology\n";
        } # no go_def found 
        $slim_str = $term2slim{$goid};
        @slims = ();
        @slims = split (/\;/,$slim_str);
        foreach my $slim_id (@slims) {
           if (exists ($go_def{$slim_id}{'go_type'}))  {
              $slim_def_type = $go_def{$slim_id}{'go_type'};
              $gname = $go_def{$slim_id}{'name'};
           }
           else {
               print $err_fh "$slim_id\t$goid -  $uids_str\tSlimmed GO not found in ontology\n";
            } # no go_def found 
           if (exists $go_slim{$slim_id}) { $slim_type = $go_slim{$slim_id}; }
           if (($gtype ne $slim_type) || ($gtype ne $slim_def_type)) {
                 my $uids_str = $unq_gos{$goid};
                 print $err_fh "$goid\t$uids_str\tGO and Slim Aspect mismatch\n";
                 next; 
           }
           # if ( (defined $gtype) && ($gtype ne ' ') && ($gtype ne '') ) {
                # if ($gtype eq 'C') { $C{$slim_id}++; }
                # if ($gtype eq 'F') { $F{$slim_id}++; }
                # if ($gtype eq 'P') { $P{$slim_id}++; }
           # }
           my $uids_str = $unq_gos{$goid};
           my @uids_arr = split(/\;/,$uids_str);
           foreach my $u (@uids_arr) {
             my $gstr = $slim_id . $u;
             if (exists $seen_gouid{$gstr}) { ; }
             else {
                $seen_gouid{$gstr}=undef;
                if ($gtype eq 'C') { $C{$slim_id}++; }
                if ($gtype eq 'F') { $F{$slim_id}++; }
                if ($gtype eq 'P') { $P{$slim_id}++; }
             }
               my $dline = ();
               $dline = { gtype => $gtype, slim => $slim_id, gname => $gname, uid => $u, goid => $goid, orig_gname => $orig_gname };
               if ($gtype eq 'C') { push (@c_detail,  $dline); }
               if ($gtype eq 'P') { push (@p_detail,  $dline); }
               if ($gtype eq 'F') { push (@f_detail,  $dline); }
        } # each uid associated with the go
     } # foreach slim associated with a go_id
   } # term2slim for each go exists
   else {
     if (exists $go_def{$goid}{'go_type'})  {
         my $uids_str = $unq_gos{$goid};
         print $err_fh "$goid\t$uids_str\tSlim Term not found for GO\n";
     } # go is valid just not slimmed
     else {
         my $uids_str = $unq_gos{$goid};
         print $err_fh "$goid\t$uids_str\tGO not found in ontology\n";
     } # go is not in ontology
   } # no term2slim found
 } # each goid from input

           #
           # Generate the output for the detail summary and aspect files 
           #
  open($detail_fh, ">",$detail_file) || die "cannot open detail file $!\n"; 
  open($cc_fh, ">",$cc_file) || die "cannot open cc file $!\n"; 
  open($mf_fh, ">",$mf_file) || die "cannot open mf file $!\n"; 
  open($bp_fh, ">",$bp_file) || die "cannot open bp file $!\n"; 
  
print $detail_fh "GO_Type\tSlim_ID\tGO_Name\tInput_Accession\tInput_GOID\n";
foreach my $id1 (sort keys %C){
  my $printDetail=0;
  my $hash_cnt = scalar (@c_detail);
  for (my $i=0; $i < $hash_cnt; $i++) {
     if ($c_detail[$i]{'slim'} eq $id1) {
        $datafound=1;
        if ($printDetail == 0) {
          print $cc_fh "$id1\t$c_detail[$i]{'gname'}\t$C{$id1}\n";
          $printDetail++;
        }
        print $detail_fh "$c_detail[$i]{'gtype'}\t$c_detail[$i]{'slim'}\t$c_detail[$i]{'gname'}\t$c_detail[$i]{'uid'}\t$c_detail[$i]{'goid'}\t$c_detail[$i]{'orig_gname'}\n";
     } # detail  matches the slimmed id  
  } # foreach detail record
} # end of C Hash
undef(@c_detail);
undef (%C);

foreach my $id1 (sort keys %F){
  my $printDetail=0;
  my $hash_cnt = scalar (@f_detail);
  for (my $i=0; $i < $hash_cnt; $i++) {
     if ($f_detail[$i]{'slim'} eq $id1) {
        $datafound1=1;
        if ($printDetail == 0) {
          print $mf_fh "$id1\t$f_detail[$i]{'gname'}\t$F{$id1}\n";
          $printDetail++;
        }
        print $detail_fh "$f_detail[$i]{'gtype'}\t$f_detail[$i]{'slim'}\t$f_detail[$i]{'gname'}\t$f_detail[$i]{'uid'}\t$f_detail[$i]{'goid'}\t$f_detail[$i]{'orig_gname'}\n";
     }
  }
} 
undef(@f_detail);
undef (%F);

foreach my $id1 (sort keys %P){
  my $printDetail=0;
  my $hash_cnt = scalar (@p_detail);
  for (my $i=0; $i < $hash_cnt; $i++) {
     if ($p_detail[$i]{'slim'} eq $id1) {
        $datafound2=1;
        if ($printDetail == 0) {
           print $bp_fh "$id1\t$p_detail[$i]{'gname'}\t$P{$id1}\n";
          $printDetail++;
        }
        print $detail_fh "$p_detail[$i]{'gtype'}\t$p_detail[$i]{'slim'}\t$p_detail[$i]{'gname'}\t$p_detail[$i]{'uid'}\t$p_detail[$i]{'goid'}\t$p_detail[$i]{'orig_gname'}\n";
     }
  }
}
undef(%P);
undef(@p_detail);

if (!$datafound) { print $cc_fh "No data found"; }
if (!$datafound1) { print $mf_fh "No data found"; }
if (!$datafound2) { print $bp_fh "No data found"; }
if ((!$datafound) && (!$datafound1) && (!$datafound2) ) {
        print $detail_fh "No data found\n";
} 


close($err_fh);
close($cc_fh);
close($mf_fh);
close($bp_fh);
close($detail_fh);

} # end of generate output 


#################################################################
#
# read_input
#
# Desc: this subroutine will read the input flat file into hash
#
#################################################################
sub readInput() { 
   my ($in_fh, $in_file,$temp_fh,$temp_file,%seen_gouid, $gstr );
      $gstr = '';
      %seen_gouid = %unq_gos = (); 
      %errors=();
   $in_file = $opt_i;
   $temp_file = $in_file . 'temp';

       #
       # some text editors and Macs do not have end of lines w/ just lf. correct
       # 
   open ($in_fh, "<", $in_file) or die "cannot open < input $in_file : $!";
   open ($temp_fh, ">", $temp_file) or die "cannot open temp input $temp_file : $!";
   while (my $line = <$in_fh> ) {
       $line =~ s/\r\n/\n/g;
       $line =~ s/\r/\n/g;
        print $temp_fh $line;
   }
   close $in_fh;
   close $temp_fh;

 open($in_fh, "<$temp_file") or die "$!";
 while (my $line= <$in_fh>) {
	chomp($line);
	$line =~ s/(\n|\r)//g;
	my ($uid,$goid_str, $rest) = split(/\t/,$line,3);
    $uid  = trimSpace($uid);
     my @go_arr = split(/[,\|;]/,$goid_str);
     foreach my $goid (@go_arr) {
        $goid = trimSpace($goid);
        if ((!defined $goid) || ($goid !~ m/GO:\d{7,15}/)) { $errors{$goid} = $line; next; }

        if (exists $unq_gos{$goid}) { ; }
        else { $unq_gos{$goid} = undef; }
        
          $gstr = $goid . $uid;
          if (exists $seen_gouid{$gstr}) { ; }
          else {
              $seen_gouid{$gstr}=undef;
              my $existing_key = $unq_gos{$goid};
              if (defined $existing_key && $existing_key ne '') {
                 $unq_gos{$goid} = $existing_key . ';' . $uid;
              }
              else { $unq_gos{$goid} = $uid;  }
        } # have not seen the go_id and uid yet.
  } # foreach multiple GO line
} # foreach input line
 close $in_fh;

 unlink($temp_file);
 undef(%seen_gouid);

}   

#################################################################
#
# readGOslim
#
# Desc: this subroutine will read go_slim flat file into hash
#
#################################################################
sub readGOslim() { 
   my ($in_fh, $in_file,$slimset);
         %go_slim=();
   $slimset = $in_file = '';
   $slimset= $opt_s;
 
   $in_file = SLIMDATA_DIR . 'go_slim_' . $slimset . '.tsv';
   open ($in_fh, "<", $in_file) or die "cannot open go_slim $in_file : $!";
   while (my $line = <$in_fh>) {
      chomp($line);
      my ($go_id, $go_type );
      $go_id = $go_type = '';
      ($go_id, $go_type) = split(/\t/,$line,2);
      $go_slim{$go_id}=$go_type;
   }
   close $in_fh;
}  # end of read_go_slim   

#################################################################
#
# read_term2slim
#
# Desc: this subroutine will read term2slim flat file into hash
#
#################################################################
sub readTerm2slim() { 
   my ($in_fh, $in_file, $slimset);
         %term2slim=();
     $slimset = $in_file = '';
   $slimset= $opt_s;

   $in_file = SLIMDATA_DIR . 'term2slim_' . $slimset . '.tsv';
   open ($in_fh, "<", $in_file) or die "cannot open term2slim $in_file : $!";
   while (my $line = <$in_fh>) {
      chomp($line);
      my ($go_id, $slim_id );
      $go_id = $slim_id = '';
      ($go_id, $slim_id) = split(/\t/,$line,2);
      if (exists $term2slim{$go_id}) {
        my $existing_key = $term2slim{$go_id};
        if (defined $existing_key && $existing_key ne '') {
            $term2slim{$go_id} = $existing_key . ';' . $slim_id;
        }
        else { $term2slim{$go_id} = $slim_id;  }
     }
     else { $term2slim{$go_id} = $slim_id;  }
   }
   close $in_fh;
} #end of read_term2slim   
 
#################################################################
#
# readGOdef
#
# Desc: this subroutine will read go_def flat file into hash
#
#################################################################
sub readGOdef() { 
   my ($in_fh, $in_file);
       %go_def=();

   $in_file = SLIMDATA_DIR . 'godef.tsv'; 
   open ($in_fh, "<", $in_file) or die "cannot open godef $in_file : $!";
   while (my $line = <$in_fh>) {
      chomp($line);
      my ($go_id, $go_type, $go_name);
      $go_id = $go_type =  $go_name = '';
      ($go_id, $go_type,$go_name) = split(/\t/,$line,3);
      $go_def{$go_id}{'go_type'}=$go_type;
      $go_def{$go_id}{'name'}=$go_name;
   }
   close $in_fh;
}  # end read_godef
  
#################################################################
#
# checkOpts
#
# Desc: this subroutine will read in user supplied options
#
#################################################################
sub checkOpts {
  if ($printhelp) {
     print STDERR <<END;
Usage:  perl $0 [-h] -i input_text_file -s slim_dataset(generic,goa,pir,plant,tigr,yeast) [-o output_file_prefix]

Required parameters:
        -i input text file (must be input_id\tGO_ID)
        -s slim_dataset. Must be generic,goa,pir,plant,tigr or yeast

Optional parameters:
    -o  output_file_prefix. 
            There are 4 output files generated ending with cc.txt, mf.txt, bp.txt and s2p2g.txt
            If this parameter is not provided then the output filenames will begin with input_file_name
    -h displays this message
                
Examples:
        % perl $0 -i go_slim_input.txt -s yeast

    Print Help message
        % perl $0 -h
END
    exit;
  }

  my %valid_sets = (generic => 1,goa => 1,pir => 1,tigr => 1,plant => 1,yeast => 1, metagenomics => 1);
  my ($term2slim_file, $go_def_file, $goslim_file,$st,$mtime,$age, $goslim_set, $currDate);
  $term2slim_file = $go_def_file = $goslim_file = $goslim_set = '';
  $st = $age = $mtime = '';

 $currDate = time();

 if (!$opt_i) {
   die "Input filename must be provided.\nExiting now.\n\n";
 }
 if (!-f $opt_i) { die "Input filename $opt_i must exist.\nExiting now.\n\n"; }
 if (-z $opt_i) { die "Input filename $opt_i contains no records.\nExiting now.\n\n"; }
 if (!-r $opt_i) { die "Input filename $opt_i cannot be read.\nExiting now.\n\n"; }

 if (!$opt_s) {
   die "slim dataset must be provided.\n It must be generic, goa, pir, plant, tigr or yeast. Exiting now.\n\n";
 }
 if (not exists $valid_sets{$opt_s}) {
   die "slim dataset must be provided.\n It must be generic, goa, pir, plant, tigr or yeast. Exiting now.\n\n";
 }
 $goslim_set = $opt_s;

 $term2slim_file = SLIMDATA_DIR . 'term2slim_' . $goslim_set . '.tsv';
  if (!-f $term2slim_file) { die "file $term2slim_file must exist.\nExiting now.\n\n"; }
  elsif (-z $term2slim_file) { die "file $term2slim_file contains no records.\nExiting now.\n\n"; }
  elsif (!-r $term2slim_file) { die "file $term2slim_file cannot be read.\nExiting now.\n\n"; }
   $st = stat($term2slim_file) or die "Cannot stat $term2slim_file: $!";
   $mtime = $st->mtime;
   $age = ($currDate - $mtime) / 86400; # convert seconds to days
  if ($age > 30) { print STDERR "file $term2slim_file is more than 30 days old.  Might want to consider ftping new file\n"; }

 $go_def_file = SLIMDATA_DIR . 'godef.tsv'; 
  if (!-f $go_def_file) { die "file $go_def_file must exist.\nExiting now.\n\n"; }
  elsif (-z $go_def_file) { die "file $go_def_file contains no records.\nExiting now.\n\n"; }
  elsif (!-r $go_def_file) { die "file $go_def_file cannot be read.\nExiting now.\n\n"; }
   $st = stat($go_def_file) or die "Cannot stat $go_def_file: $!";
   $mtime = $st->mtime;
   $age = ($currDate - $mtime) / 86400; # convert seconds to days
  if ($age > 30) { print STDERR "file $go_def_file is more than 30 days old.  Might want to consider ftping new file\n"; }

 $goslim_file = SLIMDATA_DIR . 'go_slim_' . $goslim_set . '.tsv';
  if (!-f $goslim_file) { die "file $goslim_file must exist.\nExiting now.\n\n"; }
  elsif (-z $goslim_file) { die "file $goslim_file contains no records.\nExiting now.\n\n"; }
  elsif (!-r $goslim_file) { die "file $goslim_file cannot be read.\nExiting now.\n\n"; }
   $st = stat($goslim_file) or die "Cannot stat $goslim_file: $!";
   $mtime = $st->mtime;
   $age = ($currDate - $mtime) / 86400; # convert seconds to days
  if ($age > 30) { print STDERR "file $goslim_file is more than 30 days old.  Might want to consider ftping new file\n"; }


} #end of checkOpts
                 #############################
                 ##  trim_whitespace        ##
                 ##  Returns trimmed string ##
                 #############################
sub trimSpace($){
   my $str = shift;

   if (defined $str && $str ne '' && $str ne ' ') {
     $str =~ s/^\s+//g; #remove leading spaces
     $str =~ s/\s+$//g; #remove trailing spaces
  }
  else { $str = ''; }

  return $str;
}

__END__
