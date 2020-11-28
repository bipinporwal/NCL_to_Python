##------------------------------------------------------------------------------

"""
##================================================================
## Routine          : month_to_season_combined.py (serial version)
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
from ncl_to_python.month_to_season_module import *
import argparse


# Fetch the dataset path, data-variable name, season name using argparse
parser = argparse.ArgumentParser()
parser.add_argument("filepath", type=str, help="Enter the dataset/file path")
parser.add_argument("variable", type=str, help="Enter the variable/dataarray to extract from dataset")
parser.add_argument("-s", "--seasons", nargs='*', default=[], help="(Optional) NOTE: Don't use this argument for month_to_season12(). \
                                                                   Enter one or more seasons to calculate. e.g 'JJA' or e.g. 'SON' 'NDJ'")

args = parser.parse_args()

# Extract path, variable name, season from args namespace
path = args.filepath
var_name = args.variable
season_list = args.seasons

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

# In month_to_season_combined, enter the parameter as we normally do for month_to_season functions, i.e.,:
# (Variable) for month_to_season12
# (Variable, Season) for month_to_season
# (Variable, Seasons) for month_to_seasonN
result = month_to_season_combined(var, *season_list)

print(result)

ds.close()


