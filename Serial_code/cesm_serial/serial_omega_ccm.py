##------------------------------------------------------------------------------

"""
##================================================================
## Routine          : omega_ccm.py (serial version)
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
from ncl_to_python.cesm_module import omega_ccm
import time

# Fetch the dataset path using argparse
parser = argparse.ArgumentParser()
parser.add_argument("filepath_u", type = str, help = "the path where file/dataset for u is located")
parser.add_argument("u", type=str, help = "enter variable name for u")
parser.add_argument("filepath_v", type = str, help = "the path where file/dataset for v is located")
parser.add_argument("v", type=str, help = "enter variable name for v")
parser.add_argument("filepath_div", type = str, help = "the path where file/dataset for div is located")
parser.add_argument("div", type=str, help = "enter variable name for divergence")
parser.add_argument("filepath_dpsl", type = str, help = "the path where file/dataset for dpsl is located")
parser.add_argument("dpsl", type=str, help = "enter variable name for dpsl")
parser.add_argument("filepath_dpsm", type = str, help = "the path where file/dataset for dpsm is located")
parser.add_argument("dpsm", type=str, help = "enter variable name for dpsm")
parser.add_argument("filepath_pmid", type = str, help = "the path where file/dataset for pmid is located")
parser.add_argument("pmid", type=str, help = "enter variable name for pmid")
parser.add_argument("filepath_pdel", type = str, help = "the path where file/dataset for pdel is located")
parser.add_argument("pdel", type=str, help = "enter variable name for pdel")
parser.add_argument("filepath_psfc", type = str, help = "the path where file/dataset for psfc is located")
parser.add_argument("psfc", type=str, help = "enter variable name for psfc")


# Enter data for other variables using argparse
parser.add_argument("--hybdif", nargs='+', type=float, help = "Enter a one-dimensional array containing the difference between the hybrid interface coefficients",required=True)
parser.add_argument("--hybm", nargs='+', type=float, help = "Enter a  one-dimensional array containing hybrid B coefficient values",required=True)
parser.add_argument("--nprlev", nargs='+', type=float, help = "Enter number of pure pressure levels",required=True)



args = parser.parse_args()
path1 = args.filepath_u
path2 = args.filepath_v
path3 = args.filepath_div
path4 = args.filepath_dpsl
path5 = args.filepath_dpsm
path6 = args.filepath_pmid
path7 = args.filepath_pdel
path8 = args.filepath_psfc


u1 = args.u
v1 = args.v
div1 = args.div
dpsl1 = args.dpsl
dpsm1 = args.dpsm
pmid1 = args.pmid
pdel1 = args.pdel
psfc1 = args.psfc
hd=args.hybdif
hb=args.hybm
n=args.nprlev


# Open dataset using xarray
try:
    ds1 = xr.open_dataset(path1)
except IOError:
    print("File Not Found for u")
    exit()
    
try:
    ds2 = xr.open_dataset(path2)
except IOError:
    print("File Not Found for v")
    exit()
   
try:
    ds3 = xr.open_dataset(path3)
except IOError:
    print("File Not Found for div")
    exit()
    
try:
    ds4 = xr.open_dataset(path4)
except IOError:
    print("File Not Found for dpsl")
    exit()

try:
    ds5 = xr.open_dataset(path5)
except IOError:
    print("File Not Found for dpsm")
    exit()
    
try:
    ds6 = xr.open_dataset(path6)
except IOError:
    print("File Not Found for pmid")
    exit()
    
try:
    ds7 = xr.open_dataset(path7)
except IOError:
    print("File Not Found for pdel")
    exit()
    
try:
    ds8 = xr.open_dataset(path8)
except IOError:
    print("File Not Found for psfc")
    exit()  
    
                  
try:
    u2 = ds1[u1]
    u3 = u2[0,0:2,0:10,0:10]
    # Re-order the coordinates
    u4 = u3.transpose('lon','lat','level')
    
except KeyError:
    print("Variable u not found")
    exit()

try:
    v2 = ds2[v1]
    v3 = v2[0,0:2,:10,:10]
    # Re-order the coordinates
    v4 = v3.transpose('lon','lat','level')
    
except KeyError:
    print("Variable v not found")
    exit()

try:
    div2 = ds3[div1]
    div3 = div2[0,0:2,0:10,0:10]
    # Re-order the coordinates
    div4 = div3.transpose('lon','lat','level')
    
except KeyError:
    print("Variable div not found")
    exit()

try:
    dpsl2 = ds4[dpsl1]
    dpsl3 = dpsl2[0,:10,:10]
    # Re-order the coordinates
    dpsl4 = dpsl3.transpose('lon','lat')
    
except KeyError:
    print("Variable dpsl not found")
    exit()

try:
    dpsm2 = ds5[dpsm1]
    dpsm3 = dpsm2[0,:10,:10]
    # Re-order the coordinates
    dpsm4 = dpsm3.transpose('lon','lat')
    
except KeyError:
    print("Variable dpsm not found")
    exit()

try:
    pmid2 = ds6[pmid1]
    pmid3 = pmid2[0,0:2,:10,:10]
    # Re-order the coordinates
    pmid4 = pmid3.transpose('lon','lat','level')
    
except KeyError:
    print("Variable pmid not found")
    exit()

try:
    pdel2 = ds7[pdel1]
    pdel3 = pdel2[0,0:2,:10,:10]
    # Re-order the coordinates
    pdel4 = pdel3.transpose('lon','lat','level')
    
except KeyError:
    print("Variable pdel not found")
    exit()

try:
    psfc2 = ds8[psfc1]
    psfc3 = psfc2[0,:10,:10]
    # Re-order the coordinates
    psfc4 = psfc3.transpose('lon','lat')
    
except KeyError:
    print("Variable psfc not found")
    exit()


strt = time.time()
# Call/Execute the function sequentially
result = omega_ccm(u4, v4, div4, dpsl4, dpsm4, pmid4, pdel4, psfc4, hd, hb, n)
end = time.time()


#for k in range(0,1):
    #for j in range(0,20):
        #for i in range(0,20):
            #print(result[i][j][k])
print(result)
#result.to_netcdf("s_clmTLL.nc")

