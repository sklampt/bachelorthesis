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

experiments = ['test791_taylor_onlyaccr_ws/test791_taylor_onlyaccr/annual', 
			   'test791_taylor_ws/test791_taylor/annual', 
			   'test791_taylor_double_ws/test791_taylor_double', 
			   'test793_drastic_ws/test793_156', 
			   'test793_drastic_ws/test793_176', 
			   'test793_taylor_ws/test793_taylor/annual']

file_name = ['accr_taylor', 
			 'accr_zcolleffi', 
			 'accr_double', 
			 '156', 
			 '176', 
			 'aggr_taylor']

for j in range(len(experiments)):
	for i in range(len(parameter)):
		# Opening netCDF files
		dc = Dataset('/net/n2o/wolke_scratch/sklampt/echam/init_diags_ws/years2003-2007/ens2003-2007.nc')
		ds = Dataset('/net/n2o/wolke_scratch/sklampt/echam/init_diags_ws/years2003-2007/ensstd2003-2007.nc')
		d1 = Dataset('/net/n2o/wolke_scratch/sklampt/echam/' + experiments[j] + '/zm_' + file_name[j] + '_2003-2003.nc')

		# Access variables, e.g.
		var = parameter[i]
		if var == 'CC':
			unit = ' [%]'
		elif var == 'CDNC':
			unit = ' [m-2]'
		elif var == 'IWP' or 'LWP': 
			unit = ' [g m-2]'
			
		plot_name= 'Zmean_{}_{}_nolegend'.format(var, file_name[j]) # adjust name
		plot_title = 'Zonal mean {}'.format(var)

		fig, ax = plt.subplots(nrows=1, ncols=1)

		plt.plot(dc['lat'],dc[var][0,:,0], label= 'default', c='black')
		plt.fill_between(dc['lat'], dc[var][0,:,0]-ds[var][0,:,0], dc[var][0,:,0]+ds[var][0,:,0])
		plt.plot(d1['lat'],d1[var][0,:,0], label= file_name[j], c='green')

		plt.title(plot_title)

		#plt.legend(bbox_to_anchor=(1,1), loc="upper left")#, title = 'sed. of cloud ice *') # loc decides location of legend
		ax.set_ylabel(var + unit)          #CDNC & ICNC [1/m2] not [1/m3]!
		ax.set_xlabel('latitude')

		plt.savefig('/net/n2o/wolke_scratch/sklampt/echam/plots/'+'/plot_{}.pdf'.format(plot_name), bbox_inches='tight')