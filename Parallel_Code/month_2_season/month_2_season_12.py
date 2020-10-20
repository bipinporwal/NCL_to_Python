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

j = sys.argv[1]
j = int(j)
# Scale clusters to add j workers (j= number of jobs)
cluster.scale(j)


client = Client(cluster)

# Enter the path to the dataset
path = open("INPUT_PATH.txt")
path1 = path.read()
path1 = path1.rstrip('\n')
ds = xr.open_mfdataset(path1, chunks = {'nj':40, 'ni':40}, parallel = True)


var = ds["fsalt"]

strt = time.time()
result = month_to_season12(var).compute()
end = time.time()


# Shutdown the client, workers and jobs running
client.shutdown()

print(result)
print("Time taken by the function: {} seconds".format(end-strt))



