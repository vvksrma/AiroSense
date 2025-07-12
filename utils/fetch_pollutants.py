import ee
import os
import requests
from datetime import datetime, timezone, timedelta
import pandas as pd

# Authenticate and initialize Earth Engine
ee.Authenticate()
ee.Initialize(project='airosense')

today = datetime.now(timezone.utc).date()

START_DATE = str(today - timedelta(days=10))
END_DATE = str(today)

# Constants
MOLECULAR_WEIGHTS = {
    "no2": 46.0055,
    "co": 28.01,
    "o3": 48.00,
    "so2": 64.066,
    # Add more if needed
}

COLUMN_HEIGHT_M = 10000   # in meters (assumed vertical column height)
R = 8.314                 # Ideal gas constant (J/mol·K)
T = 298                   # Standard temperature in K (~25°C)
P = 101325                # Standard pressure in Pascals

STATES = {
    "Andaman and Nicobar Islands": (11.6724, 92.7359),  # Port Blair
    "Andhra Pradesh": (16.5062, 80.6480),               # Vijayawada
    "Arunachal Pradesh": (27.0844, 93.6053),            # Itanagar
    "Assam": (26.1433, 91.7898),                        # Guwahati
    "Bihar": (25.5941, 85.1376),                        # Patna
    "Chandigarh": (30.7333, 76.7794),                   # Chandigarh
    "Chhattisgarh": (21.2514, 81.6296),                 # Raipur
    "Dadra and Nagar Haveli and Daman and Diu": (20.3974, 72.8328), # Daman
    "Delhi": (28.6139, 77.2090),                        # New Delhi
    "Goa": (15.2993, 74.1240),                          # Panaji
    "Gujarat": (23.0225, 72.5714),                      # Ahmedabad
    "Haryana": (28.4595, 77.0266),                      # Gurugram
    "Himachal Pradesh": (31.1048, 77.1734),             # Shimla
    "Jammu and Kashmir": (34.0837, 74.7973),            # Srinagar
    "Jharkhand": (23.3441, 85.3096),                    # Ranchi
    "Karnataka": (12.9716, 77.5946),                    # Bengaluru
    "Kerala": (8.5241, 76.9366),                        # Thiruvananthapuram
    "Ladakh": (34.1526, 77.5770),                       # Leh
    "Lakshadweep": (10.5667, 72.6420),                  # Kavaratti
    "Madhya Pradesh": (23.2599, 77.4126),               # Bhopal
    "Maharashtra": (19.0760, 72.8777),                  # Mumbai
    "Manipur": (24.8170, 93.9368),                      # Imphal
    "Meghalaya": (25.5788, 91.8933),                    # Shillong
    "Mizoram": (23.7271, 92.7176),                      # Aizawl
    "Nagaland": (25.6751, 94.1086),                     # Kohima
    "Odisha": (20.2961, 85.8245),                       # Bhubaneswar
    "Puducherry": (11.9416, 79.8083),                   # Puducherry
    "Punjab": (30.7333, 76.7794),                       # Chandigarh (shared capital)
    "Rajasthan": (26.9124, 75.7873),                    # Jaipur
    "Sikkim": (27.3314, 88.6138),                       # Gangtok
    "Tamil Nadu": (13.0827, 80.2707),                   # Chennai
    "Telangana": (17.3850, 78.4867),                    # Hyderabad
    "Tripura": (23.8315, 91.2868),                      # Agartala
    "Uttar Pradesh": (26.8467, 80.9462),                # Lucknow
    "Uttarakhand": (30.3165, 78.0322),                  # Dehradun
    "West Bengal": (22.5726, 88.3639)                   # Kolkata
}

