import ee
import os
import pandas as pd

# Global Assest
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

# Save to CSV
def save_to_csv(state, folder, column_name, mean_val):
    os.makedirs(f"data/raw/{folder}", exist_ok=True)
    df = pd.DataFrame([{
        "state": state,
        "date_range": f"{START_DATE} to {END_DATE}",
        column_name: mean_val
    }])
    filename = state.lower().replace(" ", "_") + f"_{folder}.csv"
    df.to_csv(f"data/raw/{folder}/{filename}", index=False)
    print(f"✅ {state} {folder.upper()} data saved.")

# Fetch NO₂ from Sentinel-5P
def fetch_no2():
    for state, (lat, lon) in STATES.items():
        try:
            point = ee.Geometry.Point(lon, lat)
            collection = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2") \
                .select("NO2_column_number_density") \
                .filterDate(START_DATE, END_DATE) \
                .filterBounds(point)

            mean_val = collection.mean().reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=point.buffer(10000),
                scale=1000
            ).get("NO2_column_number_density").getInfo()

            save_to_csv(state, folder="no2", column_name="mean_NO2", mean_val=mean_val)

        except Exception as e:
            print(f"❌ Error for {state}: {e}")

# Fetch O3 from Sentinel-5P
def fetch_o3():
    for state, (lat, lon) in STATES.items():
        try:
            point = ee.Geometry.Point(lon, lat)
            collection = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_O3") \
                .select("O3_column_number_density") \
                .filterDate(START_DATE, END_DATE) \
                .filterBounds(point)

            mean_val = collection.mean().reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=point.buffer(10000),
                scale=1000
            ).get("O3_column_number_density").getInfo()

            save_to_csv(state, folder="o3", column_name="mean_O3", mean_val=mean_val)

        except Exception as e:
            print(f"❌ Error for {state}: {e}")


# Fetch so2 from Sentinel-5P
def fetch_so2():
    for state, (lat, lon) in STATES.items():
        try:
            point = ee.Geometry.Point(lon, lat)
            collection = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_SO2") \
                .select("SO2_column_number_density") \
                .filterDate(START_DATE, END_DATE) \
                .filterBounds(point)

            mean_val = collection.mean().reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=point.buffer(10000),
                scale=1000
            ).get("SO2_column_number_density").getInfo()

            save_to_csv(state, folder="so2", column_name="mean_so2", mean_val=mean_val)

        except Exception as e:
            print(f"❌ Error for {state}: {e}")


# Fetch CO from Sentinel-5P
def fetch_co():
    for state, (lat, lon) in STATES.items():
        try:
            point = ee.Geometry.Point(lon, lat)
            collection = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_CO") \
                .select("CO_column_number_density") \
                .filterDate(START_DATE, END_DATE) \
                .filterBounds(point)

            mean_val = collection.mean().reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=point.buffer(10000),
                scale=1000
            ).get("CO_column_number_density").getInfo()

            save_to_csv(state, folder="co", column_name="mean_co", mean_val=mean_val)

        except Exception as e:
            print(f"❌ Error for {state}: {e}")

def merge_all_pollutant_data():
    pollutants = ['no2', 'so2', 'co', 'o3']
    folder = 'data/raw'
    merged_df = None

    for pol in pollutants:
        path = os.path.join(folder, pol)
        files = os.listdir(path)
        all_states = []

        for file in files:
            df = pd.read_csv(os.path.join(path, file))
            all_states.append(df)

        pol_df = pd.concat(all_states)
        # Prevent duplicate column names
        val_col = [col for col in pol_df.columns if col.startswith('mean_')][0]

        if merged_df is None:
            merged_df = pol_df
        else:
            merged_df = pd.merge(merged_df, pol_df, on=["state", "date_range"], how="outer")

    os.makedirs('data/processed', exist_ok=True)
    merged_df.to_csv('data/processed/combined_pollution_data.csv', index=False)
    print("✅ Combined dataset saved.")


if __name__ == "__main__":
    fetch_so2()
    fetch_co()
    fetch_no2()
    fetch_o3()
    merge_all_pollutant_data()