import requests
from math;
import ceil;

from openaq import OpenAQ

client = OpenAQ(api_key = '450640de2e43e7d2161926832f1f122e5c59ed1974f37e1c3aeb063414bf042f')

locations = client.locations.list()
meta = locations.meta
found = meta.found

limit = 1000

pages = ceil(found/limit)

for page in pages:
    locations.client.list(limit=limit, page=page)

client.close()


# import requests
# import pandas as pd
# import os

# API_KEY = "450640de2e43e7d2161926832f1f122e5c59ed1974f37e1c3aeb063414bf042f"
# LOCATION = "Delhi Technological University"  # Check this using /locations API

# url = "https://api.openaq.org/v3/measurements"
# headers = {
#     "Accept": "application/json",
#     "X-API-Key": API_KEY
# }
# params = {
#     "location": LOCATION,
#     "parameter": "pm25",
#     "limit": 100,
#     "page": 1,
#     "sort": "desc",
#     "order_by": "datetime"
# }

# response = requests.get(url, headers=headers, params=params)
# # res = requests.get("https://api.openaq.org/v3/locations?country=IN&limit=100", headers=headers)


# # if res.status_code == 200:
# #     data = res.json()["results"]
# #     for loc in data:
# #         print(f"{loc['id']} - {loc['name']}")
# # else:
# #     print("❌ Error:", res.status_code, res.text)
# if response.status_code == 200:
#     results = response.json()["results"]
#     df = pd.DataFrame(results)
#     os.makedirs("data/raw", exist_ok=True)
#     df.to_csv("data/raw/delhi_ground_pm25.csv", index=False)
#     print("✅ PM2.5 data saved to data/raw/delhi_ground_pm25.csv")
# else:
#     print("❌ Error:", response.status_code, response.text)
