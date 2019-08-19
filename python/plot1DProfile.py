#!/usr/bin/env python

#### IMPORTANT NOTE: This script works only with python version 2.7.5 or greater
#### This script plots the 1D field profiles for data generated using LAMMPS fix ave/chunk
#### USAGE: python plot1DField --help
#### USAGE: python plot1DField -f inputFile1 inputFile2 ... inputFileN

#### import packages
import sys,os,string, argparse 
import numpy as np
import matplotlib.pyplot as plt
import itertools
from argparse import RawTextHelpFormatter

#### parse file
def parseFile(lines,x_col_id,y_col_id):
    elems = []
    steps = []
    # copy x and y fields into array:
    for line in lines:
      if line[0] != '#': # ignore comments
        #words = string.split(line) # for python version < 3.0
        words = line.split()
        if len(words) > 3:
          X = float(words[x_col_id])
          Y = float(words[y_col_id])

          elems.append([X,Y])
        else:
          steps.append(float(words[0]))

    return np.array(elems),np.array(steps)

#### plot function
def plotProfile(elems,steps,steps2plot):
    a=elems
    numPts=int(a.shape[0]/len(steps))

    # plot field profiles on a single figure
    marker = itertools.cycle((',', '+', '.', 'o', '*', '^', 'v', '>', '<', 'x', 'D', 'h', 'd')) 
    labels = []
    print steps2plot
    for step in steps2plot:
	i, = np.where(steps == step)
	if len(i)==0:
	    print ('data for requested timestep does not exist!')
	    sys.exit()
	#plt.plot(a[i*numPts:(i+1)*numPts,0], a[i*numPts:(i+1)*numPts,1], marker=marker.next()) # for python version < 3.0
    	plt.plot(a[i*numPts:(i+1)*numPts,0], a[i*numPts:(i+1)*numPts,1], marker=next(marker))
    	labels.append('ts = %i' % (step))
    	plt.legend(labels, ncol=4, loc='upper center', 
               	   bbox_to_anchor=[0.5, 1.1], 
                   columnspacing=1.0, labelspacing=0.0,
                   handletextpad=0.0, handlelength=1.5,
                   fancybox=True, shadow=True)


#### main function
def main():
    parser = argparse.ArgumentParser(description='Plot 1D profiles from data produced with LAMMPS fix ave/chunk command.\n\
Tested with Python 2.7.5',formatter_class=RawTextHelpFormatter)
    parser.add_argument('-x', '--xfield', nargs='?', type=str, default='Coord1', help = "(default: %(default)s)")
    parser.add_argument('-y', '--yfield', nargs='?', type=str, default='vx', help = "(default: %(default)s), options: vx,vy,vz,density/mass,density/number,Ncount,temp")
    parser.add_argument('-f', '--file', nargs='+', required=True, help = "Can take one or more input files. Atleast one file should be mentioned")
    parser.add_argument('-t', '--timestep', nargs='+', type=int, default='99999', help = "(default: %(default)s) This plots profiles for the requested steps. By default plots profile for the last step")
    parser.add_argument('-pp', '--plotNprofiles', const='5', nargs='?', type=int, help = "(default: %(default)s), Plots N (default N=5) profiles for N regularly spaced timesteps")
    args = parser.parse_args()

    print args
    steps2plot=[]

    for fileName in args.file:
		if not os.path.exists(fileName):
			sys.exit('Data file does not exist!')
		inFile = open(fileName, "r")
		
		lines = inFile.readlines()
		inFile.close()

		options=lines[2].split()
		options.remove('#')
		if args.xfield in options:
			x_col_id = lines[2].split().index(args.xfield)-1
		else:
			print 'xfield value: {} does not exist as a field in the data file! The possible options are: {}'.format(args.xfield, options)
			sys.exit()
		
		if args.yfield in options:
			y_col_id = lines[2].split().index(args.yfield)-1
		else:
			print 'yfield value: {} does not exist as a field in the data file! The possible options are: {}'.format(args.yfield,options)
			sys.exit()
			
		elems,steps = parseFile(lines,x_col_id,y_col_id)

		if args.plotNprofiles is not None:
			N=int(len(steps)/(args.plotNprofiles))
			if N==0: 
				print ('Not enough data! try reducing N')
			else:
				steps2plot=steps[0::N]
		else:
			if args.timestep != 99999 and args.timestep is not None:
				steps2plot=args.timestep
			else:
				steps2plot=[steps[-1]]

		#print (steps2plot)
		plotProfile(elems,steps,steps2plot)

    print ('Happy plotting!')

if __name__ == "__main__":
    main()
    plt.show()
