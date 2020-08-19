import numpy as np
import pandas as pd
import glob, yaml, pathlib
from netCDF4 import Dataset
from scipy.interpolate import interp1d

class ABLStats:
  """Generic class that contains abl statistics"""
  def __init__(self):
    self.z = []
    self.u = []
    self.v = []
    self.w = []
    self.hvelmag = []
    self.T = []
    self.istats = {
      'ustar': 0.0,
      'wstar': 0.0,
      'L': 0.0,
      'Q': 0.0,
      'Tsurf': 0.0,
      'zi': 0.0
    }
    self.ps_data = {
      'z': [],
      'f': [],
      'suu': [],
      'svv': [],
      'sww': []
    }

  def interp_hvelmag(self, z):
    return np.interp(z, self.z, self.hvelmag)

  def point_spectra(self, z):
    suu = interp1d(self.ps_data['z'], self.ps_data['suu'],axis=0)(z)
    svv = interp1d(self.ps_data['z'], self.ps_data['svv'],axis=0)(z)
    sww = interp1d(self.ps_data['z'], self.ps_data['sww'],axis=0)(z)
    return self.ps_data['f'], suu, svv, sww
  
class NaluWindStats(ABLStats):
  """ABLStats class specific to NaluWind output"""
  def __init__(self,dir_name):
    vel_file = glob.glob(dir_name+'/*velocity.dat')[0]
    a = pd.read_csv(vel_file, sep='\s+', skiprows=1, names=['z','u','v','w','u_mag'] )
    self.z = a['z'].values
    self.u = a['u'].values
    self.v = a['v'].values
    self.w = a['w'].values
    self.hvelmag = a['u_mag'].values
    temp_file = glob.glob(dir_name+'/*temperature.dat')[0]
    a = pd.read_csv(temp_file, sep='\s+', skiprows=1, names=['z','T'] )
    self.T = a['T'].values
    if (len(glob.glob(dir_name+'/*reynoldsstresses.dat'))>0):
      restress_file = glob.glob(dir_name+'/*reynoldsstresses.dat')[0]
      a = pd.read_csv(restress_file, sep='\s+', skiprows=1, names=['z','uu', 'uv', 'uw','vv','vw','ww','tke'] )
      self.vel_var = {
        "<u'u'>" : a["uu"],
        "<u'v'>" : a["uv"],
        "<u'w'>" : a["uw"],
        "<v'v'>" : a["vv"],
        "<v'w'>" : a["vw"],
        "<w'w'>" : a["ww"],
      }
    else:
      self.vel_var = {
        "<u'u'>" : [],
        "<u'v'>" : [],
        "<u'w'>" : [],
        "<v'v'>" : [],
        "<v'w'>" : [],
        "<w'w'>" : [],
      }
    if (len(glob.glob(dir_name+'/*_temperaturefluxes.dat'))>0):
      tfluxes_file = glob.glob(dir_name+'/*_temperaturefluxes.dat')[0]
      a = pd.read_csv(tfluxes_file, sep='\s+', skiprows=1, names=['z','Tu', 'Tv', 'Tw'] )
      self.tflux_var = {
        "<T'u'>" : a["Tu"],
        "<T'v'>" : a["Tv"],
        "<T'w'>" : a["Tw"],
      }      
    else:
      self.tflux_var = {
        "<T'u'>" : [],
        "<T'v'>" : [],
        "<T'w'>" : [],
      }      
    if (len(glob.glob(dir_name+'/*_sfstemperaturefluxes.dat'))>0):
      tfluxes_file = glob.glob(dir_name+'/*_sfstemperaturefluxes.dat')[0]
      a = pd.read_csv(tfluxes_file, sep='\s+', skiprows=1, names=['z','Tu', 'Tv', 'Tw'] )
      self.sfstflux_var = {
        "<T'u'>" : a["Tu"],
        "<T'v'>" : a["Tv"],
        "<T'w'>" : a["Tw"],
      }      
    else:
      self.sfstflux_var = {
        "<T'u'>" : [],
        "<T'v'>" : [],
        "<T'w'>" : [],
      }      
  
    spectra_files = glob.glob(dir_name+'/*spectra*dat')
    self.ps_data = {
      'z': np.array(sorted([ float(pathlib.Path(i).stem.split('_')[-1][1:]) for i in spectra_files])),
      'f': pd.read_csv(spectra_files[0],sep='\s+',skiprows=1,header=None,usecols=[0]).values[:,0],
      'suu': np.array([pd.read_csv(i,sep='\s+',skiprows=1,header=None,usecols=[1]).values[:,0] for i in spectra_files ] ),
      'svv': np.array([pd.read_csv(i,sep='\s+',skiprows=1,header=None,usecols=[2]).values[:,0] for i in spectra_files ] ),
      'sww': np.array([pd.read_csv(i,sep='\s+',skiprows=1,header=None,usecols=[3]).values[:,0] for i in spectra_files ] )
    }
    try:
      self.istats = yaml.load(open(dir_name+'/istats.yaml'),Loader=yaml.BaseLoader)
    except:
      self.istats = {}

