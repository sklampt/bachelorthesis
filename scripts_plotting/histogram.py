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

### parameters that are plotted
#parameter = ['DIAG01_2', 'DIAG01_3', 'DIAG01']
#parameter = ['DIAG01_2']
parameter = ['DIAG01']

for k in range(len(parameter)):
	# Opening netCDF files
	#default = 2          # added controle case for comparison
	#run_nr = 1
	#run_nr2 = 5
	#run_nr2 = 10
	run_nr = 1
	run_nr_diff = 2

	d1  = Dataset('/net/n2o/wolke_scratch/sklampt/echam/init_diags_ws/year2003/monthly_2003/'.format(run_nr_diff)+'init_diags_200312.01_activ'.format(run_nr_diff)+'.nc')

	#var = parameter[k]

	run_name = ['12_all', '12_0-300', '12_0-100', '12_40-70']
	
	for i in range(len(run_name)):
		var = parameter[k]
		fig, ax = plt.subplots(nrows=1, ncols=1)

		if var == 'DIAG01_2':
			plt.hist(d1[var][:,:,:].flatten(), label='january')
			#plt.hist(d1[var][:,:,:].flatten(), bins=[1e-7, 1e-6, 1e-5, 0.1, 0.9, 0.99, 1.], label='december')
			#plt.hist(d1[var][:,:,:].flatten(), bins=[1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.1], label='january')
			var = 'ice_crystal_radius'
			unit = ' [m]'
		elif var == 'DIAG01_3':
			plt.hist(d1[var][:,:,:].flatten(), label='january')
			var = 'rho_air'
			unit = ' [kg m-3]'
		else:
			#plt.hist(d1[var][:,:,:].flatten(), label='january')
			#plt.hist(d1[var][:,:,:].flatten(), bins=[0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240], label='december')
			#np.where(d1[var][:,:,:] == 0., np.nan, d1[var][:,:,:])
			#d1[var][1,1,1] = np.nan
			#d1[var][:,:,:][d1[var][:,:,:] == 0.] = np.nan
			#print(d1[var][:,:,:])
			d2 = d1[var][:,:,:].ravel()
			for j in range(len(d2)):
				if d2[j] == 0:
					d2[j] = np.nan
			#print(d2)
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
			var = 'alpha'
			unit = ''

		plot_name= 'frequency_{}_{}'.format(var, run_name[i]) # adjust name
		#plot_title = 'Frequency {}'.format(var)

		#plt.title(plot_title)

		plt.legend(bbox_to_anchor=(1,1), loc="upper left")#, title = 'sed. of cloud ice *') # loc decides location of legend
		ax.set_ylabel('frequency')          #CDNC & ICNC [1/m2] not [1/m3]!
		ax.set_xlabel(var + unit)
		#ax.set_xscale('log')


		plt.savefig('/net/n2o/wolke_scratch/sklampt/echam/plots/init/alpha/'+'/plot_{}.pdf'.format(plot_name), bbox_inches='tight')
