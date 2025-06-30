import ee
import os
import requests
from datetime import datetime, timezone
import pandas as pd

# Authenticate and initialize Earth Engine
ee.Authenticate()
ee.Initialize(project='airosense')

START_DATE = "2025-06-01"
END_DATE = "2025-06-10"

STATES = {
    "Andaman and Nicobar Islands": (11.7401, 92.6586),
    "Andhra Pradesh": (15.9129, 79.74),
    "Arunachal Pradesh": (28.218, 94.7278),
    "Assam": (31.1048, 77.1734),
    "Bihar": (25.0961, 85.3131),
    "Chhattisgarh": (21.2787, 81.8661),
    "Dadra and Nagar Haveli and Daman and Diu": (20.1809, 73.0169),
    "Delhi": (28.7041, 77.1025),
    "Goa": (15.2993, 74.124),
    "Gujarat": (22.2587, 71.1924),
    "Haryana": (29.0588, 76.0856),
    "Himachal Pradesh": (31.1048, 77.1734),
    "Jharkhand": (23.6102, 85.2799),
    "Karnataka": (15.3173, 75.7139),
    "Kerala": (10.8505, 76.2711),
    "Lakshadweep": (10.0, 73.0),
    "Madhya Pradesh": (22.9734, 78.6569),
    "Maharashtra": (19.7515, 75.7139),
    "Manipur": (24.6637, 93.9063),
    "Meghalaya": (25.467, 91.3662),
    "Mizoram": (23.1645, 92.9376),
    "Nagaland": (26.1584, 94.5624),
    "Odisha": (20.9517, 85.0985),
    "Puducherry": (11.9416, 79.8083),
    "Punjab": (31.1471, 75.3412),
    "Rajasthan": (27.0238, 74.2179),
    "Sikkim": (27.533, 88.5122),
    "Tamil Nadu": (11.1271, 78.6569),
    "Telangana": (18.1124, 79.0193),
    "Tripura": (23.9408, 91.9882),
    "Chandigarh": (30.7333, 76.7794),
    "Jammu and Kashmir": (33.7782, 76.5762),
    "Ladakh": (34.2996, 78.2932),
    "Uttar Pradesh": (26.8467, 80.9462),
    "Uttarakhand": (30.0668, 79.0193),
    "West Bengal": (22.9868, 87.855)
}

# column_name.lower() used before saving
def save_to_csv(state, folder, column_name, mean_val):
    os.makedirs(f"data/raw/{folder}", exist_ok=True)
    column_name = column_name.lower()  # ✅ lowercase fix
    df = pd.DataFrame([{
        "state": state,
        "satellite_window": f"{START_DATE} to {END_DATE}",
        column_name: mean_val
    }])
    filename = state.lower().replace(" ", "_") + f"_{folder}.csv"
    df.to_csv(f"data/raw/{folder}/{filename}", index=False)
    print(f"✅ {state} {folder.upper()} data saved.")


def fetch_pollutant(dataset_id, band_name, folder_name, column_name):
    for state, (lat, lon) in STATES.items():
        try:
            point = ee.Geometry.Point(lon, lat)
            collection = ee.ImageCollection(dataset_id) \
                .select(band_name) \
                .filterDate(START_DATE, END_DATE) \
                .filterBounds(point)

            mean_val = collection.mean().reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=point.buffer(10000),
                scale=1000
            ).get(band_name).getInfo()

            save_to_csv(state, folder_name, column_name, mean_val)

        except Exception as e:
            print(f"❌ Error for {state} - {folder_name}: {e}")


