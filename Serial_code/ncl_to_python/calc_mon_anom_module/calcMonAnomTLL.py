"""
##================================================================
## Routine          : calcMonAnomTLL.py
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

def calcMonAnomTLL(x, xAve):
    """Calculates monthly anomalies by subtracting the long term mean from each point (time,lat,lon version)

    Parameters
    ----------
    x : A three-dimensional DataArray. Dimensions must be time,lat,lon The time dimension must be a multiple of 12.

    xAve : A three-dimensional DataArray equal to the monthly averages of x. The leftmost two dimensions are lat and lon, while the leftmost must be of size 12.

    Returns
    -------
    objectDataArray : A DataArray object of the same size and type as x.

    """

    # x is the dataarray and xAve is the monthly averages array of x
    
    len_of_dim = x.sizes
    no_of_time = len_of_dim[x.dims[0]] # no_of_time = Size of time dimension
    num_of_dim = len(len_of_dim)

    # Check if num_of_dim of dataarray matches the function
    if (num_of_dim != 3):
        print("Expected variable of num_of_dim = 3, recieved num_of_dim = {}".format(num_of_dim))
        return None
    
    
    # Check if number of months are multiple of 12; if not, exit the function
    no_of_months = 12
    if ((no_of_time % no_of_months) != 0):
        print("calcMonAnom: dimension must be a multiple of 12")
        return None
    
    # Store the time dimension name present in dataset as time variable
    time = x.dims[0]
    
    # Store as a string for groupby operation
    time_month = time + '.month'
    
    
    # Calculate anomalies by subtracting monthly means from actual dataarray
    xAnom = x.groupby(time_month) - xAve
        
    # Copy and update the attributes
    xAnom.attrs = x.attrs
    xAnom.attrs['anomaly_op_ncl'] = "Anomalies from Annual Cycle: calcMonAnomTLL"
    
    # Drop the extra month co-ordinate from xAnom DataArray
    xAnom = xAnom.drop('month')
    xAnom = xAnom.rename("xAnom")
    
    # Copy the encoding from the original DataArray
    xAnom.encoding = x.encoding
    
    # Return the new dataarray
    return xAnom
