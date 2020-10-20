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
                     processes=1,
                     memory='40GB',
                     walltime='24:00:00',
                     resource_spec='select=1:ncpus=36:mem=40GB:vntype=cray_compute',
                     env_extra=['aprun -n 1'])

j = sys.argv[1]
j = int(j)
# Scale clusters to add j workers (j= number of jobs)
cluster.scale(j)

client = Client(cluster)


# Enter the path to the dataset
path = open("INPUT_PATH.txt")
path1 = path.read()
path1 = path1.rstrip('\n')
#print("PATH IS: {}".format(path1))
ds = xr.open_mfdataset(path1, chunks = {'nj':60, 'ni':60}, parallel = True)

var = ds["fsalt"]

strt = time.time()
result = month_to_seasonN(var, "JFM", "SON").compute()
end = time.time()


# Shutdown the client, workers and jobs running
client.shutdown()



print(result)
print("Time taken by the function: {} seconds".format(end-strt))



