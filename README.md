# TaMERI

Prediction of 'TrAnsMembrane Evolutionary Rate Influence' (TaMERI) via Machine learning algorithm (Neural Networks + Random Forest)

## Prerequisites

Python (version >= 3.5), Korbinian and a UniProt flat file containing transmembrane proteins

R with the libraries: ['data.table', 'magrittr', 'tidyr', 'ggplot2', 'stringr']

Perl

### Installing

Run the setup.py python script to install all required module dependencies.
> python setup.py install

Perl and R with all required modules (only 'stringr' isn't a default library) have to be manually installed

## Execution

The TaMERI execution requires a specific modi (training | prediction | validation) and the path to the data set.
Optionally you can specify the used machine learning algorithm (Neural_Network | Random_Forest)
Have a look at the help manual for a more detailed list of all commands
> python TaMERI/Main.py -h


The training process to identify the best parameters can be run with the following command:
> python TaMERI/Main.py -t data/TaMERI.homo_sapiens.tsv -c

The 't' argument represents the training modus with the 'c' argument for calibration which result into training hundreds of models with different parameters and choosing the best.

The validation process to automatically run a 5-fold cross-validation, calculate MAE+MVS+R2 values and create plots for better evaluation through the Rscript 'scripts/evaluate_Validation.R'.
> python TaMERI/Mainy.py -v data/TaMERI.homo_sapiens.tsv

## Author

Dominik Müller

Email: ga37xiy@tum.de

Dmitrij Frishman lab - Department of Genome-Oriented Bioinformatics

Technical University of Munich

## License

This project is licensed under the MIT License
