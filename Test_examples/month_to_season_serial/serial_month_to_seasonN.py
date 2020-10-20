import xarray as xr
import sys
sys.path.insert(1, '..')
from ncl_to_python.month_to_season_module import *
import time

# Enter the path to the dataset
path = open("INPUT_PATH.txt")
path1 = path.read()
path1 = path1.rstrip('\n')
ds = xr.open_dataset(path1)
var = ds["AQRAIN"]


strt = time.time()
result = month_to_seasonN(var, "DJF", "MAM")
end = time.time()
print(result)

path.close()


