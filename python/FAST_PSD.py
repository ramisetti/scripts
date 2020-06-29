#############################################################
#	Plot Power Spectral Density of OpenFAST outputs     #
#	Authors: Srinivasa B. Ramisetti, Ramya N.	    #
#	Created:   27-June-2020		  	            #
#	E-mail: ramisettisrinivas@yahoo.com		    #
#	Web:	http://ramisetti.github.io		    #
#############################################################
#!/usr/bin/env python

import os,sys,argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from argparse import RawTextHelpFormatter

parser = argparse.ArgumentParser(description='Plot power spectral density profiles of OpenFAST output data.\n\
Tested with Python 2.7.5',formatter_class=RawTextHelpFormatter)
parser.add_argument('-f', '--file', nargs='+', required=True, help = "Can accespt one or more input data files. Atleast one file should be mentioned")
parser.add_argument('-dt', '--timestep', nargs=1, type=float, default='0.05', help = "(default: %(default)s), Timestep (dt) will define sampling frequency")
parser.add_argument('-N', '--nsamples', nargs=1, type=int, default='72000', help = "(default: %(default)s), Number of sampled points (N)")
parser.add_argument('-fL', '--freqMin', nargs=1, type=float, default='0.0', help = "(default: %(default)s), Minimum frequency for the frequency scale (x-axis)")
parser.add_argument('-fH', '--freqMax', nargs=1, type=float, default='0.5', help = "(default: %(default)s), Nquist or maximum frequency for the frequency scale (x-axis)")
args = parser.parse_args()
print(args)

dt=args.timestep # timestep
N=args.nsamples # number of sampling points
fL=args.freqMin
fH=args.freqMax
listofT=[]
listofPSD=[]
filenames=sys.argv[1:]
for i in args.file:
    filename=str(i)
    #print(type(filename))

    # skip the first 6 lines and read the data into df
    df = pd.read_csv(filename, sep='\t', skiprows=6, encoding="utf-8-sig")

    # delete the empty spaces within the header names
    df.columns = df.columns.str.strip().str.replace(' ', '')
    
    # skip the next row with units after the header row
    # and create new df with all columns data in float
    new_df=df.iloc[1:].astype(float)

    # copy the time data and append to list
    # T=new_df['Time'].head(72000).to_numpy()
    # listofT.append(T)

    if N>new_df['Time'].count():
        N=new_df['Time'].count();
        print('Choosing nsamples=',N,' because of smaller data size')

    # copy the WaveElev data and append to list
    WaveElev=new_df['Wave1Elev'].head(N).to_numpy()

    # compute Power Spectrum
    tmp=np.abs(np.fft.fft(WaveElev))**2
    #N=len(T)
    # compute one-sided power dpectral density normalized by N*N
    tmp=2.0*tmp/(N*N)
    listofPSD.append(tmp)

# get the length of time series and consider minimum one
# N=min(map(len, listofPSD))
#print(N)

if np.mod(N,2)==0:
    half_N=int(N/2+1)
else:
    half_N=int((N+1)/2)

# set lowest frequency or frequency interval
f_low=1.0/(N*dt)
# set Nquist frequency
fNquist=1/(2*dt)
frequency=np.arange(0,fNquist,f_low)

for filename, PSD in zip(args.file, listofPSD):
    id=os.path.basename(filename)
    oneside_psd=PSD[1:half_N]
    plt.ylabel("PSD (A^2/HZ)")
    plt.xlabel("Frequency (Hz)")
    plt.xlim(xmax = fH, xmin = fL)
    plt.plot(frequency,oneside_psd,label=id+' N*N')
    #plt.plot(frequency,oneside_psd*N*dt,label=id+' Fs*N')

# show plot
plt.title("Power spectral density")
plt.legend()
plt.show()
