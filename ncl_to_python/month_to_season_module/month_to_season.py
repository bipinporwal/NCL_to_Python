"""
##================================================================
## Routine          : month_to_season.py
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
# ignore warnings
import warnings
warnings.filterwarnings('ignore')

# import necessary libraries
import numpy as np
import pandas as pd
import xarray as xr

def month_to_season(xMon, SEASON):
    """Computes a user-specified three-month seasonal mean (DJF, JFM, FMA, MAM, AMJ, MJJ, JJA, JAS, ASO, SON, OND, NDJ).

    
    Parameters
    ----------
    xMon : A one-, three-, or four-dimensional DataArray [xMon(time) or xMon(time,lat,lon) or xMon(time,lev,lat,lon)]
           of any numeric type. xMon must have named dimensions and the time (leftmost) dimension must be divisible by 12.
           The data are assumed to be monthly mean data and the first record is assumed to be January.
    
    SEASON : A string representing the season to calculate: e.g., "JFM", "JJA".

    Returns
    -------
    objectDataArray : The return value will be of the same type and dimensionality as xMon, except the leftmost dimension
                      will have been divided by 12.
    
                      If the input data contains metadata (e.g., coordinate variables and attributes), these will be retained.
                      There is no output time dimension. The output contains only the season requested.

                      The attribute "NMO" is returned (for possible use in subscripting.)

    """
    # xMon is the DataArray and SEASON is the season passed as an argument
    
    # Create a new array of seasons
    season = np.array(["DJF","JFM","FMA","MAM","AMJ","MJJ","JJA","JAS","ASO","SON","OND","NDJ"])
    
    # Check if the season argument passed is valid or not
    if SEASON not in season:
        print("month_to_season: bad season: SEASON={}".format(SEASON))
        return None
    else:
        NMO_tup = np.where(season==SEASON)
        NMO = NMO_tup[0].item()
    
    # Get the number of dimensions of dataarray
    len_of_dim = xMon.sizes
    num_of_dim = len(len_of_dim)
    
    # Check if the number of dimensions of dim is valid or invalid
    if (num_of_dim == 2 or num_of_dim >= 5):
        print("month_to_season12: number of dimensions = {}".format(num_of_dim))
        print("----- Dimension currently not handled -----")
        return None
    
    # Check if number of months are multiple of 12
    no_of_months = 12
    no_of_time = len_of_dim[xMon.dims[0]]
    if ((no_of_time % no_of_months) != 0):
        print("month_to_season12: dimension must be a multiple of 12")
        return None
   
    
    # Calculate number of years
    no_of_years = int(no_of_time/no_of_months)
    con = 1./3.
    
    # Starting and ending years
    no_year_start = 0
    no_year_last = no_of_years - 1
    if (NMO == 0):
        no_year_start = 1
    elif (NMO == (no_of_months-1)):
        no_year_last = no_of_years - 2
    
    # Create a copy of new dataarray using the existing one
    da_new = xMon.copy(deep = True, data = None)
    
    # For number of dimensions = 1
    if (num_of_dim == 1):
        for nyr in range(no_year_start, (no_year_last+1)):
            n = nyr * no_of_months + NMO
            da_new[n] = (xMon[n-1] + xMon[n] + xMon[n+1]) * con
        
        if (NMO == 0):
            n = 0
            da_new[n] = (xMon[n] + xMon[n+1])*0.5
        
        if (NMO == (no_of_months-1)):
            n = (no_of_years-1)*no_of_months + NMO
            da_new[n] = (xMon[n] + xMon[n-1])*0.5

        da_new = da_new[NMO:no_of_time:no_of_months]               
        
    # For number of dimensions = 3
    if (num_of_dim == 3):
        for nyr in range(no_year_start, (no_year_last+1)):
            n = nyr*no_of_months + NMO
            da_new[n,:,:] = (xMon[(n-1),:,:] + xMon[n,:,:] + xMon[(n+1),:,:]) * con
        
        if (NMO == 0):
            n = 0
            da_new[n,:,:] = (xMon[n,:,:] + xMon[(n+1),:,:])*0.5
        
        if (NMO == (no_of_months-1)):
            n = (no_of_years-1)*no_of_months + NMO
            da_new[n,:,:] = (xMon[n,:,:] + xMon[(n-1),:,:])*0.5
        
        da_new = da_new[NMO:no_of_time:no_of_months,:,:]

    
    # For number of dimensions = 4
    if (num_of_dim == 4):
        for nyr in range(no_year_start, (no_year_last+1)):
            n = nyr*no_of_months + NMO
            da_new[n,:,:,:] = (xMon[(n-1),:,:,:] + xMon[n,:,:,:] + xMon[(n+1),:,:,:]) * con
        
        if (NMO == 0):
            n = 0
            da_new[0,:,:,:] = (xMon[n,:,:,:] + xMon[(n+1),:,:,:])*0.5
        
        if (NMO == (no_of_months-1)):
            n = (no_of_years-1)*no_of_months + NMO
            da_new[(n),:,:,:] = (xMon[n,:,:,:] + xMon[(n-1),:,:,:])*0.5
        
        da_new = da_new[NMO:no_of_time:no_of_months,:,:,:]
                                  
        
    # Add and update the attributes
    da_new = da_new.rename("x"+SEASON)
    da_new.attrs['NMO'] = NMO
    da_new.attrs['long_name'] = SEASON + ": " + da_new.attrs['long_name']
    da_new.encoding = xMon.encoding      
    # Return the newly created DataArray
    return da_new


