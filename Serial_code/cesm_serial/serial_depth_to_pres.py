##------------------------------------------------------------------------------

"""
##================================================================
## Routine          : depth_to_pres.py (serial version)
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
from ncl_to_python.cesm_module import depth_to_pres
import time

# Fetch the data using argparse

parser = argparse.ArgumentParser()
parser.add_argument("depth", nargs='+', type=float,help = "Enter depth values") #List of depth values
parser.add_argument("opt", nargs='+', type=int,help = "Enter option")
	
args = parser.parse_args()
d=args.depth
h=args.opt

strt = time.time()
h=0
# Call/Execute the function sequentially
result = depth_to_pres(d,h)
end = time.time()

print(result)

