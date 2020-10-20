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
# In month_to_season_combined, enter the parameter as we normally do for month_to_season functions, i.e.,:
# (Variable) for month_to_season12
# (Variable, Season) for month_to_season
# (Variable, Seasons) for month_to_seasonN
result = month_to_season_combined(var, "JJA", "SON", "NDJ")
end = time.time()
print(result)

path.close()


