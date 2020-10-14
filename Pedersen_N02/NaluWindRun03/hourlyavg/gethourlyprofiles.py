# Important header information
naluhelperdir = '../../../utilities/'
# Import libraries
import sys
import numpy as np
import matplotlib.pyplot as plt
sys.path.insert(1, naluhelperdir)
import plotABLstats
import yaml as yaml
#from IPython.display import Image
from matplotlib.lines import Line2D
import matplotlib.image as mpimg

# Nalu-wind parameters
rundir    = '/gpfs1/ahsieh/Wind/HFMQ3ABL/Neutral_OneEq'
statsfile = 'abl_statisticsC.nc'

# Nalu-wind parameters
rundir    = '/gpfs1/ahsieh/Wind/HFMQ3ABL/Neutral_OneEq'
statsfile = 'abl_statisticsC.nc'
#avgtimes  = [111600, 115200]  # Average from 31hr to 32hr of run-time
avgtimeshr = [
            # [24, 25],
            #  [25, 26],
              [26, 27],
              [27, 28],
              [28, 29],
              [29, 30],
              [30, 31],
              [31, 32]]
allavgtimes = [[x[0]*3600, x[1]*3600] for x in avgtimeshr]

#print(allavgtimes)

# Load the initial data
data             = plotABLstats.ABLStatsFileClass(stats_file=rundir+'/'+statsfile);

for avgtimes in allavgtimes:
    prefix = "%06i"%avgtimes[0]
    print("start time: %s"%prefix)
    print("end time:   %06i"%avgtimes[1])
    # Load nalu-wind data
    Vprof, vheader    = plotABLstats.plotvelocityprofile(data, None, tlims=avgtimes, exportdata=True)
    Tprof, theader    = plotABLstats.plottemperatureprofile(data, None, tlims=avgtimes, exportdata=True)
    # Extract TKE and Reynolds stresses
    REstresses, REheader    = plotABLstats.plottkeprofile(data, None, tlims=avgtimes, exportdata=True)
    # Extract Utau
    avgutau = plotABLstats.avgutau(data, None, tlims=avgtimes)
    print('Avg Utau = %f'%avgutau)
    # Calculate the inversion height
    try: 
        zi, utauz = plotABLstats.calcInversionHeight(data, [750.0], tlims=avgtimes)
    except:
        zi = 0.0
    print('zi = %f'%zi)
    

    # Export the Nalu-Wind data for other people to compare
    np.savetxt('NaluWind_N02_%s_velocity.dat'%prefix,         
               Vprof,      header=vheader)
    np.savetxt('NaluWind_N02_%s_temperature.dat'%prefix,      
               Tprof,      header=theader)
    np.savetxt('NaluWind_N02_%s_reynoldsstresses.dat'%prefix, 
               REstresses, header=REheader)
    
    savedict={'zi':float(zi), 'ustar':float(avgutau)}
    f=open('istats_%s.yaml'%prefix,'w')
    f.write('# Averaged quantities from %f to %f\n'%(avgtimes[0], avgtimes[1]))
    f.write(yaml.dump(savedict, default_flow_style=False))
    f.close()
