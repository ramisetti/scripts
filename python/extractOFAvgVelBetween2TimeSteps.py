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

time1=int(sys.argv[1])
time2=int(sys.argv[2])
deltaN=int(sys.argv[3])

if (time2 < time1):
	sys.exit("Usage: python extractOFAvgVelBetween2TimeSteps time1 time2(>time1) deltaN")

previous_file="cfd_vel_0."+str(time1)+".csv"
current_file="cfd_vel_0."+str(time2)+".csv"

cols_to_keep = ['Points:1', 'pAvg', 'UAvgVel:0', 'UAvgVel:1', 'UAvgVel:2']
# open each file created using OFToCSV script
# and extract velocity profile along y-direction
df=pd.DataFrame(data=None,columns=[cols_to_keep])
df.loc[len(df)]=['# Time averaged data', '','','','']
df.loc[len(df)]=['# Timestep XXX XXX', '','','','']
df.loc[len(df)]=['# Coord1 p vx vy vz', '','','','']
step=[]
df_temp=pd.DataFrame(data=None,columns=[cols_to_keep])

step.append(time2)

print ('calculating avgerage velocity at step %d between steps %d and %d \n' %(time2,time1,time2))
data_prev=pd.read_csv(previous_file)
data=pd.read_csv(current_file)

# calculate the average velocity between two timesteps
# OF calculates stores the time averaged velocity in UMean
# however, UMean is time averaged from initial time to timestep
# where it is written to file
# below lines calculate time averaged velocity for previous N steps
# using equation: UAvg=(No_of_steps2*UMean2-No_of_steps1*UMean1)/(No_of_step2-No_of_step1)
if (time2==1):
	data['UAvgVel:0']=data['UMean:0']
	data['UAvgVel:1']=data['UMean:1']
	data['UAvgVel:2']=data['UMean:2']
	data['pAvg']=data['p']
else:
	data['UAvgVel:0']=(deltaN*time2*data['UMean:0']-deltaN*(time1)*data_prev['UMean:0'])/(deltaN*(time2-time1))
	data['UAvgVel:1']=(deltaN*time2*data['UMean:1']-deltaN*(time1)*data_prev['UMean:1'])/(deltaN*(time2-time1))
	data['UAvgVel:2']=(deltaN*time2*data['UMean:2']-deltaN*(time1)*data_prev['UMean:2'])/(deltaN*(time2-time1))

data['pAvg']=(deltaN*time2*data['p']-deltaN*(time1)*data_prev['p'])/deltaN

#data['Points:1']+=9.0
# convert y coordinates to non-dimensional numbers 
data['Points:1']/=3.4e-10
# convert velocity to non-dimensional numbers 
data['UAvgVel:0']*=(2.15e-12/3.4e-10)
data['UAvgVel:1']*=(2.15e-12/3.4e-10)
data['UAvgVel:2']*=(2.15e-12/3.4e-10)

group=data[cols_to_keep].groupby('Points:1',as_index = False).mean()
df_temp.loc[len(df_temp)] = [time2, 'XXX', 'XXX', '','']
df_temp=df_temp.append(group)

# uncomment below lines if needed (useful to debug)
# ofp=str(time)+'.csv'
# data.to_csv(ofp,float_format='%g',index=False)

df = df.append(df_temp)
df = df.reset_index(drop=True)

if len(step)==0:
    sys.exit('Please run pvpython OFToCSV.py to generate cfd_vel* files first !!!')

print ("writing data to CFDAvgVel.xy!")
# write single file with average velocity profiles for each timestep
df.to_csv('CFDAvgVel.xy', sep='\t', float_format='%g',header = None, index=False)
sys.exit()
