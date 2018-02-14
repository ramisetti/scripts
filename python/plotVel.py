#!/usr/bin/env python

#### IMPORTANT NOTE: This script works only with python version 3 or greater
#### This script writes an output file and plots the velocity profiles
#### USAGE: python plotVel.py inputFile1 inputFile2 ... inputFileN

#### import packages
import sys,os,string
import numpy as np
import matplotlib.pyplot as plt
import itertools

#### parse file
def parseFile(lines,x_col_id,y_col_id):
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

          elems.append([X,Y])
        else:
          step.append(float(words[0]))

    return np.array(elems),np.array(step)

#### plot function
def plotProfile(elems,step):
    a=elems
    numPts=int(a.shape[0]/len(step))

    # plot velocity profiles on a single figure
    marker = itertools.cycle((',', '+', '.', 'o', '*', '^', 'v', '>', '<', 'x', 'D', 'h', 'd')) 
    labels = []
    for i in range(0,len(step)):
        #plt.plot(a[i*numPts:(i+1)*numPts,0], a[i*numPts:(i+1)*numPts,1], marker=marker.next()) # for python version < 3.0
        plt.plot(a[i*numPts:(i+1)*numPts,0], a[i*numPts:(i+1)*numPts,1], marker=next(marker))
        labels.append('ts = %i' % ((i+1)*1e5))
        plt.legend(labels, ncol=4, loc='upper center', 
                   bbox_to_anchor=[0.5, 1.1], 
                   columnspacing=1.0, labelspacing=0.0,
                   handletextpad=0.0, handlelength=1.5,
                   fancybox=True, shadow=True)

#### main function
def main():
    N=len(sys.argv)
    if N < 2:
        sys.exit("Syntax: python plotVel.py inputFile1 inputFile2 ... inputFileN")

    for i in range(1,N):
        inFileName = sys.argv[i]
        inFile = open(inFileName, "r")
        lines = inFile.readlines()
        inFile.close()

        if 'Coord1' in lines[2]:
            x_col_id = lines[2].split().index('Coord1')-1
        if 'vx' in lines[2]:
            y_col_id = lines[2].split().index('vx')-1

        elems,step = parseFile(lines,x_col_id,y_col_id)
        plotProfile(elems,step)

#### function to plot density profile produced using lammps fix ave/chunk command
def plotDens():
    N=len(sys.argv)
    if N < 2:
        sys.exit("Syntax: python plotVel.py inputFile1 inputFile2 ... inputFileN")

    for i in range(1,N):
        inFileName = sys.argv[i]
        inFile = open(inFileName, "r")
        lines = inFile.readlines()
        inFile.close()

        if 'Coord1' in lines[2]:
            x_col_id = lines[2].split().index('Coord1')-1
        if 'density/mass' in lines[2]:
            y_col_id = lines[2].split().index('density/mass')-1

        elems,step = parseFile(lines,x_col_id,y_col_id)
        plotProfile(elems,step)

if __name__ == "__main__":
    main()
    plt.show()
