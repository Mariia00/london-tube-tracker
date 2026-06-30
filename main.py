from dotenv import load_dotenv
import os
import requests
import json
import folium
import webbrowser
import sys


# Loading environment variables from .env
load_dotenv()

# Getting API keys
APP_ID = os.getenv("TFL_APP_ID")
APP_KEY = os.getenv("TFL_APP_KEY")


# URL API
# Tube stations names API
url = "https://api.tfl.gov.uk/StopPoint/Mode/tube"
# # Victoria Line route API
url_line = "https://api.tfl.gov.uk/Line/victoria/Route/Sequence/all"

# Parameters for the API request
params = {
    "app_id": APP_ID,
    "app_key": APP_KEY
}

# Making the request
response = requests.get(url_line, params=params)


# first_station = data["centrePoint"]
#print(json.dumps(data, indent=4))
#sys.exit()




def get_inbound_stations(line_name):
    url_line = f"https://api.tfl.gov.uk/Line/{line_name}/Route"
    response = requests.get(url_line, params=params)
    data = response.json()
    print(data.keys())
    # print(data["lineStrings"])
    #sys.exit()


    
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






    # inbound = stopPointsSeq[0]
    # inbound_stations = inbound["stopPoint"]
    # return inbound_stations


# def draw_line(map, tooltip, color, stations):
#     line_locations = []
#     for station in stations:
#         lines = []
#         for line in station["lines"]:
#          lines.append(line["name"])
#         folium.Marker(
#             location = [station['lat'], station["lon"]],
#             popup = f"{station['name']} ({station['id']}) ({', '.join(lines)})"
#         ).add_to(map)
#         line_locations.append([station['lat'], station['lon']])

#     folium.PolyLine(line_locations, tooltip=tooltip, color=color, weight=5, opacity=1).add_to(map)


def draw_line(map, tooltip, color, line_name):
    url_line = f"https://api.tfl.gov.uk/Line/{line_name}/Route/Sequence/inbound"
    response = requests.get(url_line, params=params)
    data = response.json()

    seen_markers = {}

    for sequence in data["stopPointSequences"]:
        line_locations = []
        for station in sequence["stopPoint"]:
            if not station.get("lat") or not station.get("lon"):
                continue
            # Add marker only once per station
            # if station["id"] not in seen_markers:
            # seen_markers.add(station["id"])
            if station["id"] not in seen_markers:
                seen_markers[station["id"]] = 0
            seen_markers[station["id"]] += 1
            if seen_markers[station["id"]] > 2:
                print(f"Station {station['name']} ({station['id']}) appears in {seen_markers[station['id']]} sequences")
                continue
            lines = [line["name"] for line in station.get("lines", [])]
            folium.Marker(
                    location=[station['lat'], station["lon"]],
                    popup=f"{station['name']} ({station['id']}) ({', '.join(lines)})"
                ).add_to(map)
            line_locations.append([station['lat'], station['lon']])
                



def draw_line_new(map, tooltip, color, line_name):
    # Ensure line_name is lowercase as per TfL convention (e.g., 'elizabeth')
    line_id = line_name.lower()
    url_line = f"https://api.tfl.gov.uk/Line/{line_id}/Route/Sequence/inbound"
    
    # Ensure you pass your params (include API keys if you have them)
    response = requests.get(url_line, params=params)
    data = response.json()

    seen_markers = {}

    for sequence in data["stopPointSequences"]:
        line_locations = []
        for station in sequence["stopPoint"]:
            if not station.get("lat") or not station.get("lon"):
                continue

            # Extract line IDs for this specific stop point
            station_line_ids = [l["id"] for l in station.get("lines", [])]
            
            # Only proceed if the station explicitly belongs to the line we are drawing
            if line_id not in station_line_ids:
                continue

            if station["id"] not in seen_markers:
                seen_markers[station["id"]] = 0
            
            seen_markers[station["id"]] += 1
            
            if seen_markers[station["id"]] > 3:
                continue

            # --- FIX: Only display lines relevant to your current map context ---
            # Instead of grabbing every line on a National Rail hub, we filter down.
            # You can either show ONLY the line you are drawing, or keep it clean.
            lines_display = [l["name"] for l in station.get("lines", []) if l["id"] == line_id]
            
            # Alternatively, if you want to show interchanges but skip non-TfL junk:
            # tfl_modes = ['elizabeth', 'central', 'circle', 'hammersmith-city', 'metropolitan']
            # lines_display = [l["name"] for l in station.get("lines", []) if l["id"] in tfl_modes]

            folium.Marker(
                location=[station['lat'], station["lon"]],
                popup=f"{station['name']} ({station['id']})<br>Line: {', '.join(lines_display)}",
                tooltip=tooltip
            ).add_to(map)
            
            line_locations.append([station['lat'], station['lon']])
        
        # --- FIX: Removed the duplicate PolyLine block ---
        # Skip empty or single-point sequences
        if len(line_locations) < 2:
            continue

        # Draw each branch as its own segment exactly once
        folium.PolyLine(
            line_locations,
            tooltip=tooltip,
            color=color,
            weight=5,
            opacity=1
        ).add_to(map)


# Creating a map centered on London
tube_map = folium.Map(location=[51.5074, -0.1278], zoom_start=12)



