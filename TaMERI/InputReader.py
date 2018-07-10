#-----------------------------------------------------#
#                   Library imports                   #
#-----------------------------------------------------#
import pandas as pd

#-----------------------------------------------------#
#                   Read a Test set                   #
#-----------------------------------------------------#
def read_TestSet(path):
    #Read the tab seperated vector table (TSV) via Numpy
    data_set = pd.read_csv(path, names = ["mpg", "cylinders", "displacement", "horsepower", "weight",
                                                "acceleration", "model_year", "origin", "car_name"], sep=r"\s+")
    return data_set
