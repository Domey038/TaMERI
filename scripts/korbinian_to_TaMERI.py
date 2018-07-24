#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
import argparse
import sys
import os
import pandas as pd
import re
import subprocess
from random import randint

#-----------------------------------------------------#
#                  Parse command line                 #
#-----------------------------------------------------#
#Implement a modified ArgumentParser from the argparse package
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message + "\n")
        self.print_help()
        sys.exit(2)
#Initialize the modifed argument parser
parser = MyParser(formatter_class=argparse.RawDescriptionHelpFormatter, add_help=False, description=
    """Korbinian results to TaMERI tsv converter.""")
#Add arguments for mutally exclusive required group
parser.add_argument('-k', '--korbinian', type=str, action='store', required=True, dest='args_korbinian',
                    help='Path to Korbinian summary directory')
parser.add_argument('-u', '--uniprot', type=str, action='store', required=True, dest='args_uniprot',
                    help='Path to a uniprot flat file')
parser.add_argument('-s', '--gsv', type=str, action='store', required=True, dest='args_gsv',
                    help='Path to directory of the external software: goslimviewer')
parser.add_argument('-o', '--output', type=str, action='store', required=True, dest='args_out',
                    help='Output path of the TaMERI tsv file')
#Parse arguments
args = parser.parse_args()

#-----------------------------------------------------#
#        Read a Uniprot file in flat file format      #
#-----------------------------------------------------#
def read_UniProt(pathUniProt):
    #initialize variables
    protein_list = []
    uniprot_id = None
    isTM = None
    goTerms = []
    openEntry = False
    #Start reading through the UniProt file
    with open(pathUniProt, 'r') as uniprotFILE:
        #Iterate over each line in the flat file
        for line in uniprotFILE:
            #Remove new line character
            if "\n" in line:
                line = line.rstrip("\n")
            #IF new entry started -> get Accession ID
            if line.startswith("AC") and not openEntry:
                patternAC = re.search('^AC\s+([a-zA-Z0-9]+);', line)
                uniprot_id = patternAC.group(1)
                openEntry = True
            #IF entry contains a alpha helical TM annotation -> switch isTM boolean tag
            elif re.match("FT\s+TRANSMEM.*Helical", line):
                isTM = True
            #IF entry contains a Gene Ontology annotation -> save
            elif re.match("DR\s+GO;\s.*", line):
                patternGO = re.search('^DR\s+GO;\s(GO:[0-9]+);', line)
                go_term = patternGO.group(1)
                goTerms.append(go_term)
            #IF entry ended
            elif line.startswith("//"):
                #IF protein is a alpha helical TM protein -> save it into cache
                if isTM:
                    uniprot_protein = (uniprot_id, goTerms)
                    protein_list.append(uniprot_protein)
                #clear variables
                uniprot_id = None
                isTM = False
                goTerms = []
                openEntry = False
    return protein_list

