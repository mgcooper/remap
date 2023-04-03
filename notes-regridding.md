# Regridding

## tools

- ESMPy
- pangeo-data/xESMF (calls ESMPy) (JiaweiZhuang)
- leifdenby/regridcart (calls xESMF and pyregridder)
- NOAA-ORR-ERD/gridded ()
- MPAS-Dev/pyremap
- pytroll/pyresample (nominally for Satpy library geospatial image data resampling)
- CDO
- NCO
- remapper

[Pyremap](https://mpas-dev.github.io/pyremap/stable/quick_start.html) was suggested in land group meeting

## notes

- my recollection is that regridcart seems like the easiest
- not complete packages but useful:
  - Python-CDO-grid

Tips for Sarah:

- need hourly or 3 hourly data
- interpolating to common time vector
- mass units, converting to common units
- conservative remapping / grid types
- converting to cumulative runoff
- rounding
- ice mask edge effects

ncclimo/ncremap
remember to use -P elm option to avoid subgrid issues (need to follow up on this)
