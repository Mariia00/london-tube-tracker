from dotenv import load_dotenv
import os
import requests
import json
import folium
import webbrowser
import sys




# # Victoria Line route API
url_mode = "https://api.tfl.gov.uk/Line/victoria/Arrivals"


# Making the request
response = requests.get(url_mode)

data = response.json()

for prediction in data:
        print(prediction["vehicleId"])
        print(prediction["naptanId"])
        print(prediction["currentLocation"])
        print(prediction["towards"])
        
        
        print("-----------------------------")
        




# "$type": "Tfl.Api.Presentation.Entities.Prediction, Tfl.Api.Presentation.Entities",
#     "id": "-1721974608",
#     "operationType": 1,
#     "vehicleId": "706",
#     "naptanId": "940GZZLUMED",
#     "stationName": "Mile End Underground Station",
#     "lineId": "district",
#     "lineName": "District",
#     "platformName": "Westbound - Platform 2",
#     "bearing": "",
#     "destinationNaptanId": "940GZZLUKOY",
#     "destinationName": "Kensington (Olympia) Underground Station",
#     "timestamp": "2026-06-02T19:02:19.5558778Z",
#     "timeToStation": 28,
#     "currentLocation": "Left Bow Road",
#     "towards": "Olympia",
#     "expectedArrival": "2026-06-02T19:02:47Z",
#     "timeToLive": "2026-06-02T19:02:47Z",
#     "modeName": "tube",
#     "timing": {
#         "$type": "Tfl.Api.Presentation.Entities.PredictionTiming, Tfl.Api.Presentation.Entities",
#         "countdownServerAdjustment": "00:00:00",
#         "source": "0001-01-01T00:00:00",
#         "insert": "0001-01-01T00:00:00",
#         "read": "2026-06-02T19:01:55.917Z",
#         "sent": "2026-06-02T19:02:19Z",
#         "received": "0001-01-01T00:00:00"
#     }
# }, {
#     "$type": "Tfl.Api.Presentation.Entities.Prediction, Tfl.Api.Presentation.Entities",
#     "id": "1617205728",
#     "operationType": 1,
#     "vehicleId": "715",
#     "naptanId": "940GZZLUTWH",
#     "stationName": "Tower Hill Underground Station",
#     "lineId": "district",
#     "lineName": "District",
#     "platformName": "Eastbound - Platform 3",
#     "direction": "outbound",
#     "bearing": "",
#     "destinationNaptanId": "940GZZLUUPM",
#     "destinationName": "Upminster Underground Station",
#     "timestamp": "2026-06-02T19:02:19.5558778Z",
#     "timeToStation": 28,
#     "currentLocation": "Between Monument and Tower Hill",
#     "towards": "Upminster",
#     "expectedArrival": "2026-06-02T19:02:47Z",
#     "timeToLive": "2026-06-02T19:02:47Z",
#     "modeName": "tube",
#     "timing": {
#         "$type": "Tfl.Api.Presentation.Entities.PredictionTiming, Tfl.Api.Presentation.Entities",
#         "countdownServerAdjustment": "00:00:00",
#         "source": "0001-01-01T00:00:00",
#         "insert": "0001-01-01T00:00:00",
#         "read": "2026-06-02T19:01:57.911Z",
#         "sent": "2026-06-02T19:02:19Z",
#         "received": "0001-01-01T00:00:00"
#     }
# }, 