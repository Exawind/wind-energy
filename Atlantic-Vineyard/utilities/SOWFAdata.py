#!/usr/bin/env python
#

from netCDF4 import Dataset
import numpy as     np
import sys
from scipy import interpolate

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

sanitizeline = lambda x: x.replace('(','').replace(')','').replace(';','').strip().split()

def readsection(filename, key, splitfirstcol=False):
  """
  """
  output=[]
  with open(filename, 'r') as f:
    alllines=f.readlines()
    i=0
    while i<len(alllines):
      cleanline = sanitizeline(alllines[i])
      if (len(cleanline)>0) and cleanline[0]==key:
        # Found the key
        #print('%i %s'%(i, cleanline[0]))
        while True:
          i=i+1
          if (i>=len(alllines)):  
            #print('%i reached the end of file'%i)
            break
          nextline = sanitizeline(alllines[i])
          if len(nextline)==0:
            #print('%i empty, skipping'%i)
            continue
          if len(nextline)>0 and isfloat(nextline[0]):
            #print('%i has %s'%(i, repr(nextline)))
            output.append([float(x) for x in nextline])
          else:
            #print('%i is a word: %s'%(i, repr(nextline)))
            break
      i=i+1
  npoutput =  np.array(output)
  if splitfirstcol:
    return npoutput[:,0], npoutput[:,1:]
  else:
    return npoutput


def readplainfile(filename, splitfirstcol=False):
  output=[]
  with open(filename, 'r') as f:
    alllines=f.readlines()
    i=0
    while i<len(alllines):
      cleanline = sanitizeline(alllines[i])
      if (len(cleanline)>0):
        output.append([float(x) for x in cleanline])
      i=i+1
  npoutput =  np.array(output)
  if splitfirstcol:
    return npoutput[:,0], npoutput[:,1:]
  else:
    return npoutput


if __name__ == "__main__":
  # TEST functions here
  z         = readsection('atlantic-vineyard/winter-unstable/drivingData/givenSourceT', 
                          'sourceHeightsTemperature')
  print(z.shape)
  print(z.reshape(len(z)))
  time,temp = readsection('atlantic-vineyard/winter-unstable/drivingData/givenSourceT', 
                        'sourceTableTemperature', splitfirstcol=True)
  print(time.shape, temp.shape)
  print(time)
  print(temp)
  
  time, tflux = readplainfile('atlantic-vineyard/summer-stable/drivingData/surfaceTemperatureFluxTable', splitfirstcol=True)
  print(time.shape, tflux.shape)
  print(time)
