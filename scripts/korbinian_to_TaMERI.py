#!/usr/bin/env python
# -*- coding: utf-8 -*-


#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
import argparse
import sys
import os
import pandas as pd

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
parser.add_argument('-i', '--input', type=str, action='store', required=True, dest='args_in',
                    help='Path to Korbinian summary directory')
parser.add_argument('-o', '--output', type=str, action='store', required=True, dest='args_out',
                    help='Output path of the TaMERI tsv file')
#Parse arguments
args = parser.parse_args()

#-----------------------------------------------------#
#                    Runner code                      #
#-----------------------------------------------------#
#Identify list number
summary_path = os.path.normpath(args.args_in)
summary_path_list = summary_path.split(os.sep)
list_number = summary_path_list[-1]

#Read cr_summary.csv file
path_cr_csv = os.path.join(args.args_in, "List" + list_number + "_cr_summary.csv")
data_set = pd.read_csv(path_cr_csv, sep=",")
TaMERI_df = data_set[['protein_name', 'AAIMON_slope_all_TMDs_mean', 'number_of_TMDs']]
TaMERI_df = TaMERI_df.rename(columns={'protein_name': 'id', 'AAIMON_slope_all_TMDs_mean': 'AAIMON_slope',
                                      'number_of_TMDs': 'TM_regions'}, inplace=False)

#Read simple csv file
path_simple_csv = os.path.join(args.args_in, "List" + list_number + ".csv")
data_set = pd.read_csv(path_simple_csv, sep=",", low_memory=False)
temporary_df = data_set[['protein_name', 'perc_TMD', 'seqlen']]
temporary_df = temporary_df.rename(columns={'protein_name': 'id', 'perc_TMD': 'TM_proportion',
                                            'seqlen': 'sequence_length'}, inplace=False)

#Merge the two panda data frames
TaMERI_df = TaMERI_df.merge(temporary_df, left_on='id', right_on='id', how='inner')

#Reorder the columns
cols = ['id', 'sequence_length', 'TM_regions', 'TM_proportion', 'AAIMON_slope']
TaMERI_df = TaMERI_df[cols]

#output
TaMERI_df.to_csv(args.args_out, sep="\t", index=False, header=True)
