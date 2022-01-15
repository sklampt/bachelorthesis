#######################################################
# Script to estimate the ranges of conversion rates in the CMP routines
# Processes: aggregation
# use conda env: iacpy3_2020
# 2021 07 28
# author: Ulrike Proske
# sources:
#   Lohmann and Roeckner (1996): Design and performance of a new cloud microphysics scheme developed for the ECHAM general circulation model
#   Murakami (1990): NUmerical Modeling of Dynamical and Microphysical Evolution of an isolated convective Cloud: The 19 July 1981 CCOPE Cloud
#######################################################


#Load packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from netCDF4 import Dataset
import numpy.ma as ma
import matplotlib as matplotlib
from matplotlib import ticker, cm

import matplotlib.colors as cols
import matplotlib.cm as cmx
#import matplotlib._cntr as cntr
from matplotlib.colors import BoundaryNorm
from matplotlib.collections import LineCollection
from scipy import stats
from scipy.stats.stats import pearsonr

import math
from math import degrees, radians, cos, sin, acos

import seaborn as sns

plt.style.use(matplotlib.get_configdir()+'/paper_phasingcmp.mplstyle')
plt.rc('axes', axisbelow=True)

cm = matplotlib.colors.ListedColormap(sns.color_palette('Blues', 6).as_hex())

output_path = 'out/'
save_attr = '_gamma220'

def alpha(rho_air, r_iv):
    gamma = 220 #TODO: it looks like this is different in the Lohmann and Roeckner (1996) paper than in the code; 220 vs. 95
    #TODO: gamma is ccsaut in the code? But that's set via tuning and therefore something like 400
    rho_sigma = 1.3 #kg/m^3
    rho_ice = 500 #kg/m^3
    r_so = 1e-4 #m
    # shouldn't use gamma here because I'm replacing in the code where gamma isn't used yet
    zc1 = rho_air*17.5*(rho_sigma/rho_air)**(0.33)/rho_ice
    alpha = -(6/zc1*np.log10(r_iv/r_so))
    return alpha

def plot_mesh(x, y, z):

    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(12/2.54,12/2.54/2), sharex=True, gridspec_kw={'wspace': 0.5})
    plt.subplots_adjust(0,0,1,1)
    # Adjust canvas size: https://stackoverflow.com/questions/16057869/setting-the-size-of-the-plotting-canvas-in-matplotlib
    #fig = plt.figure(figsize=(3, 1.5))
    im = plt.pcolormesh(y, x, z)
    fig.colorbar(im, label='alpha')
    plt.xlabel(r'$r_{iv}$ (\SI{}{\micro \meter})')
    plt.ylabel(r'$\rho_{\mathrm{air}}$ (\SI{}{\kg \per \cubic \meter})')
    plt.savefig(output_path+'mesh'+save_attr+'.pdf', bbox_inches='tight')
    plt.close()

def plot_hist(array_alpha):
    print(np.median(array_alpha), np.nanmean(array_alpha))
    plt.hist(array_alpha.ravel(), bins=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,30,40,50,60,70,80,90,100])
    plt.xlabel('alpha')
    plt.ylabel('Frequency')
    plt.savefig(output_path+'hist'+save_attr+'.pdf', bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    rho_air = np.arange(0.25,1,0.0075)
    r_iv = np.arange(1e-6, 99e-6, 1e-6)
    import IPython; IPython.embed()
    array_alpha = np.zeros((np.shape(rho_air)[0],np.shape(r_iv)[0]))
    for i, rho in enumerate(rho_air):
        for j, r in enumerate(r_iv):
            array_alpha[i,j] = alpha(rho, r)
    x = np.zeros(np.shape(rho_air)[0]+1)
    x[0] = rho_air[0]-0.0075/2
    x[1:] = rho_air[:]+0.0075/2
    y = np.zeros(np.shape(r_iv)[0]+1)
    y[0] = r_iv[0]-1e-6/2
    y[1:] = r_iv[:]+1e-6/2
    plot_mesh(x, y, array_alpha)
    plot_hist(array_alpha)
