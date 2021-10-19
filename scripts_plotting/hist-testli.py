# Plotting
import matplotlib.pyplot as plt
import matplotlib as matplotlib
import seaborn as sns
import numpy as np
# netCDF
from netCDF4 import Dataset
import xarray as xr

import warnings
warnings.simplefilter(action = "ignore", category = RuntimeWarning)

from pathlib import Path
import re

#TODO: fill this
months = {
    1: "jan",
    2: "feb",
    3: "mar",
    4: "apr",
    5: "may",
    6: "jun",
    7: "jul",
    8: "aug",
    9: "sep",
    10: "oct",
    11: "nov",
    12: "dec",
}

folder_path = Path('/net/n2o/wolke_scratch/sklampt/echam/init_diags_ws/year2003/monthly_2003/')

for file in sorted(folder_path.glob('*init_diags_2003*.01_activ*.nc')):
    print(file)
    parameters = ['DIAG01']

    match = re.search(r'\S*init_diags_2003(\S{2})', str(file))
    month = match.group(1)
    month = months.get(int(month), 'default')
    print(month)

    for parameter in parameters:
        d1  = Dataset(file)

        run_names = [f'{month}_all', f'{month}_0-300', f'{month}_0-100', f'{month}_40-70']

        for run_name in run_names:
            var = parameter
            fig, ax = plt.subplots(nrows=1, ncols=1)


            d2 = d1[var][:,:,:].ravel()
            for j in range(len(d2)):
                if d2[j] == 0:
                    d2[j] = np.nan

            d2 = d2[~np.isnan(d2)]

            print("run name:", run_name)
            print("mean:", np.mean(d2))
            print("median:", np.median(d2))

            if run_name == f'{month}_all':
                plt.hist(d2, label=month)
            elif run_name == f'{month}_0-300':
                b = np.arange(0, 300, 5)
                plt.hist(d2, bins=b, label=month)
            elif run_name == f'{month}_0-100':
                b = np.arange(0, 100, 2)
                plt.hist(d2, bins=b, label=month)
            elif run_name == f'{month}_40-70':
                b = np.arange(40, 70, 0.5)
                plt.hist(d2, bins=b, label=month)

            var = 'alpha'
            unit = ''

            plot_name= 'frequency_{}_{}'.format(var, run_name) # adjust name

            plt.legend(bbox_to_anchor=(1,1), loc="upper left")#, title = 'sed. of cloud ice *') # loc decides location of legend
            ax.set_ylabel('frequency')          #CDNC & ICNC [1/m2] not [1/m3]!
            ax.set_xlabel(var + unit)
            #ax.set_xscale('log')

            plt.savefig('/net/n2o/wolke_scratch/sklampt/echam/plots/init/alpha/'+'/plot_{}.pdf'.format(plot_name), bbox_inches='tight')
