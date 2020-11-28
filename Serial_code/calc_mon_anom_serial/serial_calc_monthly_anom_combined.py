##------------------------------------------------------------------------------

"""
##================================================================
## Routine          : calcMonAnomCombined.py   (serial version)
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


import xarray as xr
import sys
sys.path.insert(1, '..')
from ncl_to_python.climatology_module import *
from ncl_to_python.calc_mon_anom_module import *
import argparse


# Fetch the dataset path, data-variable name, season name using argparse
parser = argparse.ArgumentParser()
parser.add_argument("filepath", type=str, help="Enter the dataset/file path")
parser.add_argument("variable", type=str, help="Enter the variable/dataarray to extract from dataset")
parser.add_argument("index", type=int, choices=[0, 2, 3], help="Enter the index of time dimension. Valid values are 0, 2, 3. \
                                             For e.g. For calcMonAnomTLL/calcMonAnomTLLL, time is stored at index value 0, \
                                             for calcMonAnomLLT, time dimension is stored at index value 2, and \
                                             for calcMonAnomLLLT, time dimension is stored at index value 3.")

args = parser.parse_args()

# Extract path, variable name, season from args namespace
path = args.filepath
var_name = args.variable
index_value = args.index

# Open dataset
try:
    ds = xr.open_dataset(path)
except IOError:
    print("Incorrect path, file not found")
    exit()

# Extract variable from dataset
try:
    var = ds[var_name]
except KeyError:
    print("Incorrect variable name. Variable '{}' not found in dataset".format(var_name))
    exit()

if len(var.dims) == 3:
    if index_value == 0:
        xAve = clmMonTLL(var)
    else:
        var = var.transpose()
        xAve = clmMonLLT(var)
elif len(var.dims) == 4:
    if index_value == 0:
        xAve = clmMonTLLL(var)
    else:
        var = var.transpose()
        xAve = clmMonLLLT(var)

result = calcMonAnomCombined(index_value, var, xAve)

print(result)

ds.close()
