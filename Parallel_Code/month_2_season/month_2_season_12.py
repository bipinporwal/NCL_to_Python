"""
##================================================================
## Routine          : month_to_season12.py
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

# Import libraries
import sys
sys.path.insert(1, '../..')

import xarray as xr
from dask.distributed import Client
from dask_jobqueue import PBSCluster
from ncl_to_python.month_to_season_module import *
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
                     processes=32,
                     memory='40GB',
                     walltime='24:00:00',
                     resource_spec='select=1:ncpus=36:mem=40GB:vntype=cray_compute',
                     env_extra=[str("\ncd /lus/dal/hpcs_rnd/Python_Data_Analysis/Jatin/Ncl_to_python_parallel/Parallel_Function_Testing/dask-jobqueue/month_2_season \naprun -n 1 /bin/hostname > shost \nsource /lus/dal/hpcs_rnd/Python_Data_Analysis/Jatin/Ncl_to_python_parallel/Parallel_Function_Testing/dask-jobqueue/month_2_season/import_file ")],
				             python=str("aprun -n 1  /lus/dal/hpcs_rnd/apps/anaconda3/envs/Jatin/bin/python "),
								     sheebang='#!/bin/bash',
                     interface='ipogif0')

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

# Open dataset parallelly using dask and create chunks
ds = xr.open_mfdataset(path1, chunks = {'nj':40, 'ni':40}, parallel = True)


var = ds["fsalt"]

strt = time.time()
# Send function to workers for parallel execution
result = month_to_season12(var).compute()
end = time.time()


# Shutdown the client, workers and jobs running
client.shutdown()

print(result)
# Calculate the difference between start and end time of the function
print("Time taken by the function: {} seconds".format(end-strt))


path.close()
