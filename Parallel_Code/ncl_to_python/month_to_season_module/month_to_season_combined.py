"""
##================================================================
## Routine          : month_to_season_combined.py
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
# Import the required libraries
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import xarray as xr


def month_to_season_combined(xMon, *SEASONS):
    """Computes a user-specified list of three-month seasonal means (DJF, JFM, FMA, MAM, AMJ, MJJ, JJA, JAS, ASO, SON, OND, NDJ).

    
    Parameters
    ----------
    xMon : A one-, three-, or four-dimensional DataArray [darray(time) or darray(time,lat,lon) or darray(time,lev,lat,lon)] of any numeric type. xMon must have named dimensions and the time (leftmost) dimension must be divisible by 12.
           The data are assumed to be monthly mean data and the first record is assumed to be January.
    
    *SEASONS : (Optional) A string or an array of strings representing the seasons to calculate: e.g.,"JJA" or "DJF","JJA".


    Returns
    -------
    objectDataArray : The return value will be of the same type and dimension as xMon. Depending on the function you select it may or may not
                      add dimension/attributes.

    """
    
    # month_to_season12 function
    def month_to_season12(xMon):
    
        # xMon is the DataArray passed as an argument

        # Create a new array of seasons
        season = np.array(["DJF","JFM","FMA","MAM","AMJ","MJJ","JJA","JAS","ASO","SON","OND","NDJ"])

        # Get the number of dimensions of dataarray
        len_of_dim = xMon.sizes
        num_of_dim = len(len_of_dim)

        # Check if the number of dimensions of dim is valid or invalid; if invalid, exit the function
        if (num_of_dim == 2 or num_of_dim >= 5):
            print("month_to_season12: number of dimensions = {}".format(num_of_dim))
            print("----- Dimension currently not handled -----")
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
            dr[0].values = (xMon[0] + xMon[1]) * 0.5
            dr[(no_of_time-1)].values = (xMon[(no_of_time-2)] + xMon[(no_of_time-1)]) * 0.5

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
            dr[0,:,:].values = (xMon[0,:,:] + xMon[1,:,:]) * 0.5
            dr[(no_of_time-1),:,:].values = (xMon[(no_of_time-2),:,:] + xMon[(no_of_time-1),:,:]) * 0.5

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
            dr[0,:,:,:].values = (xMon[0,:,:,:] + xMon[1,:,:,:]) * 0.5
            dr[(no_of_time-1),:,:,:].values = (xMon[(no_of_time-2),:,:,:] + xMon[(no_of_time-1),:,:,:]) * 0.5

            # Create a new DataArray using the existing ones
            xSea = xMon.copy(data = dr)

            # Add and update the attributes
            xSea.attrs['season'] = season
            xSea.attrs['long_name'] = "seasonal means: " + xSea.attrs['long_name']
            xSea = xSea.rename("xSea")
            xSea.encoding = xMon.encoding

            # Return the newly created DataArray
            return xSea
    
    
    # month_to_season function
    def month_to_season(xMon, SEASON):
    
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
                da_new[n].values = (xMon[n-1] + xMon[n] + xMon[n+1]) * con

            if (NMO == 0):
                n = 0
                da_new[n].values = (xMon[n] + xMon[n+1])*0.5

            if (NMO == (no_of_months-1)):
                n = (no_of_years-1)*no_of_months + NMO
                da_new[n].values = (xMon[n] + xMon[n-1])*0.5

            da_new = da_new[NMO:no_of_time:no_of_months]               

        # For number of dimensions = 3
        if (num_of_dim == 3):
            for nyr in range(no_year_start, (no_year_last+1)):
                n = nyr*no_of_months + NMO
                da_new[n,:,:].values = (xMon[(n-1),:,:] + xMon[n,:,:] + xMon[(n+1),:,:]) * con

            if (NMO == 0):
                n = 0
                da_new[n,:,:].values = (xMon[n,:,:] + xMon[(n+1),:,:])*0.5

            if (NMO == (no_of_months-1)):
                n = (no_of_years-1)*no_of_months + NMO
                da_new[n,:,:].values = (xMon[n,:,:] + xMon[(n-1),:,:])*0.5

            da_new = da_new[NMO:no_of_time:no_of_months,:,:]


        # For number of dimensions = 4
        if (num_of_dim == 4):
            for nyr in range(no_year_start, (no_year_last+1)):
                n = nyr*no_of_months + NMO
                da_new[n,:,:,:].values = (xMon[(n-1),:,:,:] + xMon[n,:,:,:] + xMon[(n+1),:,:,:]) * con

            if (NMO == 0):
                n = 0
                da_new[0,:,:,:].values = (xMon[n,:,:,:] + xMon[(n+1),:,:,:])*0.5

            if (NMO == (no_of_months-1)):
                n = (no_of_years-1)*no_of_months + NMO
                da_new[(n),:,:,:].values = (xMon[n,:,:,:] + xMon[(n-1),:,:,:])*0.5

            da_new = da_new[NMO:no_of_time:no_of_months,:,:,:]


        # Add and update the attributes
        da_new = da_new.rename("x"+SEASON)
        da_new.attrs['NMO'] = NMO
        da_new.attrs['long_name'] = SEASON + ": " + da_new.attrs['long_name']
        da_new.encoding = xMon.encoding

        # Return the newly created DataArray
        return da_new
    
    
    
    
    def month_to_seasonN(xMon, *SEASON):

        # xMon is the DataArray and *SEASON are the seasons passed as an argument

        # Create a new array of seasons
        season = np.array(["DJF","JFM","FMA","MAM","AMJ","MJJ","JJA","JAS","ASO","SON","OND","NDJ"])
        N = len(SEASON)

        # Check if the SEASON argument is present in season array
        for i in SEASON:
            if i not in season:
                print("month_to_seasonN: You have atleast one spelling error " + 
                      "in your SEASON specification. {} is not valid.".format(i))
                return None

        # Get the number of dimensions of dataarray
        len_of_dim = xMon.sizes
        num_of_dim = len(len_of_dim)

        # Check if the number of dimensions of dim is valid or invalid; if invalid, exit the function
        if (num_of_dim == 2 or num_of_dim >= 5):
            print("month_to_season12: number of dimensions = {}".format(num_of_dim))
            print("----- dimension currently not handled -----")
            return None

        # Check if number of months are multiple of 12; if not, exit the function
        no_of_months = 12
        no_of_time = len_of_dim[xMon.dims[0]]
        if ((no_of_time % no_of_months) != 0):
            print("month_to_season12: dimension must be a multiple of 12")
            return None
        no_of_years = no_of_time/no_of_months

        # Call the month_to_season12 function
        xSea12 = month_to_season12(xMon)


        # Store the size of latitude and longitude
        if (num_of_dim >= 3):
            size_of_lat = len_of_dim[xMon.dims[num_of_dim-2]]
            size_of_lon = len_of_dim[xMon.dims[num_of_dim-1]]

        # Check the index of first SEASON passed in season array
        i = SEASON[0]
        NMO1 = np.where(season==i)[0].item()

        xSeaN = xSea12.copy()

        # Store the SEASONS in a numpy array
        sea = np.array([], dtype ='int')
        sea_code = np.array([], dtype = 'str')

        for n in range(0, N):
            NMO = np.where(season==SEASON[n])[0].item()
            sea = np.append(sea, NMO)
            sea_code = np.append(sea_code, season[NMO])

        # Calculations for number of dimensions = 1
        if (num_of_dim == 1):
            for ns in range(0,N):
                NMO = np.where(season==SEASON[ns])[0].item()
                if(NMO == sea[0]):
                    xSeaN = xSea12[NMO:no_of_time:no_of_months]
                else:
                    xS = xSea12[NMO:no_of_time:no_of_months]
                    xSeaN = xr.concat([xSeaN, xS], "season")

        # Calculating seasonal mean for number of dimensions = 3
        if (num_of_dim == 3):
            for ns in range(0,N):
                NMO = np.where(season==SEASON[ns])[0].item()
                if (NMO == sea[0]):
                    xSeaN = xSea12[NMO:no_of_time:no_of_months,:,:]
                else:
                    xS = xSea12[NMO:no_of_time:no_of_months,:,:]
                    xSeaN = xr.concat([xSeaN, xS], 'season')


        # Calculating seasonal mean for number of dimensions = 4
        if (num_of_dim == 4):
            for ns in range(0,N):
                NMO = np.where(season==SEASON[ns])[0].item()
                if (NMO == sea[0]):
                    xSeaN = xSea12[NMO:no_of_time:no_of_months,:,:,:]
                else:
                    xS = xSea12[NMO:no_of_time:no_of_months,:,:,:]
                    xSeaN = xr.concat([xSeaN, xS], 'season')


        # Add and update the attributes
        if(xSeaN.attrs['long_name'] or xSeaN.attrs['description'] or xSeaN.attrs['standard_name']):
            xSeaN.attrs['long_name'] = "Seasonal Means: " + xSeaN.attrs['long_name']

            # Since the season co-ordinate contains indexes of data, we replace 
            # with the actual season string.
            xSeaN = xSeaN.assign_coords({'season':sea_code})
            xSeaN=xSeaN.rename("xSeaN")
            xSeaN.encoding=xMon.encoding


            # Return the newly created DataArray
            return xSeaN

    
    if (len(SEASONS) == 0):
        return month_to_season12(xMon)
    elif (len(SEASONS) == 1):
        return month_to_season(xMon, *SEASONS)
    elif (len(SEASONS) > 1):
        return month_to_seasonN(xMon, *SEASONS)
   


