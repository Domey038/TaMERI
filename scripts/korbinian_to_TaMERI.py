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
    kwString = ""
    binding_sites = 0
    np_binding = 0
    glyo = 0
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
            #IF entry contains uniprot keywords -> save
            elif re.match("^KW\s+.*", line):
                patternKW = re.search('^KW\s+(.*)', line)
                kwString = kwString + patternKW.group(1)
            #IF entry contains any functional site annotations -> save
            elif re.match("FT\s+CARBOHYD\s+.*", line):
                glyo += 1
            elif re.match("FT\s+NP_BIND\s+.*", line):
                np_binding += 1
            elif re.match("FT\s+BINDING\s+.*", line):
                binding_sites += 1
            #IF entry ended
            elif line.startswith("//"):
                #IF protein is a alpha helical TM protein -> save it into cache
                if isTM:
                    #process uniprot keywords into a list
                    kwString = kwString[:-1]
                    kwString = re.sub('\s?\{.*\}', '', kwString)
                    kwTerms = re.split(";\s?", kwString)
                    #save into protein_list cache
                    uniprot_protein = (uniprot_id, goTerms, binding_sites, np_binding, glyo, kwTerms)
                    protein_list.append(uniprot_protein)
                #clear variables
                uniprot_id = None
                isTM = False
                goTerms = []
                kwString = ""
                openEntry = False
                binding_sites = 0
                np_binding = 0
                glyo = 0
    return protein_list

#-----------------------------------------------------#
#        Extract and parse UniProt information        #
#-----------------------------------------------------#
def extract_UniProt_information(protein_list):
    #initialize panda data frame
    df = pd.DataFrame()
    #iterate over each protein
    for protein_tuple in protein_list:
        #extract information
        uniprot_id = protein_tuple[0]
        counter_bs = protein_tuple[2]
        counter_nbs = protein_tuple[3]
        counter_gy = protein_tuple[4]
        kw_terms = protein_tuple[5]
        #Add protein to dataframe
        df = df.append({'id': uniprot_id,
                        'binding_sites_number': counter_bs,
                        'nucleotide_bs_number': counter_nbs,
                        'Glyco_number': counter_gy,
                        'uniprot_KWs': kw_terms}, ignore_index=True)
    return df

#-----------------------------------------------------#
#                  Run goslimviewer                   #
#-----------------------------------------------------#
def run_goslimviewer(protein_list, slim_set):
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
    out = subprocess.call(["perl", "goslimviewer_standalone.pl", "-i", path_tmp_input, "-s", slim_set, "-o", path_tmp_output])
    #Read output into cache
    path_tmp_output_mapping = path_tmp_output + "." + slim_set + ".s2p2g.txt"
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
    os.remove(path_tmp_output + "." + slim_set + ".s2p2g.txt")
    os.remove(path_tmp_output + "." + slim_set + ".errors.txt")
    os.remove(path_tmp_output + "." + slim_set + ".bp.txt")
    os.remove(path_tmp_output + "." + slim_set + ".cc.txt")
    os.remove(path_tmp_output + "." + slim_set + ".mf.txt")
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
# TaMERI_df = data_set[['protein_name', 'AAIMON_slope_all_TMDs_mean', 'number_of_TMDs', 'AAIMON_n_homol',
#                   'TM01_SW_q_gaps_per_q_residue_mean', 'obs_changes_mean']]
TaMERI_df = TaMERI_df.rename(columns={'protein_name': 'id', 'AAIMON_slope_all_TMDs_mean': 'ER_ratio',
                                     'number_of_TMDs': 'TM_regions'}, inplace=False)
# TaMERI_df = data_set[['protein_name', 'AAIMON_mean_all_TM_res', 'number_of_TMDs']]
# TaMERI_df = TaMERI_df.rename(columns={'protein_name': 'id', 'AAIMON_mean_all_TM_res': 'ER_ratio',
#                                      'number_of_TMDs': 'TM_regions'}, inplace=False)

#Read simple csv file
path_simple_csv = os.path.join(args.args_korbinian, "List" + list_number + ".csv")
data_set = pd.read_csv(path_simple_csv, sep=",", low_memory=False)
useful_cols = ["protein_name", "multipass", "number_of_SP", "seqlen",
               "singlepass", "typeI", "typeII", "TM01_start",
               "perc_TMD", "len_TMD_mean", "TM01_lipo",
               "lipo_mean_all_TM_res", "lipo_last_TMD",
               "Cell_membrane", "Endoplasmic_reticulum", "Golgi_apparatus",
               "GPCR", "olfactory_receptor"]
korbinian_df = data_set[useful_cols]
korbinian_df = korbinian_df.rename(columns={'protein_name': 'id', 'perc_TMD': 'TM_proportion',
                                            'seqlen': 'sequence_length'}, inplace=False)

#Merge the two panda data frames
TaMERI_df = TaMERI_df.merge(korbinian_df, left_on='id', right_on='id', how='inner')

#Read uniprot file
protein_list = read_UniProt(args.args_uniprot)

#Extract binding sites etc information out of protein_list
uniprot_df = extract_UniProt_information(protein_list)

#Merge uniprot information results with the TaMERI data frame
TaMERI_df = TaMERI_df.merge(uniprot_df, left_on='id', right_on='id', how='inner')

#Run goslimviewer
# slim set can be "generic", "metagenomics", "goa", "panther", "pir", "plant", "tigr", "yeast"
# check gene ontology documentation for slim sets to get detailed information about the slim set content for each
slim_set = "metagenomics"
go_classification = run_goslimviewer(protein_list, slim_set)

#convert Gene Ontology classification from sets to lists
for uni_id in go_classification:
    for hierarchy in go_classification[uni_id]:
        go_classification[uni_id][hierarchy] = list(go_classification[uni_id][hierarchy])

#Merge gene ontology classification results with the TaMERI data frame
GO_df = pd.DataFrame.from_dict(go_classification, orient='index')
TaMERI_df = TaMERI_df.merge(GO_df, left_on='id', right_index=True, how='inner')

#Reorder the columns
#cols = ['id', 'sequence_length', 'TM_regions', 'TM_proportion', 'C', 'F', 'P', 'ER_ratio']
#TaMERI_df = TaMERI_df[cols]

#output
TaMERI_df.to_csv(args.args_out, sep="\t", index=False, header=True)
