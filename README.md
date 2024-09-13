# Open Trip Planner Isochrones
 Python code to pull transit isochrones for a set of locations.

 # Background and Getting Started
 This script is designed to use an Open Trip Planner 2 instance of whatever location (OpenStreetMap) and transit system (GTFS) you wish, and use the Travel Time API to generate isochrones for a set of locations. It requires a running Open Trip Planner 2 on your local machine. To set up Open Trip Planner 2, review the documentation and follow the provided tutorial: https://docs.opentripplanner.org/en/latest/Basic-Tutorial/

# Configuring the script
The script requires a CSV file of locations to run. The required fields are a set of latitude and longitude coordinates (YCoord and X Coord), and a location id (stop_name). This script is set up to assume the origin location is a rail or bus station, but you can modify this to suit your needs. Just be sure to update the code accordingly. 

This script defaults to generating isochrones for each minute between 8:00 am and 8:30 am for a set date, and average the geometries to account for human behavior (people might not leave for their bus/train at the same time, every day). It also runs on a weekday. Be sure to adjust these for your purposes (lines 22 and 23 in the code).

# Running the script
Assuming your OTP2 instance is running and you have a list of locations, running the script only requires an input of two directories:

1. The path to your locations.csv
2. Your desired output path to save the geojson files

Once you input these paths, the script should handle the rest.

# What do you do with geojson files?
Some GIS programs can read these directly. ArcGIS Pro can import jsons/geojsons directly and convert them into shapefiles or feature layers. Refer to the documentation of your GIS software. 
