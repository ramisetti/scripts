#### import the simple module from the paraview
#### USAGE: pvpython OFToCSV.py
from paraview import simple
import numpy as np
import os,glob

# open the foam file
filename = './case.foam'
open(filename, 'w').close()
reader = simple.OpenDataFile(filename)

# save data to csv file for each timestep
writer = simple.CreateWriter("./cfd_vel_.csv", reader)
writer.WriteAllTimeSteps = 1
writer.FieldAssociation = "Points"
writer.UpdatePipeline()

if os.path.exists(filename):
    os.remove(filename)
