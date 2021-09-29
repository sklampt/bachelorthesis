# Plotting
import matplotlib.pyplot as plt
import matplotlib as matplotlib
import seaborn as sns
import numpy as np
# netCDF
from netCDF4 import Dataset
import xarray as xr

### parameters that are plotted
parameter = ['diag02', 'diag03']

for i in range(len(parameter)):
	# Opening netCDF files
	#default = 2          # added controle case for comparison
	#run_nr = 1
	#run_nr2 = 5
	#run_nr2 = 10
	run_nr = 1
	run_nr_diff = 2

	d1  = Dataset('/net/n2o/wolke_scratch/sklampt/echam/test793_taylor_ws/test793_taylor/'.format(run_nr_diff)+'test793_taylor_year_200301.01_activ'.format(run_nr_diff)+'.nc')
	# d2  = Dataset('/net/n2o/wolke_scratch/mabeling/echam/run/run_{}/'.format(run_nr2)+'multi_annual_means_run_{}_2003-2003_zmean.nc'.format(run_nr2))
	# d3  = Dataset('/net/n2o/wolke_scratch/mabeling/echam/run/run_{}/'.format(run_nr3)+'multi_annual_means_run_{}_2003-2003_zmean.nc'.format(run_nr3))
	# d4  = Dataset('/net/n2o/wolke_scratch/mabeling/echam/run/run_{}/'.format(run_nr4)+'multi_annual_means_run_{}_2003-2003_zmean.nc'.format(run_nr4))
    # d5  = Dataset('/net/n2o/wolke_scratch/sklampt/echam/test793_ws/test793_01/'.format(run_nr_diff)+'multi_annual_means_test793_01_2003-2003'.format(run_nr_diff)+'.nc')
	# d6  = Dataset('/net/n2o/wolke_scratch/mabeling/echam/run/run_{}/'.format(run_nr2)+'multi_annual_means_run_{}_2003-2003_zmean.nc'.format(run_nr2))
	# d7  = Dataset('/net/n2o/wolke_scratch/mabeling/echam/run/run_{}/'.format(run_nr3)+'multi_annual_means_run_{}_2003-2003_zmean.nc'.format(run_nr3))
	# d8  = Dataset('/net/n2o/wolke_scratch/mabeling/echam/run/run_{}/'.format(run_nr4)+'multi_annual_means_run_{}_2003-2003_zmean.nc'.format(run_nr4))
    # d9  = Dataset('/net/n2o/wolke_scratch/sklampt/echam/test793_ws/test793_01/'.format(run_nr_diff)+'multi_annual_means_test793_01_2003-2003'.format(run_nr_diff)+'.nc')
	# d10 = Dataset('/net/n2o/wolke_scratch/mabeling/echam/run/run_{}/'.format(run_nr2)+'multi_annual_means_run_{}_2003-2003_zmean.nc'.format(run_nr2))
	# d11 = Dataset('/net/n2o/wolke_scratch/mabeling/echam/run/run_{}/'.format(run_nr3)+'multi_annual_means_run_{}_2003-2003_zmean.nc'.format(run_nr3))
	# d12 = Dataset('/net/n2o/wolke_scratch/mabeling/echam/run/run_{}/'.format(run_nr4)+'multi_annual_means_run_{}_2003-2003_zmean.nc'.format(run_nr4))



	# Access variables, e.g.
	var = parameter[i]
	if var == 'diag02':
		unit = ' [m]'
	elif var == 'diag03':
		unit = ' [kg m-3]'

	run_name = '1'

	plot_name= 'frequency_{}_{}'.format(var, run_name) # adjust name
	plot_title = 'Frequency {}'.format(var)

	fig, ax = plt.subplots(nrows=1, ncols=1)


	plt.hist(d1[var][0,:,0], label='january')
	#plt.plot(d2['lat'],d2[var][0,:,0], label= 'WBF = 0', c='green')
	#plt.plot(d3['lat'],d3[var][0,:,0], label= 'WBF, sed = 0', c='red')
	#plt.bar(dc['lat'],dc[var][0,:,0], label= 'default', c='black')



	plt.title(plot_title)

	plt.legend(bbox_to_anchor=(1,1), loc="upper left")#, title = 'sed. of cloud ice *') # loc decides location of legend
	ax.set_ylabel('frequency')          #CDNC & ICNC [1/m2] not [1/m3]!
	ax.set_xlabel(var + unit)


	plt.savefig('/net/n2o/wolke_scratch/sklampt/echam/plots/test793_taylor/'+'/plot_{}.pdf'.format(plot_name), bbox_inches='tight')
