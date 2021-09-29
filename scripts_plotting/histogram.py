# Plotting
import matplotlib.pyplot as plt
import matplotlib as matplotlib
import seaborn as sns
import numpy as np
# netCDF
from netCDF4 import Dataset
import xarray as xr

### parameters that are plotted
parameter = ['DIAG01_2', 'DIAG01_3']

for i in range(len(parameter)):
	# Opening netCDF files
	#default = 2          # added controle case for comparison
	#run_nr = 1
	#run_nr2 = 5
	#run_nr2 = 10
	run_nr = 1
	run_nr_diff = 2

	d1  = Dataset('/net/n2o/wolke_scratch/sklampt/echam/test793_taylor_ws/test793_taylor/'.format(run_nr_diff)+'test793_taylor_year_200303.01_activ'.format(run_nr_diff)+'.nc')

	# Access variables, e.g.
	var = parameter[i]
	if var == 'DIAG01_2':
		unit = ' [m]'
	elif var == 'DIAG01_3':
		unit = ' [kg m-3]'

	run_name = '3'

	plot_name= 'frequency_{}_{}'.format(var, run_name) # adjust name
	plot_title = 'Frequency {}'.format(var)

	fig, ax = plt.subplots(nrows=1, ncols=1)


	plt.hist(d1[var][0,:,0], label='march')
	#plt.plot(d2['lat'],d2[var][0,:,0], label= 'WBF = 0', c='green')
	#plt.plot(d3['lat'],d3[var][0,:,0], label= 'WBF, sed = 0', c='red')
	#plt.bar(dc['lat'],dc[var][0,:,0], label= 'default', c='black')



	plt.title(plot_title)

	plt.legend(bbox_to_anchor=(1,1), loc="upper left")#, title = 'sed. of cloud ice *') # loc decides location of legend
	ax.set_ylabel('frequency')          #CDNC & ICNC [1/m2] not [1/m3]!
	ax.set_xlabel(var + unit)


	plt.savefig('/net/n2o/wolke_scratch/sklampt/echam/plots/test793_taylor/'+'/plot_{}.pdf'.format(plot_name), bbox_inches='tight')
