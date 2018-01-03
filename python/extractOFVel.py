#### IMPORTANT NOTE: this script should be only used
#### after running the OFToCSV.py script which generates
#### the cfd_vel_* files

#### USAGE: python genCFDVel.py 

#### import packages
import os,sys,glob
import numpy as np
import matplotlib.pyplot as plt
import itertools
import pandas as pd

#cols_to_keep = ['Points:1', 'pMean', 'UMean:0', 'UMean:1', 'UMean:2']
cols_to_keep = ['Points:1', 'p', 'U:0', 'U:1', 'U:2']
# open each file created using OFToCSV script
# and extract velocity profile along y-direction
df=pd.DataFrame(data=None,columns=[cols_to_keep])
df.loc[len(df)]=['# Time averaged data', '','','','']
df.loc[len(df)]=['# Timestep Number-of-chunks XXX', '','','','']
df.loc[len(df)]=['# Coord1 p vx vy vz', '','','','']
step=[]
df_temp=pd.DataFrame(data=None,columns=[cols_to_keep])

file_list = glob.glob("cfd_vel_0.*.csv")
file_list.sort(key=lambda x: int(x.split('.')[1]))
for filename in file_list:
	# extract timestep from filename
	time=int(os.path.splitext(filename)[0].split('.')[1])
    # ignore zero timestep data to be consistent with lammps data
	if (time==0): continue
	step.append(time)

	data=pd.read_csv(filename)
	data['Points:1']/=3.4e-10
    #data['Points:1']+=9.0
	group=data[cols_to_keep].groupby('Points:1',as_index = False).mean()
	df_temp.loc[len(df_temp)] = [time, 'XXX', 'XXX', '','']
	df_temp=df_temp.append(group)


df = df.append(df_temp)
df = df.reset_index(drop=True)

if len(step)==0:
    sys.exit('Please run pvpython OFToCSV.py to generate cfd_vel* files first !!!')

print ("writing data to CFDvel.xy!")
# write single file with velocity profiles for every timestep
df.to_csv('CFDvel.xy', sep='\t', float_format='%g',header = None, index=False)
sys.exit()
