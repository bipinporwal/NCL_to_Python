"""
##================================================================
## Routine          : calcMonAnomTLLL.py
## Author/Developer : IITM Pune/RAIT Mumbai 
## Institute/Company: IIIM Pune, Ministry of Earth Science, Gov. of India
##================================================================
"""

"""
---------------------------------------------------------

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the names of author and company. 

2. Name of developers may not be used to endorse or promote products derived from this software without
specific prior written permission.

----
1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.
"""

##================================================================


# Import Libraries
import sys
sys.path.insert(1, '../..')


import xarray as xr
from dask.distributed import Client
from dask_jobqueue import PBSCluster
from ncl_to_python.climatology_module import *
from ncl_to_python.calc_mon_anom_module import *
from dask import compute
import dask
import distributed
import time

# Create a PBS Cluster job-script using dask-jobqueue
cluster = PBSCluster(queue='research',
                     project='DaskOnPBS',
                     local_directory='DASK_OUT/',
                     log_directory='DASK_OUT/',
                     cores=1,
                     processes=1,
                     memory='10GB',
                     walltime='24:00:00',
                     resource_spec='select=1:ncpus=36:mem=80GB:vntype=cray_compute',
                     env_extra=['aprun -n 1'])

# Store the command line argument in a variable 'j'
j = sys.argv[1]
j = int(j)
# Scale clusters to add j workers (j= number of jobs)
cluster.scale(j)


# Create dask-scheduler (client) and pass it the cluster configuration
client = Client(cluster)


# Enter the path to the dataset
path = open("INPUT_PATH.txt")

# Read the dataset path
path1 = path.read()
path1 = path1.rstrip('\n')
print("PATH IS: {}".format(path1))

# Open dataset parallelly using dask and create chunks
ds = xr.open_mfdataset(path1, chunks = {'lat':60, 'lon':60, 'lev':6}, parallel = True)

var = ds["AQRAIN"]


# Compute Climatology parallelly
xAve = clmMonTLLL(var)

strt = time.time()

# Send function to workers for parallel execution
result = calcMonAnomTLLL(var, xAve).compute()
end = time.time()


# Shutdown the client, workers and jobs running
client.shutdown()


print(result)

# Calculate the difference between start and end time of the function
print("Time taken by the function: {} seconds".format(end-strt))

path.close()
