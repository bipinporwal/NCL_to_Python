"""
##================================================================
## Routine          : rmMonAnnCycLLLT.py
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

##================================================================
#Import libraries
import xarray as xr
import pandas as pd

def rmMonAnnCycLLLT(x):
    """Removes the annual cycle from monthly data(lev,lat,lon,time version)

    Parameters
    ----------
    x : A four-dimensional DataArray. Dimensions must be lev,lat,lon,time. The time dimension must be a multiple of 12.

    Returns
    -------
    objectDataArray : A DataArray object of the same size and type as x.

    """
    # Calculate the sizes of time dimension
    len_of_dim = x.sizes
    no_of_time = len_of_dim[x.dims[0]] # no_of_time = Size of time dimension
    num_of_dim = len(len_of_dim)

    # Check if num_of_dim of dataarray matches the function
    if (num_of_dim != 4):
        print("Expected variable of num_of_dim = 4, recieved num_of_dim = {}".format(num_of_dim))
        return None
    
    
    # Check if number of months are multiple of 12; if not, exit the function
    no_of_months = 12
    if ((no_of_time % no_of_months) != 0):
        print("rmMonAnnCycLLLT: dimension must be a multiple of 12")
        return None
    
    # Store the time dimension name present in dataset as time variable
    time = x.dims[3]
    
    # Store as a string for groupby operation
    time_month = time + '.month'
    
    # Removes monthly annual cycle
    xrm = x.groupby('time.month')-x.groupby('time.month').mean('time')              
    
     # Copy and update the attributes
    xrm.attrs = x.attrs
    xrm.attrs['rm_op_ncl'] = "Removes Annual Cycle from Monthly data: rmMonAnnCycLLLT"             
    xrm.attrs['info'] = "function rmMonAnnCycLLLT"
    
    # Copy the encoding from the original DataArray
    xrm.encoding = x.encoding
            
    # Return the new dataarray
    return xrm
    
     
