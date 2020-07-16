#!/usr/bin/env python

import numpy as np
import sys
import matplotlib.pyplot as plt

def readdata(filename):
    """
    Reads the GABLS data from a text file
    """
    alldata=[]
    with open(filename) as fp:
        comments=fp.readline()  # Read the comment line
        N=int(fp.readline())    # Read the N size
        line=fp.readline()
        while line:
            alldata.extend([float(x) for x in line.split()])
            line=fp.readline()
    # Reshape the array
    newdat=np.reshape(np.array(alldata), (-1,N)).transpose()
    #print(np.shape(newdat))
    return newdat

def plotvel(filename, **kwargs):
    """
    Plots the horizonal velocity from data given in filename
    """
    data=readdata(filename)
    plt.plot(np.sqrt(data[:,1]**2 + data[:,2]**2), data[:,0], **kwargs)


def plotcols(filename, xcol=1, ycol=0, **kwargs):
    """
    Plots some columns from the GABLS file
    """
    data=readdata(filename)
    plt.plot(data[:,xcol], data[:,ycol], **kwargs)
    
