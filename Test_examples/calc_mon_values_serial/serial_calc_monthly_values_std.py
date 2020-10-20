import xarray as xr
import sys
sys.path.insert(1, '..')
from ncl_to_python.calculate_monthly_values_module import *
import time

# Enter the path to the dataset

path = open("INPUT_PATH.txt")
path1 = path.read()
path1 = path1.rstrip('\n')
ds = xr.open_dataset(path1)
var = ds["FLNS"]

opt = xr.DataArray(data = False)
opt.attrs["nval_crit"] = 30


strt = time.time()
result = calculate_monthly_values(var, "std", 0, opt)
end = time.time()
print(result)

path.close()