# --- AQI Breakpoints for India (CPCB) ---
BREAKPOINTS = {
    "pm2_5": [
        {"c_low": 0, "c_high": 30, "i_low": 0, "i_high": 50},
        {"c_low": 31, "c_high": 60, "i_low": 51, "i_high": 100},
        {"c_low": 61, "c_high": 90, "i_low": 101, "i_high": 200},
        {"c_low": 91, "c_high": 120, "i_low": 201, "i_high": 300},
        {"c_low": 121, "c_high": 250, "i_low": 301, "i_high": 400},
        {"c_low": 251, "c_high": 500, "i_low": 401, "i_high": 500}
    ],
    "pm10": [
        {"c_low": 0, "c_high": 50, "i_low": 0, "i_high": 50},
        {"c_low": 51, "c_high": 100, "i_low": 51, "i_high": 100},
        {"c_low": 101, "c_high": 250, "i_low": 101, "i_high": 200},
        {"c_low": 251, "c_high": 350, "i_low": 201, "i_high": 300},
        {"c_low": 351, "c_high": 430, "i_low": 301, "i_high": 400},
        {"c_low": 431, "c_high": 1000, "i_low": 401, "i_high": 500}
    ],
    "no2": [
        {"c_low": 0, "c_high": 40, "i_low": 0, "i_high": 50},
        {"c_low": 41, "c_high": 80, "i_low": 51, "i_high": 100},
        {"c_low": 81, "c_high": 180, "i_low": 101, "i_high": 200},
        {"c_low": 181, "c_high": 280, "i_low": 201, "i_high": 300},
        {"c_low": 281, "c_high": 400, "i_low": 301, "i_high": 400},
        {"c_low": 401, "c_high": 1000, "i_low": 401, "i_high": 500}
    ],
    "so2": [
        {"c_low": 0, "c_high": 40, "i_low": 0, "i_high": 50},
        {"c_low": 41, "c_high": 80, "i_low": 51, "i_high": 100},
        {"c_low": 81, "c_high": 380, "i_low": 101, "i_high": 200},
        {"c_low": 381, "c_high": 800, "i_low": 201, "i_high": 300},
        {"c_low": 801, "c_high": 1600, "i_low": 301, "i_high": 400},
        {"c_low": 1601, "c_high": 10000, "i_low": 401, "i_high": 500}
    ],
    "co": [
        {"c_low": 0, "c_high": 1, "i_low": 0, "i_high": 50},
        {"c_low": 1.1, "c_high": 2, "i_low": 51, "i_high": 100},
        {"c_low": 2.1, "c_high": 10, "i_low": 101, "i_high": 200},
        {"c_low": 10.1, "c_high": 17, "i_low": 201, "i_high": 300},
        {"c_low": 17.1, "c_high": 34, "i_low": 301, "i_high": 400},
        {"c_low": 34.1, "c_high": 50, "i_low": 401, "i_high": 500}
    ],
    "o3": [
        {"c_low": 0, "c_high": 50, "i_low": 0, "i_high": 50},
        {"c_low": 51, "c_high": 100, "i_low": 51, "i_high": 100},
        {"c_low": 101, "c_high": 168, "i_low": 101, "i_high": 200},
        {"c_low": 169, "c_high": 208, "i_low": 201, "i_high": 300},
        {"c_low": 209, "c_high": 748, "i_low": 301, "i_high": 400},
        {"c_low": 749, "c_high": 1000, "i_low": 401, "i_high": 500}
    ]
}

# shutil.rmtree('data/raw', ignore_errors=True)

# column_name.lower() used before saving
def save_to_csv(state, folder, column_name, mean_val):
    os.makedirs(f"data/raw/{folder}", exist_ok=True)
    column_name = column_name.lower()
    df = pd.DataFrame([{
        "state": state,
        "satellite_window": f"{START_DATE} to {END_DATE}",
        column_name: mean_val  # ✅ column key lowercase
    }])
    filename = state.lower().replace(" ", "_") + f"_{folder}.csv"
    df.to_csv(f"data/raw/{folder}/{filename}", index=False)
    print(f"✅ {state} {folder.upper()} data saved.")



