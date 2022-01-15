##------------------------------------------------------------------------------

"""
##================================================================
## Routine          : stdMonTLLL.py (serial version)
## Author/Developer : IITM Pune/RAIT Mumbai 
## Institute/Company: IIIM Pune, Ministry of Earth Science, Gov. of India
##================================================================
"""

"""
---------------------------------------------------------

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the names of author and company. 

2. Name of developers may not be used to endorse or promote products derived from this software without
specific prior written permission.

----
1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.
"""

##----------------------------------------------------------------------------------



# Import Libraries
import xarray as xr
import sys
import argparse

# Search modules in parent folder
sys.path.insert(1, '../')
from ncl_to_python.std_module import stdMonTLLL
import time

# Fetch the dataset path using argparse
parser = argparse.ArgumentParser()
parser.add_argument("filepath", type = str, help = "the path where file/dataset is located")
parser.add_argument("variable_name", type=str, help = "enter variable name")

args = parser.parse_args()
print(args)

path = args.filepath
print(path)

var2 = args.variable_name

# Open dataset using xarray
try:
    ds = xr.open_dataset(path)
except IOError:
    print("File Not Found")
    exit()

try:
    var1 = ds[var2]
    # Re-order the coordinates
    var = var1.transpose('time','lat','lon','level')
except KeyError:
    print("Variable not found")
    exit()

var=var[0:864,:,:,:]
strt = time.time()

# Call/Execute the function sequentially
result = stdMonTLLL(var)
end = time.time()

print(result)
#result.to_netcdf("s_clmTLL.nc")
ds.close()
