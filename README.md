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
  * Create a virtual environment in Python by entering the following command in terminal:

    `python -m virtualenv my_venv`

    where `my_venv` is the name of your virtual environment.

  * Activate the virtual environment by entering the following command:

    `source my_venv/bin/activate`

  * Run the following commands to install all the required python packages:

    `pip install -r requirements.txt`

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

1. **To see what extra arguments are required while running any function, use `python filename.py -h`.**

2. It is mandatory to import the functions on which operations can be performed. These are present in the submodules present in ncl_to_python module. For example, to import month_to_season12 function use:

   ```python
   from ncl_to_python.month_to_season_module import month_to_season12
   ```

   Similarly to import calculate_monthly_values module use:

   ```python
   from ncl_to_python.calculate_monthly_values_module import calculate_monthly_values
   ```

3. The entire testing was done on Pratyush Supercomputer. Since it uses PBS Job Script to submit the jobs in cluster, we used PBSCluster function inside the parallel version of the scripts. However to test the functions on a local multi-core computer, PBSCluster function should be commented and instead direct dask-scheduler connection needs to setup.

4. To run the test on any other HPC cluster (SLURM, LSF, etc.), Example Deployment are available at this [dask-jobqueue website](https://jobqueue.dask.org/en/latest/examples.html).

5. Most serial functions require dataset path and variable name to be passed as an argument while executing the script from terminal. The variable name (e.g. AQRAIN, FLNS, SST, etc.) and dimensions (lat, lon, etc.) of any netCDF4 dataset can be found by executing the following command in terminal:

   `ncdump -h filename.nc` , where filename.nc is the filename

6. The serial test scripts can be executed by entering the command in this syntax:

   `python serial_filename.py /path/to/dataset/filename.nc variable_name`

   **NOTE:** Some functions require more than two extra command line arguments.

7. To run the parallel version of scripts using dask-jobqueue, use the following command syntax:

   ```bash
   python filename.py /path/to/dataset/filename.nc variable_name -w 8 -c '{"key":value}'
   ```

   where `-w or --workers` represents the number of workers to use and `-c or --chunks` represent the chunk details. An example is given below:

   `python clmTLLL.py /home/user/Datasets/b.e11.BRCP85C5CNBDRD.f09_g16.032.cam.`

    `h0.AQRAIN.200601-208012.nc AQRAIN -w 32 -c '{"lat":75, "lon":75}' `

   The total size of any coordinate can be found using `ncdump -h filename.nc` command.

   Here '32' is the number of workers assigned. This number can be changed from 1 to maximum number of cores available in the cluster.

8. A single cluster file named *cluster_config.py* has been created and can be modified according to your cluster specifications. This file is available [here](https://github.com/bipinporwal/NCL_to_Python/tree/master/Parallel_Code).

9. Python has GIL issues and hence, for best results, avoid using threads.

____

### Sample to run code on a local computer

**NOTE:** To run these scripts, download ncl_to_python module (folder) from [here](https://github.com/bipinporwal/NCL_to_Python/tree/master/ncl_to_python/).

* Test script to run functions serially:

  ```python
  # Import the required libraries
  import xarray as xr
  import sys
  sys.path.insert(1, '..')
  from ncl_to_python.calculate_monthly_values_module import *
  import argparse
  
  
  # Fetch the dataset path, data-variable name, season name using argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("filepath", type=str, help="Enter the dataset/file path")
  parser.add_argument("variable", type=str, help="Enter the variable/dataarray to extract from dataset")
  parser.add_argument("statistic", type=str, help="Enter the statistic to calculate. e.g. avg, \
                                                   The list of arguements that can be passed are: \
                                                   'avg' = average, \
                                                   'sum' = sum, \
                                                   'min' = minimum, \
                                                   'max' = maximum, \
                                                   'var' = variance, \
                                                   'std' = standard deviation.")
  parser.add_argument("opt", type=bool, help="Set opt either 'True' or 'False'")
  parser.add_argument("-n", "--nval_crit", type=int, default=1, help="If opt is set 'True', enter nval_crit value (default nval_crit = 0)")
  
  args = parser.parse_args()
  
  # Extract path, variable name, season from args namespace
  path = args.filepath
  var_name = args.variable
  stat = args.statistic
  opt_val = args.opt
  nval_crit = args.nval_crit
  
  # Open dataset
  try:
      ds = xr.open_dataset(path)
  except IOError:
      print("Incorrect path, file not found")
      exit()
  
  # Extract variable from dataset
  try:
      var = ds[var_name]
  except KeyError:
      print("Incorrect variable name. Variable '{}' not found in dataset".format(var_name))
      exit()
  
  
  opt = xr.DataArray(data = opt_val)
  opt.attrs["nval_crit"] = nval_crit
  
  
  result = calculate_monthly_values(var, stat, 0, opt)
  
  print(result)
  
  ds.close()
  
  ```

  To run this script use the following command:

  ```bash
  python filename.py /path/to/dataset/dataset.nc variable_name avg False
  ```

  

* Test script to run functions parallely:

  ```python
  # Import Libraries
  import sys
  sys.path.insert(1, '../..')
  sys.path.insert(1, '../')
  
  import xarray as xr
  from dask.distributed import Client
  from dask_jobqueue import PBSCluster
  from ncl_to_python.month_to_season_module import *
  from dask import compute
  import dask
  import distributed
  import time
  from cluster_config import cluster_spec
  import argparse
  import json
  
  # Fetch the dataset path, data-variable name, season name using argparse
  parser = argparse.ArgumentParser()
  parser.add_argument("filepath", type=str, help="Enter the dataset/file path")
  parser.add_argument("variable", type=str, help="Enter the variable/dataarray to extract from dataset")
  
  args = parser.parse_args()
  
  # Extract path, variable name, season from args namespace
  path = args.filepath
  var_name = args.variable
  
  # Set up the cluster configuration for local-machine. You can choose the total number of workers to use using "n_workers = " option in LocalCluster() function. If unspecified, it uses the maximum number of cores available inside the machine. Please also note that Python has GIL issues and hence, for best results, avoid using threads.
  if __name__=="__main__":
      cluster = LocalCluster()
      client = Client(cluster)
  
  
  try:
      ds = xr.open_mfdataset(path, chunks = chunk_details, parallel=True)
  except IOError:
      print("Incorrect path, file not found")
      exit()
  
  # Extract variable from dataset
  try:
      var = ds[var_name]
  except KeyError:
      print("Incorrect variable name. Variable '{}' not found in dataset".format(var_name))
      exit()
  
  
  strt = time.time()
  result = month_to_season12(var).compute()
  end = time.time()
  
  
  # Shutdown the client, workers and jobs running
  if __name__=="__main__":
      client.shutdown()
  
  print(result)
  print("Time taken by the function: {} seconds".format(end-strt))
  
  ds.close()
  
  ```
  
  To run this script, use the following command:
  
  ```bash
  python filename.py /path/to/dataset/dataset.nc variable_name
  ```
  
  