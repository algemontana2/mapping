import json
import folium
from folium.plugins import TimestampedGeoJson

def load_residence_data(file_path):
    """Load geocoded residence data from a JSON file."""
    with open(file_path) as f:
        data = json.load(f)
    return data

def create_feature(residence):
    """Create a feature for a residence with the required properties."""
    feature = {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [residence['longitude'], residence['latitude']],
        },
        'properties': {
            'time': residence['date'],
            'style': {'color': 'red'},
            'icon': 'circle',
            'iconstyle': {
                'fillColor': 'red',
                'fillOpacity': 0.6,
                'stroke': 'false',
                'radius': 13
            },
            'popup': residence['name'],
        }
    }
    return feature

def create_map(data):
    """Create a Folium Map with timestamped geojson features."""
    m = folium.Map(location=[45.5236, -122.6750])
    features = [create_feature(residence) for residence in data]
    TimestampedGeoJson(
        {'type': 'FeatureCollection', 'features': features},
        period='P1Y',
        add_last_point=True,
    ).add_to(m)
    return m

def save_map(map_obj, outfile):
    """Save the map as an HTML file."""
    map_obj.save(outfile)

def main():
    file_path = 'geocoded_residences.json'
    data = load_residence_data(file_path)
    map_obj = create_map(data)
    save_map(map_obj, outfile='map.html')

if __name__ == '__main__':
    main()