class AMRWindStats(ABLStats):
  """ABLStats class specific to AMRWind output"""
  def __init__(self,dir_name):
    a = pd.read_csv(dir_name+'/line_average_data.csv')
    self.z = a['z'].values
    self.u = a['<u>'].values
    self.v = a['<v>'].values
    self.w = a['<w>'].values
    self.hvelmag = a['<hvelmag>'].values
    self.T = a['<temperature0>'].values
    self.vel_var = {
      "<u'u'>" : a["<u'u'>"],
      "<u'v'>" : a["<u'v'>"],
      "<u'w'>" : a["<u'w'>"],
      "<v'v'>" : a["<v'v'>"],
      "<v'w'>" : a["<v'w'>"],
      "<w'w'>" : a["<w'w'>"],
      "<w'w'w'>": a["<w'w'w'>"]
    }
    self.tflux_var = {
      "<T'u'>" : a["<temperature0'u'>"],
      "<T'v'>" : a["<temperature0'v'>"],
      "<T'w'>" : a["<temperature0'w'>"],
    }      
    self.sfstflux_var = {
      "<T'u'>" : [],
      "<T'v'>" : [],
      "<T'w'>" : [],
    }      
    self.istats = yaml.load(open(dir_name+'/istats.yaml'),Loader=yaml.BaseLoader)

    with Dataset(dir_name+'/avg_spectra.nc') as d:
      self.ps_data = {
        'z': d.variables['z'][:],
        'f': d.variables['f'][:],
        'suu': d.variables['suu'][:,:],
        'svv': d.variables['svv'][:,:],
        'sww': d.variables['sww'][:,:]
      }
    
    
class PedersonData(ABLStats):
  """ABLStats class specific to Pederson2014 data"""
  def __init__(self, dir_name, 
               ufile='Pedersen2014_N07_velocity.csv',
               tfile='Pedersen2014_N07_temperature.csv',
               tfluxfile='',
               skiprows=0):
    self.istats = yaml.load(open(dir_name+'/istats.yaml'),Loader=yaml.BaseLoader)
    a = pd.read_csv(dir_name+'/'+ufile,header=None,skiprows=skiprows,names=['hvelmag','z'],dtype=float)
    self.z = a['z'].values * float(self.istats['zi'])
    self.hvelmag = a['hvelmag'].values
    a = pd.read_csv(dir_name+'/'+tfile,header=None,skiprows=skiprows,names=['T','z'],dtype=float)
    self.T = np.interp(self.z, a['z'].values[:], a['T'].values[:])
    self.vel_var = {
      "<u'u'>" : [],
      "<u'v'>" : [],
      "<u'w'>" : [],
      "<v'v'>" : [],
      "<v'w'>" : [],
      "<w'w'>" : [],
    }

    if len(tfluxfile)>0:
      a = pd.read_csv(dir_name+'/'+tfluxfile,header=None,skiprows=skiprows,names=['wtheta','zh'],dtype=float)
      self.tflux_var = {
        "<T'u'>" : [],
        "<T'v'>" : [],
        "<T'w'>" : np.interp(self.z, a['zh'].values[:]*float(self.istats['zi']), a['wtheta'].values[:]),
      }            
    else:
      self.tflux_var = {
        "<T'u'>" : [],
        "<T'v'>" : [],
        "<T'w'>" : [],
      }      
    self.sfstflux_var = {
      "<T'u'>" : [],
      "<T'v'>" : [],
      "<T'w'>" : [],
    }      
