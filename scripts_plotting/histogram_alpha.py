############################################################
# Script to plot the range of alpha in the CMP routines
# Process: aggregation
# use conda env: iacpy3_2020
# 2021 09 22
# author: Sina Klampt
############################################################

# packages
import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
import warnings

# ignore runtime warning
warnings.simplefilter(action = "ignore", category = RuntimeWarning)


run_nr = 1
run_nr_diff = 2

# source file
d1  = Dataset('source_location'.format(run_nr_diff)+'source_file'.format(run_nr_diff)+'.nc')

run_name = ['12_all', '12_0-300', '12_0-100', '12_40-70']

for i in range(len(run_name)):
    var = 'DIAG01' # name of diagnostics

    fig, ax = plt.subplots(nrows=1, ncols=1)

    # collapse 3D array into 1D array
    d2 = d1[var][:,:,:].ravel()
    for j in range(len(d2)):
        if d2[j] == 0:
            d2[j] = np.nan

    # create histogram plots for different ranges
    if run_name[i] == '12_all':
        plt.hist(d2, label='december')
    elif run_name[i] == '12_0-300':
        b = np.arange(0, 300, 5)
        plt.hist(d2, bins=b, label='december')
    elif run_name[i] == '12_0-100':
        b = np.arange(0, 100, 2)
        plt.hist(d2, bins=b, label='december')
    elif run_name[i] == '12_40-70':
        b = np.arange(40, 70, 0.5)
        plt.hist(d2, bins=b, label='december')
    
    # rename variable, for easier understanding in plot
    var = 'alpha'

    # plotting
    plot_name= 'frequency_{}_{}'.format(var, run_name[i])
    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    ax.set_ylabel('frequency')
    ax.set_xlabel(var)

    plt.savefig('destination_location'+'/plot_{}.pdf'.format(plot_name), bbox_inches='tight')