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
parameter = ['SW', 'LW', 'LWP', 'IWP', 'CC', 'CDNC']

for i in range(len(parameter)):
	# Opening netCDF files
	run_nr = 1
	
	### TODO: update number at end (if there is more than one plot)
	plot_name= str(parameter[i]+'_50')
	
	plot_title = str(parameter[i]+' for eta = 1')
	
	### TODO: update source folder
	d1 = Dataset('/net/n2o/wolke_scratch/sklampt/echam/test793_ws/test793_50/'.format(run_nr)+'multi_annual_means_test793_50_2003-2003'.format(run_nr)+'.nc')

	# Access variables, e.g.
	d1[parameter[i]]

	#import IPython; IPython.embed()

	# Plotting on a map
	lats = d1['lat'][:]
	lons = d1['lon'][:]

	#Color:
	#cm = matplotlib.colors.ListedColormap((sns.color_palette("vlag")).as_hex()) #blue to red
	#cm = matplotlib.colors.ListedColormap((sns.color_palette("ch:rot=-.0,s=.8")).as_hex())

	cm = matplotlib.colors.ListedColormap((sns.color_palette("Reds", n_colors= 8)).as_hex())


	fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5.5,4))

	ax = plt.axes(projection=ccrs.PlateCarree())

	ax.coastlines()

	gl = ax.gridlines(draw_labels=True, linewidth=0.25, color='gray', alpha=0.5)
	gl.xlabels_top = False
	gl.ylabels_right = False
	gl.xlabels_bottom = False
	gl.ylabels_left = False

	# Mask so that nans appear white
	#m = np.ma.masked_where(np.isnan(hist2dplot),hist2dplot)
	# x and y are bounds, so z should be the value *inside* those bounds.
	# Therefore, remove the last value from the z array.
	datavar = d1[parameter[i]][0,:,:] 

	var = parameter[i]
	if var == 'CC':
		unit = ' [%]'
	elif var == 'CDNC':
		unit = ' [m-2]'
	elif var == 'SW' or 'LW':
		unit = ' [W m-2]'
	else: 
		unit = ' [g m-2]'

	#im = ax.pcolormesh(lons, lats, datavar[:, :], cmap=cm)

	v_min, v_max = 0, 400
	im = ax.pcolormesh(lons, lats, datavar[:, :], cmap=cm, vmin=v_min, vmax=v_max)
	cbar = fig.colorbar(im, orientation='horizontal', label= str(parameter[i]+unit))



	#ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '50m', edgecolor='gray', facecolor='none'))
	#states_borders_50m = cfeature.NaturalEarthFeature('cultural', 'admin_0_boundary_lines_land', '50m',
	#                                    edgecolor='k', facecolor='none')
	#ax.add_feature(states_borders_50m)

	ax.set_xticks([-180,-120,-60,0,60,120,180], crs=ccrs.PlateCarree())
	ax.set_yticks([-60,-30,0,30,60], crs=ccrs.PlateCarree())
	lon_formatter = LongitudeFormatter()
	lat_formatter = LatitudeFormatter()
	ax.xaxis.set_major_formatter(lon_formatter)
	ax.yaxis.set_major_formatter(lat_formatter)

	plt.title(plot_title)
	### TODO: update destination folder
	plt.savefig('/net/n2o/wolke_scratch/sklampt/echam/plots/drastic/test793_50/single/'.format(run_nr)+'/plot_{}.pdf'.format(plot_name), bbox_inches='tight')
