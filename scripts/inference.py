#!/usr/bin/env python3

import pandas as pd
from flipflop import flipflop
import os
import sys
import joblib

import argparse

def main():
    parser = argparse.ArgumentParser(description='Run flipflop Bayesian inference.')
    parser.add_argument('datafile', type=str,
                        help='path to csv containing beta values')
    parser.add_argument('patientinfofile', type=str,
                        help='path to csv containing patientinfo')
    parser.add_argument('outputdir', type=str, default='~', 
                        help='path to folder in which to store output')
    parser.add_argument('sample', type=str,
                        help='samplename of beta array (must be a col in datafile index in patientinfo)')
    parser.add_argument('S', type=int,
                        help='stem cell number to evaluate')
    parser.add_argument('-nlive', default=1500, dest='nlive', type=int,
                        help='number of live points in dynesty sampler (default:1500)')
    parser.add_argument('--verbose', action='store_true', default=False, dest='verbose')
    parser.add_argument('-lamscale', default=1.0, type=float,
                        help='scale of replacement rate (default:1.0)')
    parser.add_argument('-muscale', default=0.05, type=float,
                        help='scale of methylation rate (default:0.05)')
    parser.add_argument('-gammascale', default=0.05, type=float,
                        help='scale of methylation rate (default:0.05)')

    # Execute the parse_args() method
    args = parser.parse_args()

    datafile = args.datafile
    patientinfofile = args.patientinfofile
    outputdir = args.outputdir
    sample = args.sample
    S = int(args.S)
    nlive = int(args.nlive)
    verbose = args.verbose
    lamscale=float(args.lamscale)
    muscale=float(args.muscale)
    gammascale=float(args.gammascale)

    outsamplesdir = os.path.join(outputdir, sample, 'posterior')
    outsamples = os.path.join(outsamplesdir, 'sample_{}.pkl'.format(S))

    os.makedirs(outsamplesdir, exist_ok=True)

    beta_values = pd.read_csv(datafile, index_col = 0)
    patientinfo = pd.read_csv(patientinfofile, keep_default_na=False, index_col = 0) 

    beta = beta_values[sample].dropna().values
    age = patientinfo.loc[sample, 'age']

    res = flipflop.run_inference(beta, age, S, nlive=nlive, 
                                verbose=verbose, lamscale=lamscale, 
                                muscale=muscale, gammascale=gammascale)

    with open(outsamples, 'wb') as f:
        joblib.dump(res, f)

if __name__ == "__main__":
    main()