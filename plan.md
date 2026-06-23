1. Match up the stations in the tube lines to their lat/lon coordinates.
1.1 Make a dictionary where the keys are the naptan IDs, and the values are the stations.
1.2 In orderedLineRoutes, iterate over the naptan ids and make a new list of [station["lon"], station["lat"]], where station is the value inside the above dictionary.
1.3 Now you have a list of lon, lat coordinates to send to the client.
2. Send this data over a socket OR api call to the client.
2.1 On socket connection send over the list of lon, lat coordinates.