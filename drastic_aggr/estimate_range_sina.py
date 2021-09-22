#######################################################
# Script to estimate the ranges of conversion rates in the CMP routines
# Processes: aggregation
# use conda env: iacpy3_2020
# 2021 09 06
# author: Sina Klampt
# sources:
#   Lohmann and Roeckner (1996): Design and performance of a new cloud microphysics scheme developed for the ECHAM general circulation model
#   Murakami (1990): NUmerical Modeling of Dynamical and Microphysical Evolution of an isolated convective Cloud: The 19 July 1981 CCOPE Cloud
#   Ulrike Proske: estimate_ranges.py
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

#plt.style.use(matplotlib.get_configdir()+'/paper_phasingcmp.mplstyle')
plt.rc('axes', axisbelow=True)

cm = matplotlib.colors.ListedColormap(sns.color_palette('Blues', 6).as_hex())

output_path = 'out/'
#save_attr = '_zris_new_alpha1'

# range for air density and ice crystal size, inv. air density calculated with rho_air
def alpha1(rho_air, r_iv):
    rho_sigma = 1.3 # [kg/m^3]     -> what does rho_sigma mean? in the following code: rho_inv = rho_sigma/rho_air
    rho_ice = 500   # crhoi [kg/m^3]
    r_so = 1e-4     # [m]

    zc1 = 17.5 * rho_air * (rho_sigma/rho_air)**(0.33) / rho_ice
    alpha = -(6/zc1 * np.log10(r_iv/r_so))
    return alpha

# range for air density and inverse air density, ice crystal size fix
def alpha2(rho_air, rho_inv, ris):
    rho_ice = 500    # crhoi [kg/m^3]
    #ris = 2e-6      # [m]
    r_so = 1e-4      # [m]

    zc1 = 17.5 * rho_air * (rho_inv)**(0.33) / rho_ice
    alpha = -(6/zc1 * np.log10(ris/r_so))
    return alpha

# range for inverse air density and ice crystal size, air density fix
def alpha3(rho_inv, r_iv, rair):
    #rair = 1.225    # [kg/m3], 101.325kPa & 15degC (wikipedia)
    rho_ice = 500    # crhoi [kg/m^3]
    r_so = 1e-4      # [m]

    zc1 = 17.5 * rair * (rho_inv)**(0.33) / rho_ice
    alpha = -(6/zc1 * np.log10(r_iv/r_so))
    return alpha

def plot_mesh1(x, y, z):
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(12/2.54,12/2.54/2), sharex=True, gridspec_kw={'wspace': 0.5})
    plt.subplots_adjust(0,0,1,1)
    # Adjust canvas size: https://stackoverflow.com/questions/16057869/setting-the-size-of-the-plotting-canvas-in-matplotlib
    #fig = plt.figure(figsize=(3, 1.5))
    im = plt.pcolormesh(y, x, z)
    fig.colorbar(im, label='alpha')
    plt.xlabel(r'$r_{ice crystal}$ [$\mu$m]')
    plt.ylabel(r'$\rho_{\mathrm{air}}$ [kg/m³]')
    plt.savefig(output_path+'mesh'+save_attr+'.pdf', bbox_inches='tight')
    plt.close()

def plot_mesh2(x, y, z):
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(12/2.54,12/2.54/2), sharex=True, gridspec_kw={'wspace': 0.5})
    plt.subplots_adjust(0,0,1,1)
    # Adjust canvas size: https://stackoverflow.com/questions/16057869/setting-the-size-of-the-plotting-canvas-in-matplotlib
    #fig = plt.figure(figsize=(3, 1.5))
    im = plt.pcolormesh(y, x, z)
    fig.colorbar(im, label='alpha')
    plt.xlabel(r'$\rho_{\mathrm{inv}}$ [m³/kg]')
    plt.ylabel(r'$\rho_{\mathrm{air}}$ [kg/m³]')
    plt.savefig(output_path+'mesh'+save_attr+'.pdf', bbox_inches='tight')
    plt.close()

