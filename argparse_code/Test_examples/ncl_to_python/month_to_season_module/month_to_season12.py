"""
##================================================================
## Routine          : month_to_season12.py
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

# ignore warnings
import warnings
warnings.filterwarnings('ignore')

# import necessary libraries
import numpy as np
import pandas as pd
import xarray as xr


def month_to_season12(xMon):
    """Computes three-month seasonal means (DJF, JFM, FMA, MAM, AMJ, MJJ, JJA, JAS, ASO, SON, OND, NDJ).
    
    Parameters
    ----------
    xMon : A one-, three-, or four-dimensional DataArray [xMon(time) or xMon(time,lat,lon) or xMon(time,lev,lat,lon)]
           of any numeric type. xMon must have named dimensions and the time (leftmost) dimension must be divisible by 12.
           The data are assumed to be monthly mean data and the first record is assumed to be January.

    Returns
    -------
    objectDataArray : The return value will be of the same type and dimensionality as xMon. If the input data contains metadata 
                      (e.g., coordinate variables and attributes), these will be retained.

                      In addition, the attribute "season" is returned.

    """
    
    # xMon is the DataArray passed as an argument
    
    # Create a new array of seasons
    season = np.array(["DJF","JFM","FMA","MAM","AMJ","MJJ","JJA","JAS","ASO","SON","OND","NDJ"])
    
    # Get the number of dimensions of dataarray
    len_of_dim = xMon.sizes
    num_of_dim = len(len_of_dim)
    
    # Check if the number of dimensions of dim is valid or invalid; if invalid, exit the function
    if (num_of_dim == 2 or num_of_dim >= 5):
        print("month_to_season12: number of dimensions = {}".format(num_of_dim))
        print("----- Dimensions currently not handled -----")
        return None
    
    # Check if number of months are multiple of 12; if not, exit the function
    no_of_months = 12
    no_of_time = len_of_dim[xMon.dims[0]]
    if ((no_of_time % no_of_months) != 0):
        print("month_to_season12: dimension must be a multiple of 12")
        return None
    
    
    # Check if dimensions are named or not; if unnamed, exit the function
    for i in range(0, num_of_dim):
        if xMon.dims[i] == None or xMon.dims[i] == "":
            print("mon_to_season12: All dimensions must be named")
            print("\t\tdimension {} is missing".format(i))
            return None
    
    # Calculating seasonal mean for number of dimensions = 1
    if (num_of_dim == 1):
        
        # Calculate seasonal mean for each season
        dr = xMon.rolling(time = 3, center = True).mean(skipna = True)
        dr[0] = (xMon[0] + xMon[1]) * 0.5
        dr[(no_of_time-1)] = (xMon[(no_of_time-2)] + xMon[(no_of_time-1)]) * 0.5
        
        # Create a new DataArray using the existing ones
        xSea = xMon.copy(data = dr)
        
        # Add and update the attributes
        xSea.attrs['season'] = season
        xSea.attrs['long_name'] = "seasonal means: " + xSea.attrs['long_name']
        xSea = xSea.rename("xSea")
        
        xSea.encoding = xMon.encoding
        # Return the newly created DataArray
        return xSea
    
    
    # Calculating seasonal mean for number of dimensions = 3
    if (num_of_dim == 3):
        
        # Calculate seasonal mean for each season
        dr = xMon.rolling(time = 3, center = True).mean(skipna = True)
        dr[0,:,:] = (xMon[0,:,:] + xMon[1,:,:]) * 0.5
        dr[(no_of_time-1),:,:] = (xMon[(no_of_time-2),:,:] + xMon[(no_of_time-1),:,:]) * 0.5
        
        # Create a new DataArray using the existing ones
        xSea = xMon.copy(data = dr)
        
        # Add and update the attributes
        xSea.attrs['season'] = season
        xSea.attrs['long_name'] = "seasonal means: " + xSea.attrs['long_name']
        xSea = xSea.rename("xSea")
        xSea.encoding = xMon.encoding

        # Return the newly created DataArray
        return xSea
    
    
    # Calculating seasonal mean for number of dimensions = 4
    if (num_of_dim == 4):
        
        # Calculate seasonal mean for each season
        dr = xMon.rolling(time = 3, center = True).mean(skipna = True)
        dr[0,:,:,:] = (xMon[0,:,:,:] + xMon[1,:,:,:]) * 0.5
        dr[(no_of_time-1),:,:,:] = (xMon[(no_of_time-2),:,:,:] + xMon[(no_of_time-1),:,:,:]) * 0.5
        
        # Create a new DataArray using the existing ones
        xSea = xMon.copy(data = dr)
        
        # Add and update the attributes
        xSea.attrs['season'] = season
        xSea.attrs['long_name'] = "seasonal means: " + xSea.attrs['long_name']
        xSea = xSea.rename("xSea")
        xSea.encoding = xMon.encoding

        # Return the newly created DataArray
        return xSea


