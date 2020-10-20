import xarray as xr
import sys
sys.path.insert(1, '..')
from ncl_to_python.climatology_module import *
from ncl_to_python.calc_mon_anom_module import *
import time

# Enter the path to the dataset
path = open("INPUT_PATH1.txt")
path1 = path.read()
path1 = path1.rstrip('\n')
ds = xr.open_dataset(path1)
var = ds["fsalt"]


xAve = clmMonTLL(var)
strt = time.time()
result = calcMonAnomTLL(var, xAve)
end = time.time()

print(result)

path.close()
