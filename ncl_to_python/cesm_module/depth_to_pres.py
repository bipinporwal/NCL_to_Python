
"""
##================================================================
## Routine          : depth_to_pres.py
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
import math

def depth_to_pres(z,opt):
	
	"""Convert ocean depth to pressure

    Parameters
    ----------
    z : A single dimensional array or list containing ocean depth (meters).
    opt: Options.

    Returns
    -------
    pres: It will have units of bars. It will be the same size,shape and type as z.

    """
	
	
	nd=len(z)
	depth_msg=0.0
	c1=1.0
	pressure=[0]*nd
	pres=[0]*nd
	
	if(opt==1):
		for n in range (0,nd):
    			if(z[n]==depth_msg):
    				pressure[n] = depth_msg
    			else:
    				pressure[n] = 0.059808*(math.exp(-0.025*z[n]) - c1) + 0.100766*z[n]+(2.28405e-7)*z[n]**2
	else:
		for n in range (0,nd):
			pressure[n] = 0.059808*(math.exp(-0.025*z[n]) - c1) + 0.100766*z[n]+(2.28405e-7)*z[n]**2

	for n in range (0,nd):
		pres[n]=round(pressure[n],4)
                                                                                          
    
    # Return the new list
	return pres

