# Plotting
import matplotlib.pyplot as plt
import matplotlib as matplotlib
import seaborn as sns
import numpy as np
# netCDF
from netCDF4 import Dataset
import xarray as xr
# Maps
from cartopy import config
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

### parameters that are plotted
parameter = ['IWP']

experiments = ['test791_taylor_onlyaccr_ws/test791_taylor_onlyaccr/annual', 
			   'test791_taylor_ws/test791_taylor/annual', 
			   'test791_taylor_double_ws/test791_taylor_double', 
			   'test793_drastic_ws/test793_156', 
			   'test793_drastic_ws/test793_176', 
			   'test793_taylor_ws/test793_taylor/annual']

file_name = ['test791_onlyaccr_taylor', 
			 'test791_taylor', 
			 'test791_doublesimplification', 
			 'test793_156', 
			 'test793_176', 
			 'test793_taylor']

simplification_name = ['Accretion - Taylor', 
					   'Accretion - double Taylor', 
					   'Aggregration - Drastic, alpha = 156', 
					   'Aggregation - Drastic, alpha = 176', 
					   'Aggregation - Taylor']

for j in range(len(experiments)):
	for i in range(len(parameter)):
		plot_name = str('Diff_'+parameter[i]+ '_' +file_name[j])
		title = str('Difference of Default model and ' + simplification_name[j])

		# Opening netCDF files
		d1 = Dataset('/net/n2o/wolke_scratch/sklampt/echam/init_diags_ws/years2003-2007/multi_annual_means_init_diags_2003-2007.nc')
		d2 = Dataset('/net/n2o/wolke_scratch/sklampt/echam/' + experiments[j] + '/multi_annual_means_' + file_name[j] + '_2003-2003.nc')

		# Access variables, e.g.
		d1[parameter[i]]
		d2[parameter[i]]

		# Plotting on a map
		lats = d1['lat'][:]
		lons = d1['lon'][:]

		cm = matplotlib.colors.ListedColormap((sns.color_palette("vlag", n_colors=7)).as_hex())

		fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5.5,4))

		ax = plt.axes(projection=ccrs.PlateCarree())

		ax.coastlines()

		gl = ax.gridlines(draw_labels=True, linewidth=0.25, color='gray', alpha=0.5)
		gl.xlabels_top = False
		gl.ylabels_right = False
		gl.xlabels_bottom = False
		gl.ylabels_left = False

		datavar = d1[parameter[i]][0,:,:]
		datavar_2 = d2[parameter[i]][0,:,:]
		datavar_diff = datavar_2 - datavar
		
		if parameter[i] == 'LWP':
			bar_range = np.arange(-100, 120, 10)
			unit = ' [g m-2]'
		elif parameter[i] == 'IWP':
			bar_range = np.arange(-20, 30, 5)
			unit = ' [g m-2]'
		elif parameter[i] == 'CC':
			bar_range = np.arange(-25, 20, 5)
			unit = ' [%]'
		elif parameter[i] == 'CDNC':
			bar_range = np.arange(-15, 18, 3)
			unit = ' [m-2]'

		levels = np.linspace(0,50,5)
		norm = matplotlib.colors.BoundaryNorm(levels, ncolors=cm.N, clip=True)
		im = ax.contourf(lons, lats, datavar_diff[:, :], levels=bar_range, cmap=cm, transform=ccrs.PlateCarree())
		cbar = fig.colorbar(im, orientation='horizontal')
		cbarlabel = str(parameter[i] + unit)
		cbar.set_label(cbarlabel)

		ax.set_xticks([-180,-120,-60,0,60,120,180], crs=ccrs.PlateCarree())
		ax.set_yticks([-60,-30,0,30,60], crs=ccrs.PlateCarree())
		lon_formatter = LongitudeFormatter()
		lat_formatter = LatitudeFormatter()
		ax.xaxis.set_major_formatter(lon_formatter)
		ax.yaxis.set_major_formatter(lat_formatter)

		plt.title(title)
		plt.savefig('/net/n2o/wolke_scratch/sklampt/echam/plots/plot_{}.pdf'.format(plot_name), bbox_inches='tight')