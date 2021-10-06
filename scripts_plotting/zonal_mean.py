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

	#dc = Dataset('/net/n2o/wolke_scratch/sklampt/echam/run/run_{}/'.format(default)+'multi_annual_means_run_{}_2003-2003_zmean.nc'.format(default))
	dc = Dataset('/net/n2o/wolke_scratch/sklampt/echam/test_init_ws/test_init/'.format(run_nr)+'multi_annual_means_test_init_2003-2003'.format(run_nr)+'.nc')
	d1 = Dataset('/net/n2o/wolke_scratch/sklampt/echam/test793_taylor_ws/test793_taylor/annual/'.format(run_nr_diff)+'multi_annual_means_test793_taylor_year_2003-2003'.format(run_nr_diff)+'.nc')
	#d2 = Dataset('/net/n2o/wolke_scratch/mabeling/echam/run/run_{}/'.format(run_nr2)+'multi_annual_means_run_{}_2003-2003_zmean.nc'.format(run_nr2))
	#d3 = Dataset('/net/n2o/wolke_scratch/mabeling/echam/run/run_{}/'.format(run_nr3)+'multi_annual_means_run_{}_2003-2003_zmean.nc'.format(run_nr3))
	#d4 = Dataset('/net/n2o/wolke_scratch/mabeling/echam/run/run_{}/'.format(run_nr4)+'multi_annual_means_run_{}_2003-2003_zmean.nc'.format(run_nr4))



	# Access variables, e.g.
	var = parameter[i]
	if var == 'CC':
		unit = ' [%]'
	elif var == 'CDNC':
		unit = ' [m-2]'
	else: 
		unit = ' [g m-2]'
		
	run_name = 'lsimple_aggr_taylor'

	plot_name= 'Zmean_{}_{}'.format(var, run_name) # adjust name
	plot_title = 'Zonal mean {}'.format(var)

	fig, ax = plt.subplots(nrows=1, ncols=1)


	plt.plot(d1['lat'],d1[var][0,:,0], label= 'lsimple_aggr_taylor', c='green')
	#plt.plot(d2['lat'],d2[var][0,:,0], label= 'WBF = 0', c='green')
	#plt.plot(d3['lat'],d3[var][0,:,0], label= 'WBF, sed = 0', c='red')
	plt.plot(dc['lat'],dc[var][0,:,0], label= 'default', c='black')



	plt.title(plot_title)

	plt.legend(bbox_to_anchor=(1,1), loc="upper left")#, title = 'sed. of cloud ice *') # loc decides location of legend
	ax.set_ylabel(var + unit)          #CDNC & ICNC [1/m2] not [1/m3]!
	ax.set_xlabel('latitude')


	plt.savefig('/net/n2o/wolke_scratch/sklampt/echam/plots/test793_taylor/zonal_mean/'+'/plot_{}.pdf'.format(plot_name), bbox_inches='tight')
