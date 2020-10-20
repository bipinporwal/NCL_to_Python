import xarray as xr
import sys
sys.path.insert(1, '..')
from ncl_to_python.climatology_module import *
import time

# Enter the path to the dataset
path = open("INPUT_PATH.txt")
path1 = path.read()
path1 = path1.rstrip('\n')

ds = xr.open_dataset(path1)
var = ds["AQRAIN"]

var = var.chunk({'lat':40, 'lon':40})

strt = time.time()
result = clmMonTLLL(var)
end = time.time()


print(result)
#result.to_netcdf("s_clmTLLL.nc")
path.close()


