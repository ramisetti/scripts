#!/usr/bin/env python

#### IMPORTANT NOTE: This script works only with python version 3 or greater
#### This script plots 2D color maps for lammps 2D data
#### USAGE: python plot2DMap.py inputFile1 timestep

#### import packages
import sys,os,string
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.interpolate import griddata
import itertools
from circle_fitting import *

#### parse file
def parseFile(lines,x_col_id,y_col_id,z_col_id):
    elems = []
    step = []
    # copy X,Y coordinates and density values into array:
    for line in lines:
      if line[0] != '#': # ignore comments
        #words = string.split(line) # for python version < 3.0
        words = line.split()
        if len(words) != 3:
          X = float(words[x_col_id])
          Y = float(words[y_col_id])
          Z = float(words[z_col_id])
          elems.append([X,Y,Z])
        else:
          step.append(float(words[0]))

    return np.array(elems),np.array(step)

#### plot function
def plotProfile(elems,steps,step):
    a=elems
    numPts=int(a.shape[0]/len(steps))

    # plot density map
    a = a[step*numPts:(step+1)*numPts,]
    x = a[:,0]
    y = a[:,1]
    z = a[:,2]

    shape = np.unique(x).shape[0],np.unique(y).shape[0]
    x_arr = x.reshape(shape)
    y_arr = y.reshape(shape)
    z_arr = z.reshape(shape)

    xnew = np.linspace(np.min(x),np.max(x),shape[0]*5)
    ynew = np.linspace(np.min(y),np.max(y),shape[1]*5)
    X,Y = np.meshgrid(xnew,ynew)

    plt.contourf(x_arr, y_arr, z_arr,cmap=cm.hot)
    plt.colorbar()
    plt.title('2D density map')

    plt.show()		

#### main function
def main():
    N=len(sys.argv)
    if N < 2:
        sys.exit("Syntax: python plot2DMap.py inputFile timestep")

    inFileName = sys.argv[1]
    inFile = open(inFileName, "r")
    lines = inFile.readlines()
    inFile.close()

    if 'Coord1' in lines[2]:
		x_col_id = lines[2].split().index('Coord1')-1
    if 'Coord2' in lines[2]:
		y_col_id = lines[2].split().index('Coord2')-1
    if 'density/mass' in lines[2]:
		z_col_id = lines[2].split().index('density/mass')-1

    elems,steps = parseFile(lines,x_col_id,y_col_id,z_col_id)
    for i in range(2,N):
		plotProfile(elems,steps,int(sys.argv[i]))
	
if __name__ == "__main__":
    main()
    plt.show()

