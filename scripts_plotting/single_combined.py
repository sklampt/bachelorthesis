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
	run_nr_diff = 2
	### TODO: update source folder
	d1 = Dataset('/net/n2o/wolke_scratch/sklampt/echam/test_init_ws/test_init/'.format(run_nr)+'multi_annual_means_test_init_2003-2003'.format(run_nr)+'.nc')
	d2 = Dataset('/net/n2o/wolke_scratch/sklampt/echam/test793_ws/test793_01/'.format(run_nr_diff)+'multi_annual_means_test793_01_2003-2003'.format(run_nr_diff)+'.nc')
		
	### TODO: update number at end (if there is more than one plot)
	plot_name= str(parameter[i]+'_01')
	plot_title = str(parameter[i]+' for eta = 1')
	
	var = parameter[i]
	if var == 'CC':
		unit = ' [%]'
	elif var == 'CDNC':
		unit = ' [m-2]'
	elif var == 'SW' or 'LW':
		unit = ' [W m-2]'
	else: 
		unit = ' [g m-2]'

	
	fig = plt.figure()

	### plot d1
	# Access variables, e.g.
	d1[parameter[i]]

	# Plotting on a map
	lats1 = d1['lat'][:]
	lons1 = d1['lon'][:]

	cm = matplotlib.colors.ListedColormap((sns.color_palette("Reds", n_colors= 8)).as_hex())

	ax1 = fig.add_subplot(211)
	ax1.set_title("default")
	#fig1, ax = plt.subplots(nrows=1, ncols=1, figsize=(5.5,4))

	ax1 = plt.axes(projection=ccrs.PlateCarree())
	ax1.coastlines()

	gl = ax1.gridlines(draw_labels=True, linewidth=0.25, color='gray', alpha=0.5)
	gl.xlabels_top = False
	gl.ylabels_right = False
	gl.xlabels_bottom = False
	gl.ylabels_left = False

	datavar1 = d1[parameter[i]][0,:,:]

	v_min, v_max = 0, 400
	im1 = ax1.pcolormesh(lons1, lats1, datavar1[:, :], cmap=cm, vmin=v_min, vmax=v_max)
	cbar = fig.colorbar(im1, orientation='horizontal', label= str(parameter[i]+unit), ax= ax1)

	ax1.set_xticks([-180,-120,-60,0,60,120,180], crs=ccrs.PlateCarree())
	ax1.set_yticks([-60,-30,0,30,60], crs=ccrs.PlateCarree())
	lon_formatter = LongitudeFormatter()
	lat_formatter = LatitudeFormatter()
	ax1.xaxis.set_major_formatter(lon_formatter)
	ax1.yaxis.set_major_formatter(lat_formatter)
	

	
	### plot d2
	# Access variables, e.g.
	d2[parameter[i]]

	# Plotting on a map
	lats2 = d2['lat'][:]
	lons2 = d2['lon'][:]

	cm = matplotlib.colors.ListedColormap((sns.color_palette("Reds", n_colors= 8)).as_hex())
	
	ax2 = fig.add_subplot(212)
	ax2.set_title("lsimple_aggr = true")
	#fig2, ax = plt.subplots(nrows=1, ncols=1, figsize=(5.5,4))

	ax2 = plt.axes(projection=ccrs.PlateCarree())
	ax2.coastlines()

	gl = ax2.gridlines(draw_labels=True, linewidth=0.25, color='gray', alpha=0.5)
	gl.xlabels_top = False
	gl.ylabels_right = False
	gl.xlabels_bottom = False
	gl.ylabels_left = False

	datavar2 = d2[parameter[i]][0,:,:]

	v_min, v_max = 0, 400
	im2 = ax2.pcolormesh(lons2, lats2, datavar2[:, :], cmap=cm, vmin=v_min, vmax=v_max)
	cbar = fig.colorbar(im2, orientation='horizontal', label= str(parameter[i]+unit), ax= ax2)

	ax2.set_xticks([-180,-120,-60,0,60,120,180], crs=ccrs.PlateCarree())
	ax2.set_yticks([-60,-30,0,30,60], crs=ccrs.PlateCarree())
	lon_formatter = LongitudeFormatter()
	lat_formatter = LatitudeFormatter()
	ax2.xaxis.set_major_formatter(lon_formatter)
	ax2.yaxis.set_major_formatter(lat_formatter)
	



	### plot combined
	### TODO: update title if necessary
	
	#fig.suptitle(plot_title)
	
	#fig = plt.figure()
	#ax1 = fig.add

	
	### TODO: update destination folder
	plt.savefig('/net/n2o/wolke_scratch/sklampt/echam/plots/test793_01/single/combined/'.format(run_nr)+'/plot_{}.pdf'.format(plot_name), bbox_inches='tight')