# bakerloo_stations = get_inbound_stations("bakerloo")
#draw_line_new(tube_map, "Bakerloo Line inbound", "brown", "bakerloo")

# central_stations = get_inbound_stations("central")
# draw_line(tube_map, tooltip="Central Line inbound", color="red", line_name="elizabeth")
#draw_line_new(tube_map, tooltip="Elizabeth Line inbound", color="purple", line_name="elizabeth")

# circle_stations = get_inbound_stations("circle")
#draw_line_new(tube_map, tooltip="Circle Line inbound", color="yellow", line_name="circle")

# # district_stations = get_inbound_stations("district")
#draw_line_new(tube_map, tooltip="District Line inbound", color="green", line_name="district")

# # hammersmith_city_stations = get_inbound_stations("hammersmith-city")
# draw_line_new(tube_map, tooltip="Hammersmith & City Line inbound", color="pink", line_name="hammersmith-city")

# # # jubilee_stations = get_inbound_stations("jubilee")
# draw_line_new(tube_map, tooltip="Jubilee Line inbound", color="gray", line_name="jubilee")

# # # metropolitan_stations = get_inbound_stations("metropolitan")
# draw_line_new(tube_map, tooltip="Metropolitan Line inbound", color="magenta", line_name="metropolitan")

# # # northern_stations = get_inbound_stations("northern")
# draw_line_new(tube_map, tooltip="Northern Line inbound", color="black", line_name="northern")

# # # picadilly_stations = get_inbound_stations("piccadilly")
# draw_line_new(tube_map, tooltip="Piccadilly Line inbound", color="darkblue", line_name="piccadilly")

# # # victoria_stations = get_inbound_stations("victoria")
draw_line_new(tube_map, tooltip="Victoria Line inbound", color="blue", line_name="victoria")

# # # waterloo_city_stations = get_inbound_stations("waterloo-city")
# draw_line_new(tube_map, tooltip="Waterloo & City Line inbound", color="turquoise", line_name="waterloo-city")

# # # elizabeth_line_stations = get_inbound_stations("elizabeth")
# draw_line_new(tube_map, tooltip="Elizabeth Line inbound", color="purple", line_name="elizabeth")


tube_map.save("london_tube_map.html")
webbrowser.open("london_tube_map.html")
sys.exit()

# line_locations = []

# inbound_stations = get_inbound_stations("victoria")


# for station in inbound_stations:
#     lines = []
#     for line in station["lines"]:
#         lines.append(line["name"])
#     #print(f"{station['name']} ({station['id']}) ({station['lat']}, {station['lon']}) - Lines: {', '.join(lines)}")
#     folium.Marker(
#         location = [station['lat'], station["lon"]],
#         popup = f"{station['name']} ({station['id']}) ({', '.join(lines)})"
#     ).add_to(tube_map)
#     line_locations.append([station['lat'], station['lon']])

# folium.PolyLine(line_locations, tooltip="Victoria Line inbound", color="blue", weight=2.5, opacity=1).add_to(tube_map)
tube_map.save("victoria_line.html")
webbrowser.open("victoria_line.html")
sys.exit()




# {
#                     "$type": "Tfl.Api.Presentation.Entities.MatchedStop, Tfl.Api.Presentation.Entities",
#                     "parentId": "HUBWHC",
#                     "stationId": "940GZZLUWWL",
#                     "icsId": "1000249",
#                     "topMostParentId": "HUBWHC",
#                     "modes": [
#                         "tube"
#                     ],
#                     "stopType": "NaptanMetroStation",
#                     "zone": "3",
#                     "lines": [
#                         {
#                             "$type": "Tfl.Api.Presentation.Entities.Identifier, Tfl.Api.Presentation.Entities",
#                             "id": "victoria",
#                             "name": "Victoria",
#                             "uri": "/Line/victoria",
#                             "type": "Line",
#                             "crowding": {
#                                 "$type": "Tfl.Api.Presentation.Entities.Crowding, Tfl.Api.Presentation.Entities"
#                             },
#                             "routeType": "Unknown",
#                             "status": "Unknown"
#                         }
#                     ],
#                     "status": true,
#                     "id": "940GZZLUWWL",
#                     "name": "Walthamstow Central Underground Station",
#                     "lat": 51.582965,
#                     "lon": -0.019885
#                 }





seen = set()
unique_stations = []

for station in stopPoints:
    station_id = station.get("stationNaptan") or station["id"]
    station_modes = station.get("modes", [])
    
    if len(station_modes) != 1:
        continue

    if not station.get("lat") or not station.get("lon"):
        continue

    if station_id in seen:
        continue

    seen.add(station_id)
    unique_stations.append(station)

# Displaying station names
for station in unique_stations:
    if station['id'] == "9400ZZLUWLO":
        print(json.dumps(station, indent=4))
        #sys.exit()
    
    # Add marker to the map for each station
    folium.Marker(
        location = [station['lat'], station["lon"]],
        popup = f"{station['name']} ({station['id']}) ({station['modes']})"
    ).add_to(tube_map)

 



# Saving the map to an HTML file
tube_map.save("tube_map_1.html")

print("Map created!")

webbrowser.open("tube_map_1.html")

