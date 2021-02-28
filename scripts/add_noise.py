import pandas as pd
import numpy as np
from ticktockclock import ticktock
import argparse

parser = argparse.ArgumentParser(description='Simulate synthetic crypt')
parser.add_argument('inputfile', type=str, default='~', 
                    help='path to csv file containing "true" beta values')
parser.add_argument('outputfile', type=str, default='~', 
                    help='path to csv file in which to store output')
parser.add_argument('-delta', default=0.04, type=float, 
                    help='offset from zero') 
parser.add_argument('-eta', default=0.92, type=float, 
                    help='offset from one')   
parser.add_argument('-kappa', default=100, type=float, 
                    help='sample size of beta distribution (see https://en.wikipedia.org/wiki/Beta_distribution#Mean_and_sample_size)')   
parser.add_argument('--index', action='store_true', default=False, dest='index',
                    help='indicate whether the first column of the inputfile is the index of the csv (default False)')
# Execute the parse_args() method
args = parser.parse_args()

inputfile = args.inputfile
outputfile = args.outputfile
delta = args.delta
eta = args.eta
kappa = args.kappa
index = args.index

if index:
    # Load csv file as dataframe
    beta_true = pd.read_csv(inputfile, index_col=0)
else:
    beta_true = pd.read_csv(inputfile)

# Linear transform on beta to account for array saturating (e.g. shifts mean of
# lower peak from 0 to delta and upper peak from 1 to eta)
beta_rescale = ticktock.rescale_beta(beta_true, delta, eta)

# Apply noise model (for each true beta value, draw the measured beta
# value from a beta distribution with a mean equal to the true beta value
# and a sample size equal to kappa)
beta_sample = ticktock.beta_rvs(beta_rescale, kappa)

if index:
    beta = pd.DataFrame(beta_sample, columns=beta_true.columns, index=beta_true.index)
    beta.to_csv(outputfile)
else:
    beta = pd.DataFrame(beta_sample, columns=beta_true.columns)
    beta.to_csv(outputfile, index=False)