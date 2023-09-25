import netCDF4
import xarray as xr
import os

def SF_getm(SFdata, SFmonth, ensNumber):
    '''Returns data only for the desired month and ensemble member'''
    mgroups = SFdata.groupby('time.month').groups # Turn each month into a group
    mdata = SFdata.isel(time = mgroups[list(mgroups)[SFmonth - 1]], number = ensNumber) # Select all days within the desired month's group, only from the desired ensemble member
    extraday = SFdata.isel(time = mgroups[list(mgroups)[SFmonth]][0], number = ensNumber) # Add the first day of the next month because seasonal forecasts seem to always start on the 2nd. This will result in each month consisting of the 2nd of the current month through the 1st of the next month
    return(xr.concat([mdata,extraday], dim = 'time')) # Concatenate the month together and return



folder_path = 'C:/Users/alexm/OneDrive/Documents/WaterJade/Downscaling/data/'
folder_path = folder_path +'/' #make sure there's an / at the end or else os.path.join will add a \ instead. Having a // is ok

# Use os.listdir() to get a list of all files in the folder
file_list = os.listdir(folder_path)

# Create empty lists to hold data for each forecast month, to be concatenated later
yearset = []
m1datasets = []
m2datasets = []
m3datasets = []
m4datasets = []
m5datasets = []
m6datasets = []
m7datasets = []

ensNumber = 0

# Read each dataset and split it by months, dumping each month into a different list
for file_name in file_list: # Loop over all files available
    file_path = os.path.join(folder_path, file_name) # Make the filepath for the file

    # Open the netCDF4 file
    nc_file = netCDF4.Dataset(file_path, 'r')  # open netCDF at file_path
    xdata = xr.open_dataset(xr.backends.NetCDF4DataStore(nc_file)) # Convert it to xarray
    m1datasets.append(SF_getm(xdata, 1, ensNumber))
    m2datasets.append(SF_getm(xdata, 2, ensNumber))
    m3datasets.append(SF_getm(xdata, 3, ensNumber))
    m4datasets.append(SF_getm(xdata, 4, ensNumber))
    m5datasets.append(SF_getm(xdata, 5, ensNumber))
    m6datasets.append(SF_getm(xdata, 6, ensNumber))
    m7datasets.append(SF_getm(xdata, 7, ensNumber))
    yearset.append(xdata.isel(time = 0)['time.year'].values)
    yearset.append(xdata.isel(time = -1)['time.year'].values)
    nc_file.close()

datasetlist = [m1datasets,m2datasets,m3datasets,m4datasets,m5datasets,m6datasets,m7datasets]

# Find initial and final years
startyear = min(yearset)
stopyear = max(yearset)

# Concatenate into a GCM-like complete time series, then write to a netCDF in the lres folder
month = 0
while month < 7:
    input = xr.concat(datasetlist[month], dim = 'time')
    writename = f"SF{startyear}-{stopyear}m{month+1}_ens{ensNumber}.nc"
    writepath = os.path.join('C:/Users/alexm/pyClim-SDM_playground/input_data/models/', writename)
    input.to_netcdf(path = writepath, mode = 'w')
    month+=1

print('Seasonal forecast data has been preprocessed for downscaling.')