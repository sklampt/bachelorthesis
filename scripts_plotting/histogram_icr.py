# Plotting
import matplotlib.pyplot as plt
import matplotlib as matplotlib
import seaborn as sns
import numpy as np
# netCDF
from netCDF4 import Dataset
import xarray as xr

### runs that are plotted
run_name = ['01_log_big', '01_log_small']

for i in range(len(run_name)):
    run_nr_diff = 2

    # Opening netCDF files
    d1  = Dataset('/net/n2o/wolke_scratch/sklampt/echam/test793_taylor_ws/test793_taylor/'.format(run_nr_diff)+'test793_taylor_year_200301.01_activ'.format(run_nr_diff)+'.nc')

    var = 'DIAG01_2'
    fig, ax = plt.subplots(nrows=1, ncols=1)

    if run_name[i] == '01_log_big':
        plt.hist(d1[var][:,:,:].flatten(), bins=[1e-7, 1e-6, 1e-5, 0.1, 0.9, 0.99, 1.], label='january')
    elif run_name[i] == '01_log_small':
        plt.hist(d1[var][:,:,:].flatten(), bins=[1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.1], label='january')

    var = 'ice_crystal_radius'
    unit = ' [m]'

    plot_name = 'frequency_{}_{}'.format(var, run_name[i])
    plot_title = 'Frequency {}'.format(var)

    plt.title(plot_title)

    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
    ax.set_ylabel('frequency')
    ax.set_xlabel(var + unit)
    ax.set_xscale('log')

    if run_name[i] == '02_log_big':
        plt.savefig('/net/n2o/wolke_scratch/sklampt/echam/plots/test793_taylor/icr/log_big/'+'/plot_{}.pdf'.format(plot_name), bbox_inches='tight')
    elif run_name[i] == '02_log_small':
        plt.savefig('/net/n2o/wolke_scratch/sklampt/echam/plots/test793_taylor/icr/log_small/'+'/plot_{}.pdf'.format(plot_name), bbox_inches='tight')