def fetch_pollutant(dataset_id, band_name, folder_name, column_name):
    for state, (lat, lon) in STATES.items():
        try:
            print(f"📡 Fetching {column_name} for {state} at ({lat}, {lon})")
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

            if mean_val is None:
                print(f"⚠️ No satellite data for {state} ({lat}, {lon}) in {folder_name.upper()}")
                continue

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

            if "hourly" not in data or not data["hourly"]:
                print(f"❌ No hourly data found for {state}")
                continue

            hourly = data["hourly"]
            pm25_vals = hourly.get("pm2_5", [])
            pm10_vals = hourly.get("pm10", [])

            pm2_5 = pm25_vals[-1] if pm25_vals else None
            pm10 = pm10_vals[-1] if pm10_vals else None

            if pm2_5 is None and pm10 is None:
                print(f"⚠️ No PM2.5 or PM10 data available for {state}, skipping save.")
                continue

            record = {
                "state": state,
                "pm2_5": pm2_5,
                "pm10": pm10,
                "ground_timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            }

            df = pd.DataFrame([record])
            fn = state.lower().replace(" ", "_") + f"_{save_folder}.csv"
            df.to_csv(f"data/raw/{save_folder}/{fn}", index=False)
            print(f"✅ Saved for {state}: {record}")

        except Exception as e:
            print(f"❌ Error fetching ground data for {state}: {e}")

def mol_per_m2_to_ug_per_m3(mol_per_m2, pollutant):
    if pd.isna(mol_per_m2):
        return None
    M = MOLECULAR_WEIGHTS.get(pollutant)
    if M is None:
        raise ValueError(f"Molecular weight not defined for {pollutant}")
    return (mol_per_m2 * M * P * 1e6) / (R * T * COLUMN_HEIGHT_M)

def compute_aqi(cp, bps):
    if pd.isna(cp):
        return None
    cp = float(cp)
    for bp in bps:
        if bp["c_low"] <= cp <= bp["c_high"]:
            return round(
                ((bp["i_high"] - bp["i_low"]) / (bp["c_high"] - bp["c_low"])) * (cp - bp["c_low"]) + bp["i_low"]
            )
    if cp < bps[0]["c_low"]:
        return bps[0]["i_low"]
    return bps[-1]["i_high"]

def convert_to_aqi(input_folder, pollutant):
    base_output_folder = "data/raw/aqi"
    output_folder = os.path.join(base_output_folder, pollutant)
    os.makedirs(output_folder, exist_ok=True)

    expected_column = f"mean_{pollutant}"
    merged = []

    for file in os.listdir(input_folder):
        if not file.endswith(".csv"):
            continue

        filepath = os.path.join(input_folder, file)
        df = pd.read_csv(filepath)

        if expected_column not in df.columns:
            print(f"⚠️ Skipping {file} due to missing column: '{expected_column}'")
            continue

        # µg/m³
        df[f"{pollutant}_ug_per_m3"] = df[expected_column].apply(
            lambda x: mol_per_m2_to_ug_per_m3(x, pollutant)
        )

        # AQI
        df[f"{expected_column}_aqi"] = df[f"{pollutant}_ug_per_m3"].apply(
            lambda x: compute_aqi(x, BREAKPOINTS[pollutant])
        )

        # Save as: state_pollutant_aqi.csv
        state_name = file.replace(".csv", "")
        output_filename = f"{state_name}_{pollutant}_aqi.csv"
        output_path = os.path.join(output_folder, output_filename)
        df.to_csv(output_path, index=False)

        merged.append(df)

    if merged:
        print(f"✅ AQI conversion complete for {pollutant}")
        return pd.concat(merged, ignore_index=True)
    else:
        print(f"⚠️ No valid files found for {pollutant} in {input_folder}")
        return None

def compute_ground_aqi():
    ground_folder = 'data/raw/ground_monitored_data'
    updated_files = []

    for file in os.listdir(ground_folder):
        if not file.endswith('.csv'):
            continue

        path = os.path.join(ground_folder, file)
        df = pd.read_csv(path)

        # Only compute if not already present
        if 'pm2_5' in df.columns and 'pm2_5_aqi' not in df.columns:
            df['pm2_5_aqi'] = df['pm2_5'].apply(lambda x: compute_aqi(x, BREAKPOINTS['pm2_5']) if pd.notna(x) else None)
        if 'pm10' in df.columns and 'pm10_aqi' not in df.columns:
            df['pm10_aqi'] = df['pm10'].apply(lambda x: compute_aqi(x, BREAKPOINTS['pm10']) if pd.notna(x) else None)

        df.to_csv(path, index=False)
        updated_files.append(file)

    print(f"✅ Ground AQI computed for: {', '.join(updated_files)}")


def merge_all_pollutant_data():
    pollutants = ['no2', 'so2', 'co', 'o3']
    satellite_folder = 'data/raw'
    ground_folder = 'data/raw/ground_monitored_data'
    aqi_base_folder = 'data/raw/aqi'
    merged_df = None

    for pol in pollutants:
        pol_path = os.path.join(aqi_base_folder, pol)
        if not os.path.exists(pol_path):
            print(f"❌ AQI folder not found for {pol}: {pol_path}")
            continue

        files = [f for f in os.listdir(pol_path) if f.endswith(f"{pol}_aqi.csv")]
        all_states = []

        for file in files:
            df = pd.read_csv(os.path.join(pol_path, file))
            df.columns = [col.lower() for col in df.columns]

            expected_col = f"mean_{pol}"
            expected_col_aqi = f"{expected_col}_aqi"
            required_cols = {'state', 'satellite_window', expected_col, expected_col_aqi}
            if not required_cols.issubset(df.columns):
                print(f"⚠️ Skipping {file} due to missing columns: {required_cols - set(df.columns)}")
                continue

            all_states.append(df[['state', 'satellite_window', expected_col, expected_col_aqi]])

        if not all_states:
            print(f"⚠️ No valid AQI files found for {pol}")
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

        required = {'state', 'pm2_5', 'pm2_5_aqi', 'pm10', 'pm10_aqi', 'ground_timestamp'}
        if not required.issubset(df.columns):
            print(f"⚠️ Skipping {file} due to missing columns: {required - set(df.columns)}")
            continue

        ground_all.append(df[['state', 'pm2_5', 'pm2_5_aqi', 'pm10', 'pm10_aqi', 'ground_timestamp']])

    if not ground_all:
        print("❌ No ground data to merge.")
        return

    ground_df = pd.concat(ground_all, ignore_index=True)
    final_df = pd.merge(merged_df, ground_df, on='state', how='outer')
    final_df["latitude"] = final_df["state"].map(lambda s: STATES.get(s, (None, None))[0])
    final_df["longitude"] = final_df["state"].map(lambda s: STATES.get(s, (None, None))[1])

    final_cols = [
        'state', 'latitude', 'longitude',
        'pm2_5', 'pm2_5_aqi', 'pm10', 'pm10_aqi', 'ground_timestamp',
        'mean_no2', 'mean_no2_aqi',
        'mean_co', 'mean_co_aqi',
        'mean_so2', 'mean_so2_aqi',
        'mean_o3', 'mean_o3_aqi',
        'satellite_window'
    ]

    for col in final_cols:
        if col in final_df.columns and final_df[col].dtype == 'object' and col not in {'state', 'satellite_window', 'ground_timestamp'}:
            final_df[col] = pd.to_numeric(final_df[col], errors='coerce')

    final_df = final_df[[col for col in final_cols if col in final_df.columns]]

    os.makedirs('data/processed', exist_ok=True)
    final_df.to_csv('data/processed/combined_pollution_data.csv', index=False)
    print("✅ Combined dataset saved to data/processed/combined_pollution_data.csv")


if __name__ == "__main__":
    # fetch_pollutant("COPERNICUS/S5P/OFFL/L3_NO2", "NO2_column_number_density", "no2", "mean_NO2")
    # fetch_pollutant("COPERNICUS/S5P/OFFL/L3_SO2", "SO2_column_number_density", "so2", "mean_SO2")
    # fetch_pollutant("COPERNICUS/S5P/OFFL/L3_CO", "CO_column_number_density", "co", "mean_CO")
    # fetch_pollutant("COPERNICUS/S5P/OFFL/L3_O3", "O3_column_number_density", "o3", "mean_O3")

    # fetch_ground_monitored_pollutants(STATES)

    # Loop through each pollutant's folder to convert
    for pollutant in ['no2', 'so2', 'co', 'o3']:
        folder = os.path.join("data/raw", pollutant)
        convert_to_aqi(folder, pollutant)
   
    compute_ground_aqi()

    merge_all_pollutant_data()


