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
parameter = ['LWP', 'IWP', 'CC', 'CDNC']

for i in range(len(parameter)):
	# Opening netCDF files
	run_nr = 1
	run_nr_diff = 2

	### TODO: update number at end (if there is more than one plot)
	plot_name = str('Diff_'+parameter[i]+'_drastic_alpha50')

	### TODO: update source folder
	d1 = Dataset('/net/n2o/wolke_scratch/sklampt/echam/test_init_ws/test_init/'.format(run_nr)+'multi_annual_means_test_init_2003-2003'.format(run_nr)+'.nc')
	d2 = Dataset('/net/n2o/wolke_scratch/sklampt/echam/test793_ws/test793_50/'.format(run_nr)+'multi_annual_means_test793_50_2003-2003'.format(run_nr)+'.nc')

	# Access variables, e.g.
	d1[parameter[i]]
	d2[parameter[i]]
	#import IPython; IPython.embed()

	# Plotting on a map
	lats = d1['lat'][:]
	lons = d1['lon'][:]

	#lats2 = d2['lat'][:]
	#lons2 = d2['lon'][:]

	#cm = matplotlib.colors.ListedColormap((sns.color_palette("YlGn", n_colors=7)).as_hex())
	cm = matplotlib.colors.ListedColormap((sns.color_palette("vlag", n_colors=7)).as_hex())
	#cmap.set_bad(color='grey', alpha = 1.)

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
	datavar_2 = d2[parameter[i]][0,:,:]
	datavar_diff = datavar_2 - datavar

	levels = np.linspace(0,50,5)
	norm = matplotlib.colors.BoundaryNorm(levels, ncolors=cm.N, clip=True)
	im = ax.contourf(lons, lats, datavar_diff[:, :], cmap=cm, transform=ccrs.PlateCarree())#,  zorder=2)
	cbar = fig.colorbar(im, orientation='horizontal')
	cbarlabel = str(parameter[i] + ' (k)')
	cbar.set_label(cbarlabel)

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

	### TODO: update destination folder
	plt.savefig('/net/n2o/wolke_scratch/sklampt/echam/plots/drastic/test793_50/difference/'.format(run_nr)+'/plot_{}.pdf'.format(plot_name), bbox_inches='tight')
