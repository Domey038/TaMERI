#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
import pandas as pd

#-----------------------------------------------------#
#      Read a data set in TaMERI-input.tsv format     #
#-----------------------------------------------------#
def read_TaMERI_tsv(path):
    #Read the tab seperated vector table (TSV) via Numpy
    data_set = pd.read_csv(path, sep="\t")
    #Temporary remove protein names
    #TODO: save them and add them later to the corresponding prediction output
    data_set = data_set.drop('id', axis=1)
    return data_set

#-----------------------------------------------------#
#                   Read a Test set                   #
#-----------------------------------------------------#
def read_TestSet(path):
    #Read the tab seperated vector table (TSV) via Numpy
    data_set = pd.read_csv(path, names = ["mpg", "cylinders", "displacement", "horsepower", "weight",
                                                "acceleration", "model_year", "origin", "car_name"], sep=r"\s+")
    data_set = data_set.drop('car_name', axis=1)
    return data_set
