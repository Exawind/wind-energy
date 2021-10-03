#!/usr/bin/env python
#

amrwindfedir = '/projects/hfm/lcheung/amrwind-frontend/'
import sys, os
sys.path.insert(1, amrwindfedir)
sys.path.insert(1, '../utilities')

# Load the libraries
import amrwind_frontend  as amrwind
import numpy             as np
import postproamrwindsample as ppsample
import SOWFAdata as sowfa

profiledir = 'profiledata'
casedir    = './'
prefix     = 'AMRWind_winterunstable_'
#timevec=[48, 72, 96, 108, 144]   # Every 12 iter is 1 hr
timevec=[12*(x+1) for x in range(12)]   # Every 12 iter is 1 hr

# Load some SOWFA data
SOWFAdir  = '../SOWFA-WRFforcing/winter-unstable/drivingData/'
Tfile     = SOWFAdir+'/givenSourceT'
sowfatime, sowfatemp = sowfa.readsection(Tfile, 'sourceTableTemperature',
                                         splitfirstcol=True)

# Start the amrwind_frontend app 
tutorial2 = amrwind.MyApp.init_nogui()
tutorial2.ABLpostpro_loadnetcdffile(casedir+'/post_processing/abl_statistics00000.nc')

for it, time in enumerate(timevec):
    print('Time = %0.1f'%sowfatime[time])
    plotvars=['velocity', 'Uhoriz', 'Temperature', 'TKE', 'ReStresses', 'Tfluxes']
    #plotvars=['Temperature', 'velocity']
    dat=tutorial2.ABLpostpro_plotprofiles(ax=None, plotvars=plotvars,
                                          avgt=[sowfatime[time]-5, sowfatime[time]+5], 
                                          doplot=False)
    for k, g in dat.items(): print(k)
    # Write velocity profiles
    writedat=np.vstack((dat['u']['z'], 
                        dat['u']['data'], 
                        dat['v']['data'], 
                        dat['w']['data'],
                        dat['Uhoriz']['data']
                    ))
    filename=profiledir+'/'+prefix+'velocity_%06.0f.dat'%sowfatime[time]
    np.savetxt(filename, writedat.transpose(), header='z u v w uhoriz')

    # Write temperature profiles
    writedat=np.vstack((dat['T']['z'], dat['T']['data']))
    filename=profiledir+'/'+prefix+'temperature_%06.0f.dat'%sowfatime[time]
    np.savetxt(filename, writedat.transpose(), header='z T')

    # Write the Reynolds stresses
    writedat=np.vstack((dat['uu']['z'], 
                        dat['uu']['data'], 
                        dat['uv']['data'], 
                        dat['uw']['data'], 
                        dat['vv']['data'], 
                        dat['vw']['data'],
                        dat['ww']['data'], 
                        dat['TKE']['data'], 
                    ))
    filename=profiledir+'/'+prefix+'reynoldsstresses_%06.0f.dat'%sowfatime[time]
    np.savetxt(filename, writedat.transpose(), header='z uu uv uw vv vw ww TKE')

    # Write Tflux profiles
    writedat=np.vstack((dat['uT']['z'], 
                        dat['uT']['data'], 
                        dat['vT']['data'], 
                        dat['wT']['data'],
                    ))
    filename=profiledir+'/'+prefix+'temperaturefluxes_%06.0f.dat'%sowfatime[time]
    np.savetxt(filename, writedat.transpose(), header='z uT vT wT')
