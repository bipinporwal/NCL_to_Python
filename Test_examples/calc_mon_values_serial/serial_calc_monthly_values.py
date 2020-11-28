##------------------------------------------------------------------------------

"""
##================================================================
## Routine          : calculate_monthly_values.py   (serial version)
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
from ncl_to_python.calculate_monthly_values_module import *
import argparse


# Fetch the dataset path, data-variable name, season name using argparse
parser = argparse.ArgumentParser()
parser.add_argument("filepath", type=str, help="Enter the dataset/file path")
parser.add_argument("variable", type=str, help="Enter the variable/dataarray to extract from dataset")
parser.add_argument("statistic", type=str, help="Enter the statistic to calculate. e.g. avg, \
                                                 The list of arguements that can be passed are: \
                                                 'avg' = average, \
                                                 'sum' = sum, \
                                                 'min' = minimum, \
                                                 'max' = maximum, \
                                                 'var' = variance, \
                                                 'std' = standard deviation.")
parser.add_argument("opt", type=bool, help="Set opt either 'True' or 'False'")
parser.add_argument("-n", "--nval_crit", type=int, default=1, help="If opt is set 'True', enter nval_crit value (default nval_crit = 0)")

args = parser.parse_args()

# Extract path, variable name, season from args namespace
path = args.filepath
var_name = args.variable
stat = args.statistic
opt_val = args.opt
nval_crit = args.nval_crit

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


opt = xr.DataArray(data = opt_val)
opt.attrs["nval_crit"] = nval_crit


result = calculate_monthly_values(var, stat, 0, opt)

print(result)

ds.close()

