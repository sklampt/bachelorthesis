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

experiments = ['test791_taylor_double_ws/test791_taylor_double', 'test793_drastic_ws/test793_156', 'test793_drastic_ws/test793_176']

file_name = ['test791_doublesimplification', 'test793_156', 'test793_176']

for j in range(len(experiments)):
	for i in range(len(parameter)):
		# Opening netCDF files
		#default = 2          # added controle case for comparison
		#run_nr = 1
		#run_nr2 = 5
		#run_nr2 = 10
		run_nr = 1
		run_nr_diff = 2

		dc = Dataset('/net/n2o/wolke_scratch/sklampt/echam/init_diags_ws/year2003/'.format(run_nr)+'multi_annual_means_init_diags_2003-2003'.format(run_nr)+'.nc')
		d1 = Dataset('/net/n2o/wolke_scratch/sklampt/echam/' + experiments[j] + '/'.format(run_nr)+'multi_annual_means_' + file_name[j] + '_2003-2003'.format(run_nr)+'.nc')
		

		# Access variables, e.g.
		var = parameter[i]
		if var == 'CC':
			unit = ' [%]'
		elif var == 'CDNC':
			unit = ' [m-2]'
		else: 
			unit = ' [g m-2]'
			
		plot_name= 'Zmean_{}_{}'.format(var, file_name[j]) # adjust name
		plot_title = 'Zonal mean {}'.format(var)

		fig, ax = plt.subplots(nrows=1, ncols=1)


		#plt.plot(d1['lat'],d1[var][0,:,0], label= 'lsimple_aggr_taylor', c='green')
		#plt.plot(d2['lat'],d2[var][0,:,0], label= 'WBF = 0', c='green')
		#plt.plot(d3['lat'],d3[var][0,:,0], label= 'WBF, sed = 0', c='red')
		plt.plot(dc['lat'],dc[var][0,:,0], label= 'default', c='black')
		plt.plot(d1['lat'],d1[var][0,:,0], label= file_name[j], c='green')


		plt.title(plot_title)

		plt.legend(bbox_to_anchor=(1,1), loc="upper left")#, title = 'sed. of cloud ice *') # loc decides location of legend
		ax.set_ylabel(var + unit)          #CDNC & ICNC [1/m2] not [1/m3]!
		ax.set_xlabel('latitude')


		plt.savefig('/net/n2o/wolke_scratch/sklampt/echam/plots/'+'/plot_{}.pdf'.format(plot_name), bbox_inches='tight')
