
"""
##================================================================
## Routine          : potmp_insitu_ocn.py
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

def potmp_insitu_ocn(t,s,pres,pref,dim,opt):

	"""Convert seawater potential temperature at an arbitraryreference pressure given insitu temperature, salinitty and depth.

    Parameters
    ----------
	t: A scalar or array containing insitu temperature (degC). This must be the same size and shape as s.
	s: A scalar or array containing salinity (g/kg). This must be the same size and shape as t.
	pres:Ocean pressure (decibars) corresponding to each t and s.
	pref:Ocean reference pressure (decibars). Usually, this is 0.0
	dims:The dimension(s) of t to which pres correspond. Must be consecutive and monotonically increasing.
	opt: Options. When calculating potential temperature, this should be set to False. If opt=True and the attribute opt@reverse=True then the input temperatures are potential temperatures and the returned temperatures will be 'observed' temperature. 

    Returns
    -------
    result: An array. This has same size and shape as t,s,pres.

    """
	result=[]
	len_list=len(t)
	for k in range(0,len_list):
		s1=s[k]-35
		dp=pref[0]-pres[k]
		n  = round(abs(dp)/1000.0) + 1
		dp = dp/n
		for i in range(0,n):
			for j in range(0,4):
				r1 = (((-2.1687e-16) *  t[k] + (1.8676e-14)) * t[k] - (4.6206e-13) )*  pres[k]
				r2=((2.7759e-12)*t[k]-(1.1351e-10))*s1
				r3=(((-5.4481e-14)*t[k]+(8.733e-12))*t[k]-(6.7795e-10))*t[k]
				r4 = (r1+(r2+r3+1.8741e-8))*pres[k]+((-4.2393e-8)*t[k]+(1.8932e-6))*s1
				r5 = r4+(((6.6228e-10)*t[k]-(6.836e-8))*t[k]+(8.5258e-6))*t[k]+(3.5803e-5)
		
				x=dp*r5
		
				if(j==0):
					t[k] = t[k]+0.5*x
					q = x
					pres[k] = pres[k] + 0.5*dp
			
				elif(j==1):
					t[k] = t[k] + 0.29298322*(x-q)
					q = 0.58578644*x + 0.121320344*q
			
				elif(j==2):
					t[k] = t[k] + 1.707106781*(x-q)
					q = 3.414213562*x - 4.121320344*q
					pres[k] = pres[k] + 0.5*dp
			
				elif(j==3):
					t[k] = t[k] + ((x-2.0*q)/6.0)
			
		result.append(t[k])
    
    # Return the new list
	return result

