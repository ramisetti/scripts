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

def nextpow2(n):
    tmp = 1
    while tmp < n:
        tmp = tmp << 1
    return tmp

parser = argparse.ArgumentParser(description='Plot power spectral density profiles of OpenFAST output data.\n\
Tested with Python 2.7.5',formatter_class=RawTextHelpFormatter)
parser.add_argument('-f', '--file', nargs='+', required=True, help = "Can accespt one or more input data files. Atleast one file should be mentioned")
parser.add_argument('-t', '--timestep', nargs='?', type=float, default='0.05', help = "(default: %(default)s), Timestep (dt) will define sampling frequency")
parser.add_argument('-c', '--column', nargs='?', type=str, default='Wave1Elev', help = "(default: %(default)s), Data column/field name")
parser.add_argument('-N', '--nsamples', nargs='?', type=int, default='72000', help = "(default: %(default)s), Number of sampled points (N)")
parser.add_argument('-fL', '--freqMin', nargs='?', type=float, default='0.0', help = "(default: %(default)s), Minimum frequency for the frequency scale (x-axis)")
parser.add_argument('-fH', '--freqMax', nargs='?', type=float, default='0.5', help = "(default: %(default)s), Nquist or maximum frequency for the frequency scale (x-axis)")
args = parser.parse_args()
print(args)

dt=args.timestep # timestep
Fs=1.0/dt # sampling frequency
N=args.nsamples # number of sampling points
fL=args.freqMin
fH=args.freqMax
column_name=args.column
listOfData=[]
filenames=sys.argv[1:]
for i in args.file:
    filename=str(i)

    # skip the first 6 lines and read the data into df
    df = pd.read_csv(filename, sep='\t', skiprows=6, encoding="utf-8-sig")

    # delete the empty spaces within the header names
    df.columns = df.columns.str.strip().str.replace(' ', '')
    
    # skip the next row with units after the header row
    # and create new df with all columns data in float
    new_df=df.iloc[1:].astype(float)

    # copy the time data
    T=new_df['Time'].head(72000).to_numpy()
    # listofT.append(T)
    ts=T[2]-T[1]
    if ts!=dt:
        dt=ts
        Fs=1.0/dt # recalculate sampling frequency
        print('Changing timestep ',dt,' to match with the time data')

    if N>new_df['Time'].count():
        N=new_df['Time'].count();
        print('Choosing nsamples=',N,' because of smaller data size')

    if not column_name in new_df.columns:
        print("Column with label name ", column_name, " does not exit! Check the label name.")
        exit()

    # copy the WaveElev data and append to list
    WaveElev=new_df[column_name].head(N).to_numpy()

    listOfData.append(WaveElev)

#get the length of time series and consider minimum one
N=min(map(len, listOfData))
print('Length of data to compute PSD: ', N)

if np.mod(N,2)==0:
    half_N=int(N/2)
    #print('EVEN',half_N)
else:
    half_N=int((N+1)/2)
    #print('ODD',half_N)

# set lowest frequency or frequency interval
f_low=1.0/(N*dt)
# set Nquist frequency
fNquist=1/(2*dt)
frequency=np.arange(0,fNquist,f_low)
#print(N,half_N,len(frequency))

for filename, data in zip(args.file, listOfData):
    id=os.path.basename(filename)

    # compute Power Spectrum
    tmp=np.abs(np.fft.fft(data[0:N]))**2
    #print(len(tmp),len(frequency))
    # compute one-sided power dpectral density normalized by Fs*N
    tmp=2.0*tmp/(N*Fs)
    oneside_psd=tmp[0:half_N]
    
    plt.ylabel("PSD (A^2/HZ)")
    plt.xlabel("Frequency (Hz)")
    plt.xlim(xmax = fH, xmin = fL)
    plt.plot(frequency,oneside_psd,label=id+' '+column_name)

# show plot
plt.title("Power spectral density")
plt.legend()
plt.grid()
plt.show()
