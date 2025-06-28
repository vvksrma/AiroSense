import ee
import pandas as pd

ee.Authenticate()
ee.Initialize(project='airosense')

# Define Delhi coordinates
delhi = ee.Geometry.Point(77.2090, 28.6139)

# Sentinel-5P NO2 data
collection = ee.ImageCollection('COPERNICUS/S5P/OFFL/L3_NO2') \
    .select('NO2_column_number_density') \
    .filterDate('2024-06-01', '2024-06-10') \
    .filterBounds(delhi)

# Convert collection to list
data = collection.aggregate_array('NO2_column_number_density').getInfo()

# Or export the mean value
mean_val = collection.mean().reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=delhi.buffer(10000),
    scale=1000
).get('NO2_column_number_density').getInfo()

# Save as CSV
df = pd.DataFrame([{
    'city': 'Delhi',
    'date_range': '2024-06-01 to 2024-06-10',
    'mean_NO2': mean_val
}])

df.to_csv('data\\raw\\delhi_satellite_no2.csv', index=False)

print("Delhi NO2 satellite data saved to data/raw/delhi_satellite_no2.csv ✅")
