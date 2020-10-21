##------------------------------------------------------------------------------

"""
##================================================================
## Routine          : calcMonAnomTLL.py   (serial version)
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


# Import libraries
import xarray as xr
import sys

# Search modules in parent directory
sys.path.insert(1, '..')
from ncl_to_python.climatology_module import *
from ncl_to_python.calc_mon_anom_module import *
import time

# Enter the path to the dataset
path = open("INPUT_PATH1.txt")

# Read the dataset path
path1 = path.read()
path1 = path1.rstrip('\n')

# Open dataset using xarray
ds = xr.open_dataset(path1)
var = ds["fsalt"]

# Calculate climatology
xAve = clmMonTLL(var)
strt = time.time()

# Call/execute the function sequentially
result = calcMonAnomTLL(var, xAve)
end = time.time()

print(result)

path.close()
