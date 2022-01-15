
"""
##================================================================
## Routine          : dpres_hybrid_ccm.py
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
import pandas as pd
import numpy as np
import math

def dpres_hybrid_ccm(x,p0,hyam,hybm):

	"""Calculates the pressure layer thicknesses of a hybrid coordinate system. 

	Parameters
   	----------
   	x: An array of at least 2 dimensions containing surface pressure data in Pa or hPa (mb). The two rightmost dimensions must be latitude and longitude.
   	
    	p0: A scalar value equal to the surface reference pressure. Must have the same units as ps. 
    	
	hyam: A one-dimensional array equal to the hybrid A interface coefficients. 
	
	hybm: A one-dimensional array equal to the hybrid B interface coefficients. 
	
    	Returns
    	-------
    	ph: If ps is two-dimensional [e.g. (lat,lon)] or three-dimensional [e.g. (time,lat,lon)] then the return array will have an additional level dimension: (lev,lat,lon) or 			    (time,lev,lat,lon), respectively. The size of the lev dimension is one less then the size of hyai. The returned type will be double if ps is double, float otherwise.

    	"""
	#x = x[0:8,0:8,0:8]
	e = x.shape
	i = e[0]
	j = e[1]
	k = e[2]
	ph = np.ndarray(shape=(i,len(hyam)-1,j,k))
	
	#Calculates the pressure layer thicknesses of a hybrid coordinate system.
	for a in range(0,i):
		for b in range(0,len(hyam)-1):
			for c in range(0, j):
				for d in range(0, k):
					ph[a][b][c][d] = abs((hyam[b]*p0[0] + hybm[b]*x[a][c][d])-(hyam[b+1]*p0[0] + hybm[b+1]*x[a][c][d]))
                
    
    # Return the new dataarray
	return ph

