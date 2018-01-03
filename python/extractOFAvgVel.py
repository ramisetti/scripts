#### IMPORTANT NOTE: this script should be only used
#### after running the OFToCSV.py script which generates
#### the cfd_vel_* files

#### USAGE: python extractOFAvgVel.py 

#### import packages
import os,sys,glob
import numpy as np
#import matplotlib.pyplot as plt
import itertools
import pandas as pd

cols_to_keep = ['Points:1', 'pAvg', 'UAvgVel:0', 'UAvgVel:1', 'UAvgVel:2']
# open each file created using OFToCSV script
# and extract velocity profile along y-direction
df=pd.DataFrame(data=None,columns=[cols_to_keep])
df.loc[len(df)]=['# Time averaged data', '','','','']
df.loc[len(df)]=['# Timestep XXX XXX', '','','','']
df.loc[len(df)]=['# Coord1 p vx vy vz', '','','','']
step=[]
df_temp=pd.DataFrame(data=None,columns=[cols_to_keep])

file_list = glob.glob("cfd_vel_0.*.csv")
file_list.sort(key=lambda x: int(x.split('.')[1]))
N=200
previous_file="cfd_vel_0.0.csv"
for filename in file_list:
	# extract timestep from filename
	time=int(os.path.splitext(filename)[0].split('.')[1])
    # ignore zero timestep data to be consistent with lammps data
	if (time==0): continue
	step.append(time)

	print ('calculating avgerage velocity at step %d between steps %d and %d \n' %(time,N*(time-1),N*time))
	data_prev=pd.read_csv(previous_file)
	data=pd.read_csv(filename)
	# convert y coordinates to non-dimensional numbers 
	data['Points:1']/=3.4e-10

	# calculate the average velocity between two timesteps
	# OF calculates stores the time averaged velocity in UMean
	# however, UMean is time averaged from initial time to timestep
	# where it is written to file
	# below lines calculate time averaged velocity for previous N steps
	# using equation: UAvg=(No_of_steps2*UMean2-No_of_steps1*UMean1)/(No_of_step2-No_of_step1)
	if (time==1):
		data['UAvgVel:0']=data['UMean:0']
		data['UAvgVel:1']=data['UMean:1']
		data['UAvgVel:2']=data['UMean:2']
		data['pAvg']=data['p']
	else:
		data['UAvgVel:0']=(N*time*data['UMean:0']-N*(time-1)*data_prev['UMean:0'])/N
		data['UAvgVel:1']=(N*time*data['UMean:1']-N*(time-1)*data_prev['UMean:1'])/N
		data['UAvgVel:2']=(N*time*data['UMean:2']-N*(time-1)*data_prev['UMean:2'])/N
		data['pAvg']=(N*time*data['p']-N*(time-1)*data_prev['p'])/N
    
	#data['Points:1']+=9.0
	group=data[cols_to_keep].groupby('Points:1',as_index = False).mean()
	df_temp.loc[len(df_temp)] = [time, 'XXX', 'XXX', '','']
	df_temp=df_temp.append(group)
	previous_file=filename

	# uncomment below lines if needed (useful to debug)
	# ofp=str(time)+'.csv'
	# data.to_csv(ofp,float_format='%g',index=False)

df = df.append(df_temp)
df = df.reset_index(drop=True)

if len(step)==0:
    sys.exit('Please run pvpython OFToCSV.py to generate cfd_vel* files first !!!')

print ("writing data to CFDvel.xy!")
# write single file with average velocity profiles for each timestep
df.to_csv('CFDvel.xy', sep='\t', float_format='%g',header = None, index=False)
sys.exit()
