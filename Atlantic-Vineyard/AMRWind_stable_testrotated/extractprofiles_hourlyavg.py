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
prefix     = 'AMRWind_summerstable_'
timevec = range(12) # [0, 1, ... 11] in hours

# Start the amrwind_frontend app 
tutorial2 = amrwind.MyApp.init_nogui()
tutorial2.ABLpostpro_loadnetcdffile(casedir+'/post_processing/abl_statistics00000.nc')

for it, time in enumerate(timevec):
    avgtime = [(time)*3600, (time+1)*3600 ] 

    print('Averaging %i hr to %i hr'%(time, time+1))
    plotvars=['velocity', 'Uhoriz', 'Temperature', 'TKE', 'ReStresses', 'Tfluxes']
    #plotvars=['Temperature', 'velocity']
    dat=tutorial2.ABLpostpro_plotprofiles(ax=None, plotvars=plotvars,
                                          avgt=avgtime, 
                                          doplot=False)
    for k, g in dat.items(): print(k)
    # Write velocity profiles
    writedat=np.vstack((dat['u']['z'], 
                        dat['u']['data'], 
                        dat['v']['data'], 
                        dat['w']['data'],
                        dat['Uhoriz']['data']
                    ))
    filename=profiledir+'/'+prefix+'velocity_avg_%i_to_%i.dat'%(time, time+1)
    np.savetxt(filename, writedat.transpose(), header='z u v w uhoriz')

    # Write temperature profiles
    writedat=np.vstack((dat['T']['z'], dat['T']['data']))
    filename=profiledir+'/'+prefix+'temperature_avg_%i_to_%i.dat'%(time, time+1)
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
    filename=profiledir+'/'+prefix+'reynoldsstresses_avg_%i_to_%i.dat'%(time, time+1)
    np.savetxt(filename, writedat.transpose(), header='z uu uv uw vv vw ww TKE')

    # Write Tflux profiles
    writedat=np.vstack((dat['uT']['z'], 
                        dat['uT']['data'], 
                        dat['vT']['data'], 
                        dat['wT']['data'],
                    ))
    filename=profiledir+'/'+prefix+'temperaturefluxes_avg_%i_to_%i.dat'%(time, time+1)
    np.savetxt(filename, writedat.transpose(), header='z uT vT wT')
