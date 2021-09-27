#!/usr/bin/env python
# Script to create a wrf profile netCDF file

from netCDF4 import Dataset
import numpy as     np
import sys
from scipy import interpolate

# Add the path to the utilities folder
sys.path.insert(1, '../utilities')
import SOWFAdata as sowfa

def AMRcellcenters(z0, z1, Nz):
    """
    Get the cell centers on the AMR-Wind grid
    """
    dz = (z1-z0)/Nz
    return np.linspace(z0+0.5*dz,z1-0.5*dz,Nz)    

# AMR-Wind grid quantities
z0        = 0
z1        = 1920
Nz        = 192

# Output WRF forcing file
wrffilename = "wrfforcing.nc"

# SOWFA profile directories
SOWFAdir  = '../SOWFA-WRFforcing/summer-stable/drivingData/'
Tfile     = SOWFAdir+'/givenSourceT'
Ufile     = SOWFAdir+'/givenSourceU_component_rotated'
tfluxfile = SOWFAdir+'/surfaceTemperatureFluxTable'

# Load the SOWFA data
zT                   = sowfa.readsection(Tfile, 'sourceHeightsTemperature')
sowfatime, sowfatemp = sowfa.readsection(Tfile, 'sourceTableTemperature',
                                         splitfirstcol=True)

zMom                 = sowfa.readsection(Ufile, 'sourceHeightsMomentum')

t1, sowfa_momu       = sowfa.readsection(Ufile, 'sourceTableMomentumX',
                                         splitfirstcol=True)
t2, sowfa_momv       = sowfa.readsection(Ufile, 'sourceTableMomentumY',
                                         splitfirstcol=True)

t3, sowfa_tflux      = sowfa.readplainfile(tfluxfile, splitfirstcol=True)

print("Loaded SOWFA profiles")

# Check that the times line up
assert np.linalg.norm(sowfatime-t1)<1.0E-8, "sowfatime != t1"
assert np.linalg.norm(sowfatime-t2)<1.0E-8, "sowfatime != t2"
assert np.linalg.norm(sowfatime-t3)<1.0E-8, "sowfatime != t3"

# Flatten some arrays
sowfatime = sowfatime.reshape(len(sowfatime))
zMom      = zMom.reshape(len(zMom))
zT        = zT.reshape(len(zT))

# Construct the AMR-Wind grid at the cell centers
zamr      = AMRcellcenters(z0, z1, Nz)

# Write the netcdf file with WRF forcing
rootgrp = Dataset(wrffilename, "w", format="NETCDF4")
print(rootgrp.data_model)

# Create the heights
heights   = zamr
nheight   = rootgrp.createDimension("nheight", len(heights))
ncheights = rootgrp.createVariable("heights", "f8", ("nheight",))
ncheights[:] = heights

# Create the times
times     = sowfatime
ntime     = rootgrp.createDimension("ntime", len(times))
nctimes   = rootgrp.createVariable("times", "f8", ("ntime",))
nctimes[:] = times
print("Wrote heights and times")

# Add momentum u profiles
nc_momu     = rootgrp.createVariable("wrf_momentum_u", "f8", 
                                     ("ntime", "nheight",))
for i in range(len(times)):
    nc_momu[i,:] = np.interp(zamr, zMom, sowfa_momu[i,:])

# Add momentum v profiles
nc_momv     = rootgrp.createVariable("wrf_momentum_v", "f8", 
                                     ("ntime", "nheight",))
for i in range(len(times)):
    nc_momv[i,:] = np.interp(zamr, zMom, sowfa_momv[i,:])
print("Wrote momentum profiles")

# Add the temperature profiles
nc_temp     = rootgrp.createVariable("wrf_temperature", "f8", 
                                     ("ntime", "nheight",))
for i in range(len(times)):
    nc_temp[i,:] = np.interp(zamr, zT, sowfatemp[i,:])
print("Wrote temperature profiles")

# Add the temperature fluxes
tflux       = sowfa_tflux
nc_tflux    = rootgrp.createVariable("wrf_tflux", "f8", ("ntime",))
# Negative sign because SOWFA convention is opposite AMR-Wind
nc_tflux[:] = -tflux   
print("Wrote tflux profiles")

# Close the file
rootgrp.close()
print("Done")



