
-------------------------
 goslimviewer_standalone
-------------------------
goslimviewer_standalone.pl is a standalone script  that provides a high
level summary of GO functions for a dataset.

The output can be charted in Excel to obtain publication quality figures. 
Note that records without annotation are not analyzed by GOSlimViewer.

This tool relies on Gene Ontology GO ontology, slim sets and 1 slim set from TIGR.

Note that the TIGR and the GOA slim sets are no longer actively maintained.
  GOA was last updated Nov. 2002.  
  TIGR was last updated Aug. 2009

More information about the tool can be found at 
http://www.biomedcentral.com/1471-2164/7/229

This tool was written in Perl therefore it should run
on systems that support Perl.

There is also a web based version of this tool available 
at http://agbase.hpc.msstate.edu/cgi-bin/tools/goslimviewer_select.pl


I   -  Requirements and setup for goslimviewer_standalone

II  -  How to run the script

III -  Computational requirements for goslimviewer_standalone

IV  -  Script Input

V   -  Script Output

VI  -  Software use disclaimer

-------------------------------------
I - Requirements and setup for goslimviewer_standalone
-------------------------------------

I - 1) Requirements 

     The goslimviewer_standalone tool is a Perl script.

     Therefore the system must have Perl installed.
 
        a) Perl
           Specific Perl packages include (these should be standard packages):
         		File::stat;
            File::Basename;
 		        Getopt::Std;

        b) slim sets and gene_ontology obo data

           Included in the zip for this tool will be a slimdata directory.
           This directory includes files for each slim_set and a go_def file 

           The default location should be in a subdirectory called slimdata/
           that exists in the directory where the perl script is placed.

           You can override this default location by editing the program and 
           changing the constant SLIMDATA_DIR
        
           To keep the data updated you can always redownload the data from AgBase.
          
           The files on AgBase should be updated weekly.

           If the data file is older than 30 days then the script will 
           remind you that you might want to download a new version of this file.

           You can download the goslimviewer_standalone standalone zip file from 
           http://agbase.hpc.msstate.edu/cgi-bin/tools/goslimviewer_select.pl
    

I - 2) Setup

        ----------------------------
        Download the following files:
        ----------------------------
        a) goslimviewer_standalone.zip

           This file can be downloaded from 
           http://agbase.hpc.msstate.edu/cgi-bin/tools/goslimviewer_select.pl

           The zip file will contain:
            goslimviewer_README.txt
            goslimviewer_standalone.pl
            slimdata/godef.tsv
            slimdata/go_slim_generic.tsv
            slimdata/go_slim_goa.tsv
            slimdata/go_slim_pir.tsv
            slimdata/go_slim_plant.tsv
            slimdata/go_slim_tigr.tsv
            slimdata/go_slim_yeast.tsv
            slimdata/go_slim_metagenomics.tsv
            slimdata/go_slim_panther.tsv
            slimdata/term2slim_generic.tsv
            slimdata/term2slim_goa.tsv
            slimdata/term2slim_pir.tsv
            slimdata/term2slim_plant.tsv
            slimdata/term2slim_tigr.tsv
            slimdata/term2slim_yeast.tsv
            slimdata/term2slim_metagenomics.tsv
            slimdata/term2slim_panther.tsv

         unzip the file in a location you want to run the script.


---------------------------------------------
II  -  how to run the script
---------------------------------------------

Usage:  perl goslimviewer_standalone.pl [-h] -i input_text_file -s slim_dataset(generic,metagenomics,panther,goa,pir,plant,tigr,yeast) [-o output_file_prefix]

Required parameters:
        -i input text file (must be input_id\tGO_ID)
        -s slim_dataset. Must be generic,metagenomics,panther,goa,pir,plant,tigr or yeast

Optional parameters:
    -o  output_file_prefix.
            There are 5 output files generated ending with 
               the slimset_selected plus the extensions of 
                    cc.txt, mf.txt, bp.txt,s2p2g.txt, errors.txt
            If the output parameter is not provided then the output filenames 
               will begin with input_file_name

    -h displays this message

Example:
        % perl goslimviewer_standalone.pl -i go_slim_input.txt -s yeast

    Print Help message
        % perl goslimviewer_standalone.pl -h

------------------------
Script Validation Checks:
--------------------------
   This tool will validate that an input_file and go_slim set is provided.

   The script requires that the input file have at least 2 columns.
   The first column is an input_accession_id and the second column as a GO ID.  
   The GO_ID must be a valid GO_ID format (GO:\d{7}).   Only 1 GO_ID is allowed per line.
   


---------------------------------------------
III -  Computational requirements for GOanna
---------------------------------------------
This tool should not be computationally intensive.  


---------------------------------------------
IV  -  Script Input
---------------------------------------------

The input file need to be a tab-delimited text file.

Two columns are required.
  column 1 - input accession id
  column 2 - GO id

There can be more than 2 columns in the input file but only the
first 2 are read.   

The GO ids need to be 1 GO id per line

Any records that do not appear to have a valid GO are ignored.
Any records where slim data is not found are ignored.

 ---------------------
  Sample input lines
 ---------------------
 A0JNB7	GO:0005381
 A0JNB7	GO:0006826
 A0JNB7	GO:0008021
 A0M8U2	GO:0004871
 A0M8U2	GO:0005576
 A2Q127	GO:0003746
 A2VDL1	GO:0003677
 A2VDL1	GO:0005515
 A2VDL1	GO:0005622


---------------------------------------------
V   -  Script Output 
--------------------------------------------
There will be four (5) output files from the script.
   1) Detail output file (ends in s2p2g.txt )
     It outputs each slimmed GO_id input_accession 

    	The format of the output is:
	    GO_type, Slim_id, Slim_GO_Name, Input_accession, Input_GO, Input_GO_Name

    	A tab is used to delimit the fields. 

   2) cellular component summary file (ends in cc.txt) 
    	The format of the output is:
    	Slimmed_GO, Slimmed_GO_Name, Count_of_unique_input_accessions

	    A tab is used to delimit the fields. 

   3) molecular function summary file (ends in mf.txt) 
    	The format of the output is:
    	Slimmed_GO, Slimmed_GO_Name, Count_of_unique_input_accessions

	    A tab is used to delimit the fields. 

   4) biological process file (ends in bp.txt) 
    	The format of the output is:
    	Slimmed_GO, Slimmed_GO_Name, Count_of_unique_input_accessions

	    A tab is used to delimit the fields. 

   5) errors.txt
     Should output records where the 2nd column is not a GO id
        where the Slim term is not found, GO is not in ontology, etc
 ---------------------
  Sample output lines
 ---------------------
 GO domain summary data: 
  GO:0005575      cellular_component      257
  GO:0005576      extracellular region    104

 detail file:
   GO_Type Slim_ID GO_Name Input_Accession Input_GOID
   C       GO:0005575      cellular_component      A8AUG9  GO:0005581      collagen
   C       GO:0005575      cellular_component      A8AVS2  GO:0016020      membrane

 errors file:
  GO:9999999  Acc1234 GO not found in ontology
  GO8888888 Invalid GO


---------------------------------------------
VI   -  Software use disclaimer
--------------------------------------------

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

