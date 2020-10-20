import xarray as xr
import sys
sys.path.insert(1, '..')
from ncl_to_python.climatology_module import *
import time


# Enter the path to the dataset
path = open("INPUT_PATH1.txt")
path1 = path.read()
path1 = path1.rstrip('\n')

ds = xr.open_dataset(path1)
var1 = ds["fsalt"]
var = var1.transpose('nj','ni','time')

strt = time.time()
result = clmMonLLT(var)
end = time.time()

print(result)
#result.to_netcdf("s_clmLLT.nc")
path.close()
