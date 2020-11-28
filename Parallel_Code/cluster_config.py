"""
##================================================================
## Routine          : cluster_config.py
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


# Import Libraries

import dask
import distributed
from dask_jobqueue import PBSCluster


def cluster_spec(workers_count):
    """
    ------------------------------------------------------------------------------------------------
    Usage: This file can be used to specify cluster configurations and select the number of workers
    -------------------------------------------------------------------------------------------------
    Parameters:
		workers: specify the number of workers to scale
    
    Return: Cluster configuration that can be passed to dask scheduler (client)
    """

    cluster = PBSCluster(queue='research',
                     project='DaskOnPBS',
                     local_directory='DASK_OUT/',
                     log_directory='DASK_OUT/',
                     cores=workers_count,
                     processes=1,
                     memory='40GB',
                     walltime='24:00:00',
                     resource_spec='select=1:ncpus=36:mem=40GB:vntype=cray_compute',
                     env_extra=['aprun -n 1'])
    
    cluster.scale(workers_count)
    
    return cluster

