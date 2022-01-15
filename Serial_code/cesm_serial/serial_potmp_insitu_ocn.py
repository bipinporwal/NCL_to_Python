##------------------------------------------------------------------------------

"""
##================================================================
## Routine          : potmp_insitu_ocn.py (serial version)
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
from ncl_to_python.cesm_module import potmp_insitu_ocn
import time

# Fetch the data using argparse

parser = argparse.ArgumentParser()
parser.add_argument("--temperature", nargs='+', type=float, help = "Enter insitu temperature (degC) values",required=True) #List of temperature values
parser.add_argument("--salinity", nargs='+', type=float, help = "Enter salinity (g/kg) values",required=True)  #List of salinity values
parser.add_argument("--pressure", nargs='+', type=float, help = "Enter ocean pressure (decibar) values",required=True)  #List of pressure values
parser.add_argument("--reference_pressure", nargs='+', type=float, help = "Enter ocean pressure (decibar) values",required=True)  
parser.add_argument("--dimension", nargs='+', type=float, help = "The dimension(s) of t to which pres correspond. Must be consecutive and monotonically increasing. ", required=True)
parser.add_argument("--option", nargs='+', type=bool, help = "False=0, True=1",required=True)

	
args = parser.parse_args()
t=args.temperature
s=args.salinity
p=args.pressure
rp=args.reference_pressure
dim=args.dimension
opt=args.option


strt = time.time()
# Call/Execute the function sequentially
result = potmp_insitu_ocn(t,s,p,rp,dim,opt)
end = time.time()

print(result)

