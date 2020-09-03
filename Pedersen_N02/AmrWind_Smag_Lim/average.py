import matplotlib 
matplotlib.use('Agg')
import itertools, windspectra, postproamrwind, glob, yaml
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import numpy as np
from mpi4py import MPI
from netCDF4 import Dataset
from multiprocessing import Pool


def calc_average_profile_last_hour():
  a = Dataset(sorted(glob.glob('post_processing/abl_statistics*nc'))[-1])
  tstart_idx = np.searchsorted(a.variables['time'][:],111600.0)
  mean_profiles = a.groups['mean_profiles']
  vars = list(mean_profiles.variables)[1:]
  b = pd.DataFrame({ v: np.average(mean_profiles[v][tstart_idx:,:],axis=0) for v in vars})
  b['z'] = mean_profiles['h'][:]
  b.to_csv('line_average_data.csv')

def calc_average_istats_last_hour():
  a = Dataset(sorted(glob.glob('post_processing/abl_statistics*nc'))[-1])
  vars = list(a.variables.keys())[1:]
  i_stats = { v: float(np.average( a.variables[v][ a.variables['time'][:] > 111600.0] )) for v in vars}
  yaml.dump( i_stats, open('istats.yaml','w'), default_flow_style=False)

  
def calc_average_spectra_last_hour():
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  nprocs = comm.Get_size()
  
  a = Dataset(sorted(glob.glob('post_processing/*nc'))[-1])
  z = a.groups['l_v11'].variables['coordinates'][:100,2]
  nz = np.size(z)
  tttime = a.variables["time"][:]
  start_idx = np.searchsorted(tttime, 111600)
  time = tttime[start_idx:]
  l_groups = ['l_v11','l_v12','l_v13','l_v21','l_v22','l_v23','l_v31','l_v32','l_v33']

  #Figure out levels on which the current proc will operate
  r_iz = np.where( (np.linspace(0,nz-1,nz,dtype=int)%nprocs - rank) == 0)[0]
    
  f = windspectra.getWindSpectra(time, a.groups['l_v11'].variables['velocityx'][start_idx:,0 ])[0]

  with Dataset('avg_spectra.nc',mode='w',parallel=True,format='NETCDF3_CLASSIC') as d:
    d.createDimension("nz",nz)
    d.createDimension("nfreq",np.size(f))
    nc_f = d.createVariable("f","f8",("nfreq",))
    nc_z = d.createVariable("z","f8","nz")
    nc_suu = d.createVariable("suu","f8",("nz","nfreq"))
    nc_svv = d.createVariable("svv","f8",("nz","nfreq"))
    nc_sww = d.createVariable("sww","f8",("nz","nfreq"))

    if (rank == 0):
        nc_f[:] = f
        nc_z[:] = z

    for h in r_iz:
      nc_suu[h,:] = np.average([windspectra.getWindSpectra(time, a.groups[l].variables['velocityx'][start_idx:,h])[1] for l in l_groups],axis=0)
      nc_svv[h,:] = np.average([windspectra.getWindSpectra(time, a.groups[l].variables['velocityy'][start_idx:,h])[1] for l in l_groups],axis=0)
      nc_sww[h,:] = np.average([windspectra.getWindSpectra(time, a.groups[l].variables['velocityz'][start_idx:,h])[1] for l in l_groups],axis=0)

  
def plot_line_averages():
    a = pd.read_csv('line_average_data.csv')
    plt.style.use('singleColumn')
    with PdfPages('line_average_data.pdf') as pfpgs:
        for c in a.columns[4:]:
            fig = plt.figure()
            plt.plot(a[c],a['z'])
            plt.grid()
            plt.xlabel('z')
            plt.ylabel(c)
            plt.tight_layout()
            pfpgs.savefig()
            plt.close(fig)


if __name__=="__main__":
  calc_average_profile_last_hour()
  calc_average_istats_last_hour()
  calc_average_spectra_last_hour()
  #plot_line_averages()
  
