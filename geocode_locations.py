import json
import googlemaps
from collections import defaultdict

# Your Google API key
API_KEY = 'AIzaSyA1FrSysTzt3UAvQzrzUGOXt5MlhyKKdoY'

# Create a client
gmaps = googlemaps.Client(key=API_KEY)

# Load the individuals data
with open('individuals.json', 'r') as f:
    individuals = json.load(f)

# Output data
output_data = []

# Track the unique locations
unique_locations = defaultdict(dict)

# Function to geocode a place
def geocode_place(place):
    # Check if the location is already processed
    if place in unique_locations:
        return unique_locations[place]

    # Check if the place is not empty or None
    if not place:
        print("Skipping empty or None place.")
        return None

    print(f"Geocoding: {place}")

    try:
        # Geocode the place
        geocode_result = gmaps.geocode(place)
    except Exception as e:
        print(f"Error geocoding {place}: {e}")
        return None

    # If there is a result
    if geocode_result:
        # Get the location
        location = geocode_result[0]['geometry']['location']

        # Store the location in unique locations
        unique_locations[place] = location

        return location

    return None

# Function to geocode events for an individual
def geocode_events(individual):
    for event in ['birth', 'death']:
        if event in individual and 'place' in individual[event]:
            location = geocode_place(individual[event]['place'])
            if location:
                individual[event]['latitude'] = location['lat']
                individual[event]['longitude'] = location['lng']

    for residence in individual['residences']:
        place = residence['place']
        location = geocode_place(place)
        if location:
            residence['latitude'] = location['lat']
            residence['longitude'] = location['lng']

    return individual

# Go through all individuals
for individual in individuals:
    individual = geocode_events(individual)
    output_data.append(individual)

# Write the output data to a JSON file
with open('geocoded_individuals.json', 'w') as f:
    json.dump(output_data, f, indent=4)

print("Geocoding completed.")
