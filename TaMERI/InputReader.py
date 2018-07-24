#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
import pandas as pd
import re

#-----------------------------------------------------#
#      Read a data set in TaMERI-input.tsv format     #
#-----------------------------------------------------#
def read_TaMERI_tsv(path):
    #Read the tab seperated vector table (TSV) via Numpy
    data_set = pd.read_csv(path, sep="\t")
    #Assign protein ids as index for each row
    #data_set = data_set.set_index('id')
    data_set = data_set.drop('id', axis=1)
    #convert gene ontology terms into lists (instead of default strings)
    data_set = data_set.assign(F=data_set.F.str.strip('[]').str.split(','))
    data_set = data_set.assign(C=data_set.C.str.strip('[]').str.split(','))
    data_set = data_set.assign(P=data_set.P.str.strip('[]').str.split(','))
    #return input data set
    return data_set

def read_r4s_tsv(path):
    #Read the tab seperated vector table (TSV) via Numpy
    data_set = pd.read_csv(path, sep="\t")
    #Temporary remove protein names
    #TODO: save them and add them later to the corresponding prediction output
    data_set = data_set.drop(['id', 'AAIMON_slope'], axis=1)
    data_set = data_set.rename(columns={'corr': 'ER_ratio'})
    return data_set

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
#                   Read a Test set                   #
#-----------------------------------------------------#
def read_TestSet(path):
    #Read the tab seperated vector table (TSV) via Numpy
    data_set = pd.read_csv(path, names = ["mpg", "cylinders", "displacement", "horsepower", "weight",
                                                "acceleration", "model_year", "origin", "car_name"], sep=r"\s+")
    data_set = data_set.drop('car_name', axis=1)
    return data_set
