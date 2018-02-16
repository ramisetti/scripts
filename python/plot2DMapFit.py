#!/usr/bin/env python

#### IMPORTANT NOTE: This script works only with python version 3 or greater
#### This script plots 2D color maps for lammps 2D data
#### USAGE: python plot2DMapFit.py inputFile1 timesteps

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
    # copy coordinates and velocity into array:
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
def plotProfile(elems,steps,step,dens,bbox):
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

    Z = griddata((x, y), z, (X, Y), method='linear')
    plt.contourf(X, Y, Z,10,cmap=cm.hot)
    plt.colorbar()
    plt.title('2D density map with circular fitting')

    # X=X[np.where((Z>=dens[0]) & (Z<=dens[1]))]
    # Y=Y[np.where((Z>=dens[1]) & (Z<=dens[1]))]
    X=X[np.where((Z>=dens[0]) & (Z<=dens[1]))]
    Y=Y[np.where((Z>=dens[0]) & (Z<=dens[1]))]

    X=X[np.where((Y>=bbox[2]) & (Y<=bbox[3]))]
    Y=Y[np.where((Y>=bbox[2]) & (Y<=bbox[3]))]
    X=X[np.where((X>=bbox[0]) & (X<=bbox[1]))]
    Y=Y[np.where((X>=bbox[0]) & (X<=bbox[1]))]
    print(X.shape,Y.shape)
    print(X.shape,Y.shape)

    plt.plot(X,Y,'go')
    XC,YC,R,std_R=circle_fitting(X,Y)
    #XC1,YC1,R1,std_R1=circle_fitting_leastsq(X,Y)
    print(XC,YC,R,std_R)
    #print(XC1,YC1,R1,std_R1)
    theta_fit = np.linspace(-np.pi, np.pi, 180)
    x_fit = XC + R*np.cos(theta_fit)
    y_fit = YC + R*np.sin(theta_fit)

    x_fit=x_fit[np.where(y_fit>10)]
    y_fit=y_fit[np.where(y_fit>10)]
    plt.plot(x_fit, y_fit, 'w-', lw=2)
    plt.show()		

#### main function
def main():
    N=len(sys.argv)
    if N < 2:
        sys.exit("Syntax: python plot2DMapFit.py inputFile dens1 dens2 xmin xmax ymin ymax timestep")

    inFileName = sys.argv[1]
    inFile = open(inFileName, "r")
    lines = inFile.readlines()
    inFile.close()
    dens = [float(sys.argv[2]), float(sys.argv[3])]
    bbox = [float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7])]

    if 'Coord1' in lines[2]:
		x_col_id = lines[2].split().index('Coord1')-1
    if 'Coord2' in lines[2]:
		y_col_id = lines[2].split().index('Coord2')-1
    if 'density/mass' in lines[2]:
		z_col_id = lines[2].split().index('density/mass')-1

    elems,steps = parseFile(lines,x_col_id,y_col_id,z_col_id)    
    for i in range(8,N):
		step=int(sys.argv[i])
		print('plotting density map for timestp %d\n' %step)
		plotProfile(elems,steps,step,dens,bbox)
	
if __name__ == "__main__":
    main()
    plt.show()

