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


def get_stations_for_lines(line_name):
    params = {
    "app_id": APP_ID,
    "app_key": APP_KEY
    }

    url_line = f"https://api.tfl.gov.uk/Line/{line_name}/StopPoints"
    response = requests.get(url_line, params=params)
    data = response.json()

    return data

    output = []
    for station in data:
        output.append({
            "id": station["id"],
            "name": station["commonName"],
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