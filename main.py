import requests
import pandas as pd
import os
import json
import geopandas as gpd

# Import the location csv file. See the Readme for CSV format instructions and suggestions
csv = input("Enter the path to your location csv file: ")
tod_centroids = pd.read_csv(csv)

# Set the desired output directory
output_directory = input("Enter your desired output directory: ")

total = len(tod_centroids)  # total number of locations to generate isochrones
latitude = tod_centroids["YCoord"]
longitude = tod_centroids["XCoord"]

# Initialize a list to store locations
locations = [f"{lat},{lon}" for lat, lon in zip(latitude, longitude)]

# Set the time range from 8:00 am to 8:30 am. Adjust these variables depending on your preferences
start_time = pd.to_datetime("2024-09-12T08:00:00-05:00")
end_time = pd.to_datetime("2024-09-12T08:30:00-05:00")

# Make separate HTTP GET requests for each minute in the timeframe for each location
for i in range(total):
    combined_geojson = {"type": "FeatureCollection", "features": []}  # Initialize the geojson file

    for current_time in pd.date_range(start=start_time, end=end_time, freq="min"):
        current_time_str = current_time.strftime("%Y-%m-%dT%H:%M:%S%z")

        # Manually insert the colon in the time zone offset - for some reason this needs to be done, could probably
        # troubleshoot to improve
        current_time_str = current_time_str[:-2] + ':' + current_time_str[-2:]
        # print(current_time_str) - Debugging line
        # Make API request
        transit_stations = requests.get(
            "http://localhost:8080/otp/traveltime/isochrone/?batch=true",
            params={
                "location": locations[i],
                "arriveBy": "false",
                "mode": "WALK, TRANSIT",
                "time": current_time_str,
                "cutoff": "30M",
            }, )

        # Extract the GeoJSON features from the response
        geojson_features = json.loads(transit_stations.text)["features"]
        combined_geojson["features"].extend(geojson_features)

    # Convert GeoJSON to GeoDataFrame
    gdf = gpd.GeoDataFrame.from_features(combined_geojson, crs="EPSG:4326")

    # Add a small buffer to resolve any topographical issues, then dissolve the GeoDataFrame to combine geometries
    gdf['geometry'] = gdf['geometry'].buffer(0, cap_style='round', join_style='round')
    dissolved_gdf = gdf.dissolve()

    # Extract the stop ID from the current row, if generating isochrones for a rail or bus station
    current_id = tod_centroids.loc[i, "stop_name"]

    # Sanitize the filename to remove invalid characters
    sanitized_id = "".join(char if char.isalnum() or char in "._-" else "_" for char in current_id)

    # Save the dissolved GeoDataFrame to a file with stop_name in the filename
    filename = os.path.join(
        output_directory,
        f"output_iteration_{i}_stop_{sanitized_id}_combined.geojson",
    )
    dissolved_gdf.to_file(filename, driver="GeoJSON")

    print(f"Iteration {i}, Stop {current_id}: Combined GeoJSON saved to {filename}")
