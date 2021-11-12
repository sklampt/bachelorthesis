# plots the zonal mean of variable as line plot
#-X° = southern hemisphere

# Plotting
import matplotlib.pyplot as plt
import matplotlib as matplotlib
import seaborn as sns
import numpy as np

# netCDF
from netCDF4 import Dataset
import xarray as xr

### parameters that are plotted
parameter = ['LWP', 'IWP', 'CC', 'CDNC']

for i in range(len(parameter)):
	# Opening netCDF files
	#default = 2          # added controle case for comparison
	#run_nr = 1
	#run_nr2 = 5
	#run_nr2 = 10
	run_nr = 1
	run_nr_diff = 2

        # ensemble - mean
        dc = Dataset('/net/n2o/wolke_scratch/sklampt/echam/init_diags_ws/years2003-2007/'.format(run_nr)+'ens2003-2007'.format(run_nr)+'.nc')
        # ensemble - stddev
        ds = Dataset('/net/n2o/wolke_scratch/sklampt/echam/init_diags_ws/years2003-2007/'.format(run_nr)+'ensstd2003-2007'.format(run_nr)+'.nc')
        # aggr
	d1 = Dataset('/net/n2o/wolke_scratch/sklampt/echam/test793_drastic_ws/test793_156/'.format(run_nr)+'multi_annual_means_test793_156_2003-2003'.format(run_nr)+'.nc') # drastic 156
	d2 = Dataset('/net/n2o/wolke_scratch/sklampt/echam/test793_drastic_ws/test793_176/'.format(run_nr)+'multi_annual_means_test793_176_2003-2003'.format(run_nr)+'.nc') # drastic 176
	d3 = Dataset('/net/n2o/wolke_scratch/sklampt/echam/test793_taylor_ws/test793_taylor/annual/'.format(run_nr)+'multi_annual_means_test793_taylor_2003-2003'.format(run_nr)+'.nc') # taylor
	# accr
	d4 = Dataset('/net/n2o/wolke_scratch/sklampt/echam/test791_taylor_ws/test791_taylor/annual/'.format(run_nr)+'multi_annual_means_test791_taylor_2003-2003'.format(run_nr)+'.nc') # zcolleffi
	d5 = Dataset('/net/n2o/wolke_scratch/sklampt/echam/test791_taylor_onlyaccr_ws/test791_taylor_onlyaccr/annual/'.format(run_nr)+'multi_annual_means_test791_onlyaccr_taylor_2003-2003'.format(run_nr)+'.nc') # only accr
	d6 = Dataset('/net/n2o/wolke_scratch/sklampt/echam/test791_taylor_double_ws/test791_taylor_double/'.format(run_nr)+'multi_annual_means_test791_doublesimplification_2003-2003'.format(run_nr)+'.nc') # double

	# Access variables, e.g.
	var = parameter[i]
	if var == 'CC':
		unit = ' [%]'
	elif var == 'CDNC':
		unit = ' [m-2]'
	else: 
		unit = ' [g m-2]'
		
	#run_name = 'comparison_all'
	#run_name = 'comparison_aggregation'
	run_name = 'comparison_accretion'

	plot_name= 'Zmean_{}_{}'.format(var, run_name) # adjust name
	plot_title = 'Zonal mean {}'.format(var)

	fig, ax = plt.subplots(nrows=1, ncols=1)

	
	# comparison all
	plt.plot(dc[var][0,:,0], label= 'default', c='black')
        # TODO: change file and variable names...
        plt.fill_between(dc[var][0,:,0], dc[var][0,:,0] - ds[var][0,:,0], dc[var][0,:,0] + ds[var][0,:,0])
	plt.plot(d1['lat'],d1[var][0,:,0], label= 'aggregation, drastic alpha=156', c='red')
	plt.plot(d2['lat'],d2[var][0,:,0], label= 'aggregation, drastic alpha=176', c='orange')
	plt.plot(d3['lat'],d3[var][0,:,0], label= 'aggregation, taylor', c='yellow')
	plt.plot(d4['lat'],d4[var][0,:,0], label= 'accretion, taylor - zcolleffi', c='yellowgreen')
	plt.plot(d5['lat'],d5[var][0,:,0], label= 'accretion, taylor - only accr', c='aqua')
	plt.plot(d6['lat'],d6[var][0,:,0], label= 'accretion, double taylor', c='orchid')
	'''
	# comparison aggregation
	plt.plot(dc['lat'],dc[var][0,:,0], label= 'default', c='black')
	plt.plot(d1['lat'],d1[var][0,:,0], label= 'aggregation, drastic alpha=156', c='red')
	plt.plot(d2['lat'],d2[var][0,:,0], label= 'aggregation, drastic alpha=176', c='orange')
	plt.plot(d3['lat'],d3[var][0,:,0], label= 'aggregation, taylor', c='yellow')
	
	
	# comparison accretion
	plt.plot(dc['lat'],dc[var][0,:,0], label= 'default', c='black')
	plt.plot(d4['lat'],d4[var][0,:,0], label= 'accretion, taylor - zcolleffi', c='yellowgreen')
	plt.plot(d5['lat'],d5[var][0,:,0], label= 'accretion, taylor - only accr', c='aqua')
	plt.plot(d6['lat'],d6[var][0,:,0], label= 'accretion, double taylor', c='orchid')
	'''

	plt.title(plot_title)

	plt.legend(bbox_to_anchor=(1,1), loc="upper left")#, title = 'sed. of cloud ice *') # loc decides location of legend
	ax.set_ylabel(var + unit)          #CDNC & ICNC [1/m2] not [1/m3]!
	ax.set_xlabel('latitude')


	plt.savefig('/net/n2o/wolke_scratch/sklampt/echam/plots/'+'/plot_{}.pdf'.format(plot_name), bbox_inches='tight')
