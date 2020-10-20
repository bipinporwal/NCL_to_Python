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
var1 = ds["AQRAIN"]
var = var1.transpose('lev', 'lat', 'lon', 'time')

var = var.chunk({'lat':40, 'lon':40})

strt = time.time()
result = clmMonLLLT(var)
end = time.time()

print(result)
#result.to_netcdf("s_clmLLLT.nc")
path.close()

