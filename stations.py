import requests
import sys
from dotenv import load_dotenv
import os
from flask import Flask, render_template

# Loading environment variables from .env
load_dotenv()

# Getting API keys
APP_ID = os.getenv("TFL_APP_ID")
APP_KEY = os.getenv("TFL_APP_KEY")

params = {
    "app_id": APP_ID,
    "app_key": APP_KEY
}




def get_route(line_name):
    url_line = f"https://api.tfl.gov.uk/Line/{line_name}/Route/Sequence/All"


    response = requests.get(url_line, params=params)
    data = response.json()
    
    
    ordered_lines = data["orderedLineRoutes"][0]["naptanIds"]
    stations = data["stopPointSequences"][0]["stopPoint"]
    stations_dict = {}
    for station in stations:
        stations_dict[station["stationId"]] = station
        print(station)
  



    output = []
    for station_id in ordered_lines:
        station = stations_dict.get(station_id, None)
        if station is None:
            continue

        output.append({
            "id": station["id"],
            "name": station["name"],
            "lat": station["lat"],
            "lon": station["lon"]
            
            
        })
    return output



    
    # List of stations
    stopPointsSeq = data["stopPointSequences"]

    seen = set()
    all_stations = []

    for sequence in stopPointsSeq:
        for station in sequence["stopPoint"]:
            if station["id"] not in seen:
                seen.add(station["id"])
                all_stations.append(station)

    return all_stations