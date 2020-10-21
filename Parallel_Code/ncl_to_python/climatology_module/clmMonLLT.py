"""
##================================================================
## Routine          : clmMonLLT.py
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

# Import libraries

import xarray as xr

def clmMonLLT(x):
    """Calculates long term monthly means (monthly climatology) from monthly data (lat,lon,time version).

    Parameters
    ----------
    x : A three-dimensional DataArray of any numeric type. Dimensions must be lat, lon, time. The time dimension must be a multiple of 12. The dimensions must be named.

    Returns
    -------
    objectDataArray : A DataArray of the same size and type as x except that the rightmost dimension will be of size 12.

    """
    
    # Calculate the sizes of time dimension
    len_of_dim = x.sizes
    time_size = len_of_dim[x.dims[2]]
    num_of_dim = len(len_of_dim)

    # Check if num_of_dim of dataarray matches the function
    if (num_of_dim != 3):
        print("Expected variable of num_of_dim = 3, recieved num_of_dim = {}".format(num_of_dim))
        return None
    
    # Check if number of months are multiple of 12; if not, exit the function
    no_of_months = 12
    if ((time_size % no_of_months) != 0):
        print("clmMonTLL: dimension must be a multiple of 12")
        return None
    
    # Store the time dimension name present in dataset as time variable
    time = x.dims[2]
    
    # Store as a string for groupby operation
    time_month = time + '.month'
    
    # Compute 12 months average
    ave_month = x.groupby(time_month).mean(time, skipna = True)
    
    # Copy and update the attributes
    ave_month.attrs = x.attrs
    ave_month = ave_month.rename("aveMonth")
    ave_month.attrs['time_op_ncl'] = "Climatology: " + str(int(time_size/no_of_months)) + " years"
    ave_month.attrs['info'] = "function clmMonLLT"

    # Copy the encoding from original DataArray
    ave_month.encoding = x.encoding
   
    # Return the results
    return ave_month