def fetch_ground_monitored_pollutants(state_city_map, save_folder="ground_monitored_data"):
    os.makedirs(f"data/raw/{save_folder}", exist_ok=True)
    for state, (lat, lon) in state_city_map.items():
        url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": ["pm2_5", "pm10"]
        }
        try:
            res = requests.get(url, params=params, timeout=10)
            res.raise_for_status()
            data = res.json()

            if "hourly" not in data:
                print(f"No hourly data for {state} → {data}")
                continue

            hourly = data["hourly"]
            record = {"state": state}
            for param in ["pm2_5", "pm10"]:
                arr = hourly.get(param, [])
                record[param] = arr[-1] if arr else None
            record["ground_timestamp"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

            df = pd.DataFrame([record])
            fn = state.lower().replace(" ", "_") + f"_{save_folder}.csv"
            df.to_csv(f"data/raw/{save_folder}/{fn}", index=False)
            print(f"✅ Saved for {state}: {record}")
        except Exception as e:
            print(f"❌ Error fetching ground data for {state}: {e}")


def merge_all_pollutant_data():
    pollutants = ['no2', 'so2', 'co', 'o3']
    satellite_folder = 'data/raw'
    ground_folder = 'data/raw/ground_monitored_data'
    merged_df = None

    for pol in pollutants:
        pol_path = os.path.join(satellite_folder, pol)
        if not os.path.exists(pol_path):
            print(f"❌ Folder not found: {pol_path}")
            continue

        files = os.listdir(pol_path)
        all_states = []

        for file in files:
            df = pd.read_csv(os.path.join(pol_path, file))
            df.columns = [col.lower() for col in df.columns]

            expected_col = f"mean_{pol}"
            required_cols = {'state', 'satellite_window', expected_col}
            if not required_cols.issubset(df.columns):
                print(f"⚠️ Skipping {file} due to missing columns: {required_cols - set(df.columns)}")
                continue

            all_states.append(df[['state', 'satellite_window', expected_col]])

        if not all_states:
            print(f"⚠️ No valid files found for {pol}")
            continue

        pol_df = pd.concat(all_states, ignore_index=True)

        if merged_df is None:
            merged_df = pol_df
        else:
            merged_df = pd.merge(merged_df, pol_df, on=['state', 'satellite_window'], how='outer')

    if merged_df is None:
        print("❌ No satellite data found to merge.")
        return

    ground_files = os.listdir(ground_folder)
    ground_all = []

    for file in ground_files:
        df = pd.read_csv(os.path.join(ground_folder, file))
        df.columns = [col.lower() for col in df.columns]

        required = {'state', 'pm2_5', 'pm10', 'ground_timestamp'}
        if not required.issubset(df.columns):
            print(f"⚠️ Skipping {file} due to missing columns: {required - set(df.columns)}")
            continue

        ground_all.append(df[['state', 'pm2_5', 'pm10', 'ground_timestamp']])

    if not ground_all:
        print("❌ No ground data to merge.")
        return

    ground_df = pd.concat(ground_all, ignore_index=True)
    final_df = pd.merge(merged_df, ground_df, on='state', how='outer')

    final_cols = [
        'state', 'pm2_5', 'pm10', 'ground_timestamp',
        'mean_no2', 'mean_co', 'mean_so2', 'mean_o3', 'satellite_window'
    ]
    for col in final_cols:
        if col not in final_df.columns:
            final_df[col] = None

    final_df = final_df[final_cols]

    os.makedirs('data/processed', exist_ok=True)
    final_df.to_csv('data/processed/combined_pollution_data.csv', index=False)
    print("✅ Combined dataset saved to data/processed/combined_pollution_data.csv")


if __name__ == "__main__":
    fetch_pollutant("COPERNICUS/S5P/OFFL/L3_NO2", "NO2_column_number_density", "no2", "mean_NO2")
    fetch_pollutant("COPERNICUS/S5P/OFFL/L3_SO2", "SO2_column_number_density", "so2", "mean_SO2")
    fetch_pollutant("COPERNICUS/S5P/OFFL/L3_CO", "CO_column_number_density", "co", "mean_CO")
    fetch_pollutant("COPERNICUS/S5P/OFFL/L3_O3", "O3_column_number_density", "o3", "mean_O3")
    fetch_ground_monitored_pollutants(STATES)
    merge_all_pollutant_data()
