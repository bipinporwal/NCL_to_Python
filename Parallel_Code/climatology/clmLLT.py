# Import Libraries
import sys
sys.path.insert(1, '../..')


import xarray as xr
from dask.distributed import Client
from dask_jobqueue import PBSCluster
from ncl_to_python.climatology_module import *
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
path = open("INPUT_PATH1.txt")
path1 = path.read()
path1 = path1.rstrip('\n')
print("PATH IS: {}".format(path1))

ds = xr.open_mfdataset(path1, chunks = {'nj':20, 'ni':60}, parallel = True)

var1 = ds["fsalt"]
var = var1.transpose('nj','ni','time')


strt = time.time()
result = clmMonLLT(var).compute()
end = time.time()


#result.to_netcdf("p_clmLLT.nc")
# Shutdown the client, workers and jobs running
client.shutdown()

print(result)
print("Time taken by the function: {} seconds".format(end-strt))




