NCL to Python
===========================================

**Title of Manuscript**:
 * On the development of NCL equivalent serial and parallel Python routines for meteorological data analysis.

___


Requirements
-------------

* Anaconda environment with python version > 3.0
* To run the scripts on a local machine, good system specifications are:
  * Processor = Intel i5 or higher
  * Memory = 8GB RAM or higher

* Install the following packages:
  * xarray (version - 0.14)
  * dask (version - 2.5.2)
  * distributed (version - 2.5.2)
  * netCDF (version 1.5.4)

____

### Datasets

The datasets are available at [CESM Large Ensemble Community website](http://www.cesm.ucar.edu/projects/community-projects/LENS/data-sets.html)

The datasets we used for testing are mentioned below:

| SN   | File Name                                                    | Variable                           | Time Step |
| ---- | ------------------------------------------------------------ | ---------------------------------- | --------- |
| 1.   | b.e11.B1850C5CN.f09g16.005.pop.h.TEMP.040001-049912.nc       | TEMP -Potential Temperature        | Monthly   |
| 2.   | b.e11.BRCP85C5CNBDRD.f09_g16.032.cam.h0.AQRAIN.200601-208012.nc | AQRAIN - Average rain mixing ratio | Monthly   |
| 3.   | f.e11.F1850C5CN.f09f09.001.clm2.h0.RAIN.230001-239912.nc     | RAIN - Atmospheric Rain            | Monthly   |
| 4.   | b.e11.B1850C5CN.f09_g16.005.cice.h.fsalt_nh.040001-049912.nc | fsalt - Salt Flux (ice to ocean)   | Monthly   |
| 5.   | b.e11.B1850C5CN.f09_g16.005.cam.h1.FLNS.05000101-05991231.nc | FLNS - Surface Flux                | Daily     |
| 6.   | b.e11.BRCP85C5CNBDRD.f09_g16.001.pop.h.nday1.SST.20810101-21001231.nc | SST - Sea Surface Temperature      | Daily     |

____

**NOTE:** 

1. While running the scripts, set the path of the input file (dataset). The path can be set inside INPUT_PATH.txt / INPUT_PATH1.txt files.

2. It is mandatory to import the functions on which operations can be performed. These are present in the submodules present in ncl_to_python module. For example, to import month_to_season12 function use:

   ```python
   from ncl_to_python.month_to_season_module import month_to_season12
   ```

   Similarly to import calculate_monthly_values module use:

   ```python
   from ncl_to_python.calculate_monthly_values_module import calculate_monthly_values
   ```

3. The entire testing was done on Pratyush Supercomputer. Since it uses PBS Job Script to submit the jobs in cluster, we used PBSCluster function inside the parallel version of the scripts. However to test the functions on a local multi-core computer, PBSCluster function should be commented and instead direct dask-scheduler connection needs to setup.

4. To run the test on any other HPC cluster (SLURM, LSF, etc.), Example Deployment are available at this [dask-jobqueue website](https://jobqueue.dask.org/en/latest/examples.html)

5. To run the parallel version of scripts using dask-jobqueue, use the following command:

   ```bash
   python filename.py 4
   ```

   Here '4' is the number of workers assigned. This number can be changed from 1 to maximum number of cores available in the cluster.

6. Python has GIL issues and hence, for best results, avoid using threads.

____

### Sample to run serial scripts on a local computer

**NOTE:** To run these scripts, download ncl_to_python module (folder) from [here](https://github.com/bipinporwal/NCL_to_Python/tree/master/Parallel_Code/).

* Test script to run functions serially:

  ```python
  # Import the libraries
  import xarray as xr
  import sys
  # Search modules in parent folder
  sys.path.insert(1, '..')
  from ncl_to_python.calculate_monthly_values_module import *
  import time
  
  # Enter the path to the dataset
  
  path = open("INPUT_PATH.txt")
  # Read the dataset path
  path1 = path.read()
  path1 = path1.rstrip('\n')
  # Open dataset using xarray
  ds = xr.open_dataset(path1)
  # Read the datavariable. This can be different based on the dataset used.
  var = ds["FLNS"]
  
  # Set the opt variable to True/False and assign a value to critical value (nval_crit)
  opt = xr.DataArray(data = False)
  opt.attrs["nval_crit"] = 30
  
  
  strt = time.time()
  
  # Call/Execute the calculate_monthly_values function sequentially
  result = calculate_monthly_values(var, "avg", 0, opt)
  end = time.time()
  
  print(result)
  
  path.close()
  ```

  To run this script use the following command:

  ```bash
  python filename.py
  ```

  

* Test script to run functions parallely:

  ```python
  # Import libraries
  import sys
  sys.path.insert(1, '../..')
  
  import xarray as xr
  from dask.distributed import Client, LocalCluster
  #from dask_jobqueue import PBSCluster
  from ncl_to_python.month_to_season_module import *
  from dask import compute
  import dask
  import distributed
  import time
  
  # Comment the lines below
  '''
  cluster = PBSCluster(queue='research',
                       project='DaskOnPBS',
                       local_directory='/lus/dal/hpcs_rnd/Python_Data_Analysis/Jatin/ncl_to_python_v3/Parallel_Function_Testing/month_2_season/DASK_OUT/',
                       cores=1,
                       processes=1,
                       memory='40GB',
                       walltime='24:00:00',
                       resource_spec='select=1:ncpus=36:mem=40GB:vntype=cray_compute',
                       env_extra=['aprun -n 1'])
  
  j = sys.argv[1]
  # Scale clusters to add j workers (j= number of jobs)
  cluster.scale(j)
  '''
  
  # Set up the cluster configuration for local-machine. You can choose the total number of workers to use using "n_workers = " option in LocalCluster() function. If unspecified, it uses the maximum number of cores available inside the machine. Please also note that Python has GIL issues and hence, for best results, avoid using threads.
  if __name__=="__main__":
      cluster = LocalCluster()
      client = Client(cluster)
  
  # Enter the path to the dataset
  path = open("INPUT_PATH.txt")
  path1 = path.read()
  path1 = path1.rstrip('\n')
  
  # Open the dataset parallelly using dask and create proper chunks.
  ds = xr.open_mfdataset(path1, chunks = {'lat':60, 'lon':60}, parallel = True)
  
  # Extract the variable. This can be different depending on the dataset used.
  var = ds["AQRAIN"]
  
  strt = time.time()
  # Send the function to workers for parallel execution
  result = month_to_season12(var).compute()
  end = time.time()
  
  # Shutdown the client, workers and jobs running
  if __name__=="__main__":
      client.shutdown()
  
  print(result)
  
  # Calculate the difference of start and end time taken by the function.
  print("Time taken by the function: {} seconds".format(end-strt))
  
  path.close()
  ```
  
  To run this script, use the following command:
  
  ```bash
  python filename.py
  ```
  
  