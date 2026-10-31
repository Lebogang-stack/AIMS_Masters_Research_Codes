import xarray as xr


def compute_daily_max_temperature(input_filepath, output_filepath):
    """Reads ERA5 hourly 2m temperature NetCDF data, calculates the daily

    maximum temperature, and exports the result to a new NetCDF file.
    """
    # 1. Open the ERA5 hourly NetCDF dataset
    # xarray automatically parses NetCDF metadata and dimensions (time, latitude, longitude)
    print(f"Opening input file: {input_filepath}...")
    ds = xr.open_dataset(input_filepath)

    # Note: ERA5 2m temperature is usually named 't2m' or '2t'
    # Check for the correct variable name in your dataset
    temp_var = "t2m" if "t2m" in ds else "2t"

    if temp_var not in ds:
        raise KeyError(
            f"Could not find 2m temperature variable in dataset. Available variables: {list(ds.data_vars)}"
        )

    # 2. Resample/group by day ('1D' or 'D') and calculate the maximum
    print("Computing daily maximum temperatures...")
    daily_max_ds = ds[[temp_var]].resample(time="1D").max(dim="time")

    # 3. Update metadata/attributes for clarity
    daily_max_ds[temp_var].attrs["long_name"] = "Daily Maximum 2 metre temperature"
    daily_max_ds.attrs["history"] = (
        "Computed daily maximum from ERA5 hourly data"
    )

    # 4. Save the resulting dataset to a new NetCDF file
    print(f"Saving output to: {output_filepath}...")
    daily_max_ds.to_netcdf(output_filepath)
    print("Done!")


if __name__ == "__main__":
    # Specify your file paths here
    input_file = "era5_hourly_2m_temperature.nc"
    output_file = "era5_daily_max_2m_temperature.nc"

    compute_daily_max_temperature(input_file, output_file)
