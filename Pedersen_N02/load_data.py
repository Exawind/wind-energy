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

    spectra_files = glob.glob(dir_name+'/*spectra*dat')
    self.ps_data = {
      'z': np.array(sorted([ float(pathlib.Path(i).with_suffix('').name.split('_')[-1][1:]) for i in spectra_files])),
      'f': pd.read_csv(spectra_files[0],sep='\s+',skiprows=1,header=None,usecols=[0]).values[:,0],
      'suu': np.array([pd.read_csv(i,sep='\s+',skiprows=1,header=None,usecols=[1]).values[:,0] for i in spectra_files ] ),
      'svv': np.array([pd.read_csv(i,sep='\s+',skiprows=1,header=None,usecols=[2]).values[:,0] for i in spectra_files ] ),
      'sww': np.array([pd.read_csv(i,sep='\s+',skiprows=1,header=None,usecols=[3]).values[:,0] for i in spectra_files ] )
    }
    self.istats = {
      'ustar': 0.329179,
      'wstar': 0.0,
      'L': 0.0,
      'Q': 0.0,
      'Tsurf': 0.0,
      'zi': 543.0
    }

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
  def __init__(self, dir_name):
    self.istats = yaml.load(open(dir_name+'/istats.yaml'),Loader=yaml.BaseLoader)
    a = pd.read_csv(dir_name+'/umag_pederesen2014.txt',header=None,names=['hvelmag','z'],dtype=float)
    self.z = a['z'].values * float(self.istats['zi'])
    self.hvelmag = a['hvelmag'].values
    a = pd.read_csv(dir_name+'/temperature_pedersen2014.txt',header=None,names=['T','z'],dtype=float)
    self.T = np.interp(self.z, a['z'].values[::-1], a['T'].values[::-1])

        
