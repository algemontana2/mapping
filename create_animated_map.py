import folium
from folium.plugins import MarkerCluster
import pandas as pd
import json
import numpy as np

# Load the json data into a pandas DataFrame
with open('geocoded_individuals.json') as f:
    data = json.load(f)

# Flatten the data into a list of dictionaries
flattened_data = []
for d in data:
    name = d['name']
    for r in d['residences']:
        flattened_data.append({
            'name': name,
            'date': r.get('dates'),
            'place': r['place'],
            'latitude': r.get('latitude'),
            'longitude': r.get('longitude'),
        })

# Convert the flattened data to a DataFrame
df = pd.DataFrame(flattened_data)

# Convert dates to integers
def convert_date(date):
    if isinstance(date, str) and date.isdigit():
        return int(date)
    if isinstance(date, list):
        return [int(d) for d in date if str(d).isdigit()]
    return date

df['date'] = df['date'].apply(convert_date)

# Exclude rows with NaN latitude or longitude
df = df.dropna(subset=['latitude', 'longitude'])

# Calculate the mean latitude and longitude
latitude_mean = df['latitude'].mean()
longitude_mean = df['longitude'].mean()

# Create the map if mean latitude and longitude are valid
if not np.isnan(latitude_mean) and not np.isnan(longitude_mean):
    m = folium.Map(location=[latitude_mean, longitude_mean], zoom_start=2)
else:
    print("Error: Unable to calculate the mean latitude and longitude.")

# Create a marker cluster
marker_cluster = MarkerCluster().add_to(m)

# Add a marker for each residence
for idx, row in df.iterrows():
    if not pd.isna(row['latitude']) and not pd.isna(row['longitude']):
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            icon=None,
            popup=f"{row['name']}, {row['date']}",
        ).add_to(marker_cluster)

# Save the map to a file
m.save('map.html')
