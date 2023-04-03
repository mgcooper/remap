import regridcart as rc
import xarray as xr
import numpy as np
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cmocean.cm as cmo
import hvplot.xarray
import geoviews as gv

# PICK UP
# need the crs of mar, it should be in a 'grid-mapping' variable but there isn't one, need to search through old notes 

# %% open the dataset and get the main info
ds = xr.open_dataset("/Users/coop558/work/data/greenland/mar3.11/MARv3.11-ERA5-15km-2018.nc")

# try to assing the lat.lon to x,y coords
ds = ds.assign_coords(lon=ds.LON,lat=ds.LAT)

# other options: chunks, chunksizes, dtypes, encoding, imag, loc, nbytes, real, xindexes
variables = ds.data_vars
dims = ds.dims
atts = ds.attrs
coords = ds.coords
idxs = ds.indexes
sizes = ds.sizes
time = ds.TIME

# %% build a time array
t1 = datetime(2018,1,1,0,0,0)
t2 = datetime(2019,1,1,0,0,0)
dt = timedelta(hours=1)
t = np.arange(t1,t2,dt).astype(datetime)

# %% read the melt and runoff for a single grid cell

# idx 54,21 should be good ones for cheecking based on ncrowcol but don't seem to be 
melt = ds.MEH.sel(Y21_199=54,X10_105=21,method='nearest')
melt = melt.values.flatten()
melt = np.cumsum(melt/1000)
plt.plot(t,melt)

# get the lat lon value for the grid cell
latp = ds.LAT.sel(Y21_199=54,X10_105=21,method='nearest')
lonp = ds.LON.sel(Y21_199=54,X10_105=21,method='nearest')

# %% read the melt and runoff for a single grid cell using the lat lon values

# extract all lat lon values from the ds
latv = ds.LAT.values.flatten()
lonv = ds.LON.values.flatten()

# set the lat lon for the point
lat0 = 67.035
lon0 = -48.90

# find the index of the point on the grid
idx = np.argmin(np.abs(latv-lat0)+np.abs(lonv-lon0))

# get the melt timeseries for the point
melt = ds.MEH.values.flatten()[idx]

# plot the melt timeseries
melt = np.cumsum(melt/1000)
plt.plot(melt)

# this selects one grid cell and flattens but the values are all zero
# runoff = ds.MEH.sel(Y21_199=54,X10_105=21,method='nearest')
# runoff = runoff.values.flatten()
# pl.plot(t,runoff)
# runoff.max()

# %% compute the time-average and make a map

# I could not figure out how to unstack with xarray, so use np (converts to ndarray)
MEH = ds.MEH/1000
MEH = MEH.stack(hour=('TIME','ATMXH'))
MEH = MEH.cumsum(dim='hour')
MEH = MEH.mean(dim='hour')

# MEH = np.vstack(MEH)
# MEH = np.cumsum(MEH,axis=0)
# MEH = np.mean(MEH,axis=0)

fig, ax = plt.subplots()
MEH.plot(x='lon',y='lat')

fig, ax = plt.subplots()
MEH.plot()

# add a symbol for the location of the time series
ax.plot(-41.18,71.4,'r*',transform=ccrs.PlateCarree())


# %% make a map

# proj = ccrs.NorthPolarStereo(central_longitude=-40,true_scale_latitude=70)
# proj = ccrs.Stereographic(central_latitude=70,central_longitude=-40)
# proj = ccrs.NorthPolarStereo()
coast_10m = cfeature.NaturalEarthFeature('physical', 'land', '10m',
                                        edgecolor='k', facecolor='0.8')
proj = ccrs.LambertConformal()
fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(10, 5),
                       subplot_kw={'projection': proj})
MEH.plot(x='lon', y='lat',transform=proj,cmap=cmo.haline, ax=ax)
# ax.add_feature(coast_10m)
ax.set_extent([-70, -40, 60, 75], crs=proj)
ax.set_title('')
gl = ax.gridlines(draw_labels=True, x_inline=False, y_inline=False, 
                  xlocs=np.arange(-70,-40, 5), ylocs=np.arange(60, 75, 5))

# manipulate `gridliner` object to change locations of labels
gl.top_labels = False
gl.right_labels = False


# %%

# lat0 = ds.lat.mean()
# lon0 = ds.lon.mean()

target_domain = rc.LocalCartesianDomain(
    central_latitude=71.4,
    central_longitude=-41.18,
    l_meridional=3000.0e3,
    l_zonal=2000.0e3,
)
target_domain.plot_outline()
# target_domain.latlon_bounds


dx = 15.0e3 # new resoluion 1km
da_regridded = rc.resample(target_domain, da=MEH, dx=dx)


fig, ax = plt.subplots()
da_regridded.plot()


# %%
