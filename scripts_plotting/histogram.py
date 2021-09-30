# Plotting
import matplotlib.pyplot as plt
import matplotlib as matplotlib
import seaborn as sns
import numpy as np
# netCDF
from netCDF4 import Dataset
import xarray as xr

### parameters that are plotted
parameter = ['DIAG01_2', 'DIAG01_3', 'DIAG01']

for i in range(len(parameter)):
	# Opening netCDF files
	#default = 2          # added controle case for comparison
	#run_nr = 1
	#run_nr2 = 5
	#run_nr2 = 10
	run_nr = 1
	run_nr_diff = 2

	d1  = Dataset('/net/n2o/wolke_scratch/sklampt/echam/test793_taylor_ws/test793_taylor/'.format(run_nr_diff)+'test793_taylor_year_200312.01_activ'.format(run_nr_diff)+'.nc')

	var = parameter[i]

	run_name = '12_init'

	fig, ax = plt.subplots(nrows=1, ncols=1)

	if var == 'DIAG01_2':
		#plt.hist(d1[var][:,:,:].flatten(), bins=[1e-7, 1e-6, 1e-5, 0.1, 0.9, 0.99, 1.], label='december')
		#plt.hist(d1[var][:,:,:].flatten(), bins=[1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.1], label='december')
		plt.hist(d1[var][:,:,:].flatten(), label='december')
		var = 'ice_crystal_radius'
		unit = ' [m]'
	elif var == 'DIAG01_3':
		plt.hist(d1[var][:,:,:].flatten(), label='december')
		var = 'rho_air'
		unit = ' [kg m-3]'
	else:
		plt.hist(d1[var][:,:,:].flatten(), label='december')
		var = 'alpha'

	plot_name= 'frequency_{}_{}'.format(var, run_name) # adjust name
	plot_title = 'Frequency {}'.format(var)

	plt.title(plot_title)

	plt.legend(bbox_to_anchor=(1,1), loc="upper left")#, title = 'sed. of cloud ice *') # loc decides location of legend
	ax.set_ylabel('frequency')          #CDNC & ICNC [1/m2] not [1/m3]!
	ax.set_xlabel(var + unit)
	ax.set_xscale('log')


	plt.savefig('/net/n2o/wolke_scratch/sklampt/echam/plots/test793_taylor/'+'/plot_{}.pdf'.format(plot_name), bbox_inches='tight')