#-----------------------------------------------------#
#                  Run goslimviewer                   #
#-----------------------------------------------------#
def run_goslimviewer(protein_list):
    #Save and then change the current working directory into the goslimviewer directory
    original_wd = os.getcwd()
    os.chdir(args.args_gsv)
    #Dump protein_list into a temporary file
    random_integer = randint(0, sys.maxsize)
    path_tmp_input = str(random_integer) + "TaMERI_converter.go_list.TMP"
    path_tmp_output = str(random_integer) + "TaMERI_converter.results.TMP"
    with open(path_tmp_input, 'w') as go_writer:
        for protein in protein_list:
            uniprot_id = protein[0]
            goTerms = protein[1]
            for go_term in goTerms:
                go_writer.write(str(uniprot_id) + "\t" + str(go_term) + "\n")
    #Run goslimviewer
    out = subprocess.call(["perl", "goslimviewer_standalone.pl", "-i", path_tmp_input, "-s", "generic", "-o", path_tmp_output])
    #Read output into cache
    path_tmp_output_mapping = path_tmp_output + ".generic.s2p2g.txt"
    go_classification = {}
    with open(path_tmp_output_mapping, 'r') as goClassification_reader:
        header_line = next(goClassification_reader)
        #Iterate over each line in the results file
        for line in goClassification_reader:
            #Remove new line character
            if "\n" in line:
                line = line.rstrip("\n")
            #Split row into columns
            cols = line.split("\t")
            hierarchy = cols[0]
            go_term = cols[2]
            uniprot_id = cols[3]
            if not uniprot_id in go_classification:
                go_classification[uniprot_id] = {}
                go_classification[uniprot_id]["C"] = set()
                go_classification[uniprot_id]["F"] = set()
                go_classification[uniprot_id]["P"] = set()
            go_classification[uniprot_id][hierarchy].add(go_term)
    #Remove temporary files and change working directory to default again
    os.remove(path_tmp_input)
    os.remove(path_tmp_output + ".generic.s2p2g.txt")
    os.remove(path_tmp_output + ".generic.errors.txt")
    os.remove(path_tmp_output + ".generic.bp.txt")
    os.remove(path_tmp_output + ".generic.cc.txt")
    os.remove(path_tmp_output + ".generic.mf.txt")
    os.chdir(original_wd)
    #return results
    return go_classification

#-----------------------------------------------------#
#                    Runner code                      #
#-----------------------------------------------------#
#Identify list number
summary_path = os.path.normpath(args.args_korbinian)
summary_path_list = summary_path.split(os.sep)
list_number = summary_path_list[-1]

#Read cr_summary.csv file
path_cr_csv = os.path.join(args.args_korbinian, "List" + list_number + "_cr_summary.csv")
data_set = pd.read_csv(path_cr_csv, sep=",")
TaMERI_df = data_set[['protein_name', 'AAIMON_slope_all_TMDs_mean', 'number_of_TMDs']]
TaMERI_df = TaMERI_df.rename(columns={'protein_name': 'id', 'AAIMON_slope_all_TMDs_mean': 'ER_ratio',
                                     'number_of_TMDs': 'TM_regions'}, inplace=False)
# TaMERI_df = data_set[['protein_name', 'AAIMON_mean_all_TM_res', 'number_of_TMDs']]
# TaMERI_df = TaMERI_df.rename(columns={'protein_name': 'id', 'AAIMON_mean_all_TM_res': 'ER_ratio',
#                                      'number_of_TMDs': 'TM_regions'}, inplace=False)

#Read simple csv file
path_simple_csv = os.path.join(args.args_korbinian, "List" + list_number + ".csv")
data_set = pd.read_csv(path_simple_csv, sep=",", low_memory=False)
temporary_df = data_set[['protein_name', 'perc_TMD', 'seqlen']]
temporary_df = temporary_df.rename(columns={'protein_name': 'id', 'perc_TMD': 'TM_proportion',
                                            'seqlen': 'sequence_length'}, inplace=False)

#Merge the two panda data frames
TaMERI_df = TaMERI_df.merge(temporary_df, left_on='id', right_on='id', how='inner')

#Read uniprot file
protein_list = read_UniProt(args.args_uniprot)

#Run goslimviewer
go_classification = run_goslimviewer(protein_list)

#convert Gene Ontology classification from sets to lists
for uni_id in go_classification:
    for hierarchy in go_classification[uni_id]:
        go_classification[uni_id][hierarchy] = list(go_classification[uni_id][hierarchy])

#Merge gene ontology classification results with the TaMERI data frame
GO_df = pd.DataFrame.from_dict(go_classification, orient='index')
TaMERI_df = TaMERI_df.merge(GO_df, left_on='id', right_index=True, how='inner')

#Reorder the columns
cols = ['id', 'sequence_length', 'TM_regions', 'TM_proportion', 'C', 'F', 'P', 'ER_ratio']
TaMERI_df = TaMERI_df[cols]

#output
TaMERI_df.to_csv(args.args_out, sep="\t", index=False, header=True)