def plot_mesh3(x, y, z):
    fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(12/2.54,12/2.54/2), sharex=True, gridspec_kw={'wspace': 0.5})
    plt.subplots_adjust(0,0,1,1)
    # Adjust canvas size: https://stackoverflow.com/questions/16057869/setting-the-size-of-the-plotting-canvas-in-matplotlib
    #fig = plt.figure(figsize=(3, 1.5))
    im = plt.pcolormesh(y, x, z)
    fig.colorbar(im, label='alpha')
    plt.xlabel(r'$r_{ice crystal}$ [$\mu$m]')
    plt.ylabel(r'$\rho_{\mathrm{inv}}$ [m³/kg]')
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
    #drastic
    rho_air  = np.arange(0.25,1.47,0.0075)      # prho -> air density [kg/m3]
    rho_air_eff  = [0.25, 0.494, 0.738, 0.982, 1.226 ,1.47]
    rho_inv  = np.arange(1., 8.5, 0.05)         # pqrho -> inv. air density [m3/kg]
    #r_iv     = np.arange(1e-6, 1e-4, 1e-6)   # zris, diags sina
    # r_iv_eff = np.arange(2e-6, 1.85e-4, 1e-6)   # effective_ice_crystal_radius, diags sina
    #r_iv_eff = [2e-6, 3.86e-5, 7.52e-5, 1.118e-4, 1.484e-4, 1.85e-4]
    r_iv     = np.arange(3.86e-5, 1e-4, 1e-6)
    r_iv_eff = [3.86e-5, 7.52e-5, 1.118e-4, 1.484e-4, 1.85e-4]

    # alpha1
    array_alpha = np.zeros((np.shape(rho_air)[0],np.shape(r_iv)[0]))
    for i, rho in enumerate(rho_air):
        for j, r in enumerate(r_iv):
            array_alpha[i,j] = alpha1(rho, r)
    x = np.zeros(np.shape(rho_air)[0]+1)
    x[0] = rho_air[0]-0.0075/2
    x[1:] = rho_air[:]+0.0075/2
    y = np.zeros(np.shape(r_iv)[0]+1)
    y[0] = r_iv[0]-1e-6/2
    y[1:] = r_iv[:]+1e-6/2

    save_attr = '_alpha1_newrange_riv'
    plot_mesh1(x, y, array_alpha)
    #plot_hist(array_alpha)

    # alpha2
    for k in range(len(r_iv_eff)):
        ris = r_iv_eff[k]
        array_alpha = np.zeros((np.shape(rho_air)[0],np.shape(rho_inv)[0]))
        for i, rho in enumerate(rho_air):
            for j, r in enumerate(rho_inv):
                array_alpha[i,j] = alpha2(rho, r, ris)
        x = np.zeros(np.shape(rho_air)[0]+1)
        x[0] = rho_air[0]-0.0075/2
        x[1:] = rho_air[:]+0.0075/2
        y = np.zeros(np.shape(rho_inv)[0]+1)
        y[0] = rho_inv[0]-0.05/2
        y[1:] = rho_inv[:]+0.05/2

        save_attr = str('_icr_alpha2_' + str(r_iv_eff[k]))
        #plot_mesh2(x, y, array_alpha)
        #plot_hist(array_alpha)

    # alpha3
    for k in range(len(rho_air_eff)):
        rair = rho_air_eff[k]
        array_alpha = np.zeros((np.shape(rho_inv)[0],np.shape(r_iv)[0]))
        for i, rho in enumerate(rho_inv):
            for j, r in enumerate(r_iv):
                array_alpha[i,j] = alpha3(rho, r, rair)
        x = np.zeros(np.shape(rho_inv)[0]+1)
        x[0] = rho_inv[0]-0.05/2
        x[1:] = rho_inv[:]+0.05/2
        y = np.zeros(np.shape(r_iv)[0]+1)
        y[0] = r_iv[0]-1e-6/2
        y[1:] = r_iv[:]+1e-6/2

        save_attr = str('_rhoair_alpha3_newrange_riv_' + str(rho_air_eff[k]))
        plot_mesh3(x, y, array_alpha)
        #plot_hist(array_alpha)
