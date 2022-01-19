 
##------------------------------------------------------------------------------

"""
##================================================================
## Routine          : rmMonAnnCycLLLT.py   (parallel version)
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

##----------------------------------------------------------------------------------

# Import Libraries
import sys
sys.path.insert(1, '../..')
sys.path.insert(1, '../')
sys.path.insert(0, '/lus/dal/hpcs_rnd/Python_Data_Analysis/adwait_parallel/')
import xarray as xr
from dask.distributed import Client
#from dask_jobqueue import PBSCluster
from cluster_config import cluster_spec
from rmMonAnnCycLLLT import rmMonAnnCycLLLT
from dask import compute
import dask
import distributed
import time
import argparse
import json


# Fetch the dataset path, data-variable name, season name using argparse
parser = argparse.ArgumentParser()
parser.add_argument("filepath", type=str, help='Enter the dataset/file path')
parser.add_argument("variable", type=str, help="sst")
parser.add_argument("-w", "--workers", type=int, help= 'Enter the number of workers to create for parallel computing', required=True)
parser.add_argument("-c", "--chunks", type=json.loads, help="chunk to mention:'{\"lat\":55, \"lon\":55}'", required=True)

args = parser.parse_args()

# Extract path, variable name, season from args namespace
path = args.filepath
var_name = args.variable
num_of_workers = args.workers
chunk_details = args.chunks
#print(var_name)
cluster_details = cluster_spec(num_of_workers)
client = Client(cluster_details)
dask.config.set(**{"array.slicing.split_large_chunks": True})
try:
    ds = xr.open_mfdataset(path, chunks = chunk_details, parallel=True)
except IOError:
    print("Incorrect path, file not found")
    exit()

# Extract variable from dataset
try:
    var = ds[var_name]
    var1=var.transpose('z_t', 'nlat', 'nlon', 'time' )
except KeyError:
    print("Incorrect variable name. Variable '{}' not found in dataset".format(var_name))
    exit()


strt = time.time()
result = rmMonAnnCycLLLT(var1).compute()
end = time.time()


# Shutdown the client, workers and jobs running
client.shutdown()

print(result)
print("Time taken by the function: {} seconds".format(end-strt))

ds.close()


