"""
##================================================================
## Routine          : omega_ccm.py
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

def omega_ccm(u, v, d, dpsl, dpsm, pmid, pdel, psfc, hybd, hybm, nprlev):

  """Calculates vertical pressure velocity (time,lat,lon version)
  
  Parameters
  ----------
	u: An array of 3 or 4 dimensions containing zonal wind component. The three rightmost dimensions must be level x lat x lon [e.g. U(time,lev,lat,lon)]. The order of the level dimension must be top-to-bottom.

	v: An array of 3 or 4 dimensions containing meridional wind component. Same dimension structure as u.

	div: An array of 3 or 4 dimensions containing divergence. Same dimension structure as u.

	dpsl: An array of 3 or 4 dimensions containing longitudinal component of grad ln(psfc). Same dimension structure as u.

	dpsm: An array of 3 or 4 dimensions containing latitudinal component of grad ln(pfc). Same dimension structure as u.

	pmid: An array of 3 or 4 dimensions containing mid-level pressure values. Same dimension structure as u.

	pdel: An array of 3 or 4 dimensions containing layer pressure thickness values. Same dimension structure as u.

	psfc: An array of 2 or 3 dimensions containing surface pressure [Pa]. The two rightmost dimensions must be lat x lon [e.g. PSFC(time,lat,lon)].

	hybdif: A one-dimensional array containing the difference between the hybrid interface coefficients [eg, hybi(k+1)-hybi(k)]. The size is the size of the level dimension of u. The order must be top-to-bottom.

	hybm: A one-dimensional array containing the hybrid B coefficients. Must have the same dimension as the level dimension of u. The order must be top-to-bottom.

	nprlev: Number of pure pressure levels (i.e. the number of levels where the sigma component of the hybrid coefficients is zero).

  Returns
  -------
  omega: vertical pressure velocity. Has the same dimensions as u."""

  o=u.shape
  klev = o[2]
  jlat = o[1]
  ilon = o[0]

  hkk=np.ndarray(shape=(ilon,jlat))
  hlk=np.ndarray(shape=(ilon,jlat))
  suml=np.ndarray(shape=(ilon,jlat))
  rpmid=np.ndarray(shape=(ilon,jlat,klev))
  omega=np.ndarray(shape=(ilon,jlat,klev))
    
  for j in range(0,jlat):
    for i in range(0,ilon):
      suml[i][j]=0
        
  for k in range(0,klev):
    for j in range(0,jlat):
      for i in range(0,ilon):
        rpmid[i][j][k] = 1/pmid[i][j][k]
          
  for j in range(0,jlat):
    for i in range(0,ilon):
      hkk[i][j]     = 0.5*rpmid[i][j][0]
      omega[i][j][0]= -(hkk[i][j])*d[i][j][0]*pdel[i][j][0]
      suml[i][j]   = suml[i][j] + d[i][j][0]*pdel[i][j][0]
        
  if (1>=nprlev[0]):
    for j in range(0,jlat):
      for i in range(0,ilon):
        vgpk = (u[i][j][0]*dpsl[i][j] + v[i][j][0]*dpsm[i][j])*psfc[i][j]
        tmp = vgpk*hybd[0]
        omega[i][j][0]= omega[i][j][0] + hybm[0]*rpmid[i][j][0]*vgpk - hkk[i][j]*tmp
        suml[i][j] = suml[i][j]+ tmp
          
  for k in range(1,klev-1):
    for j in range(0,jlat):
      for i in range(0,ilon):
        hkk[i][j]    = 0.5*rpmid[i][j][k]
        hlk[i][j]     = rpmid[i][j][k]
        omega[i][j][k] = -hkk[i][j]*d[i][j][k]*pdel[i][j][k] - hlk[i][j]*suml[i][j]
        suml[i][j]    = suml[i][j]  + d[i][j][k]*pdel[i][j][k]
          
    if(k>=nprlev[0]):
      for j in range(0,jlat):
        for i in range(0,ilon):
          vgpk=(u[i][j][k]*dpsl[i][j] + v[i][j][k]*dpsm[i][j])*psfc[i][j]
          tmp = vgpk*hybd[k]
          omega[i][j][k] = omega[i][j][k] + hybm[k]*rpmid[i][j][k]*vgpk- hkk[i][j]*tmp
          suml[i][j]    = suml[i][j]  + tmp
            
  for j in range(0,jlat):
    for i in range(0,ilon):
      hkk[i][j] = 0.5*rpmid[i][j][klev-1]
      hlk[i][j]=     rpmid[i][j][klev-1]
      omega[i][j][klev-1] = - (hkk[i][j]*d[i][j][klev-1]*pdel[i][j][klev-1]) - (hlk[i][j]*suml[i][j])
        
        
  if(klev>=nprlev[0]):
    for j in range(0,jlat):
      for i in range(0,ilon):
        vgpk=(u[i][j][klev-1]*dpsl[i][j] + v[i][j][klev-1]*dpsm[i][j])*psfc[i][j]
        omega[i][j][klev-1] = omega[i][j][klev-1] + hybm[klev-1]*rpmid[i][j][klev-1]*vgpk - hkk[i][j]*vgpk*hybd[klev-1]
          
  for k in range(0,klev):
    for j in range(0,jlat):
      for i in range(0,ilon):
        omega[i][j][k] = omega[i][j][k]*pmid[i][j][k]
          
          
  return omega
  
