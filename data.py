
import csv
from math import sin, cos, sqrt, atan2, radians

LatLongDict = {}
#radius of earth in miles
R = 3959.0

# Reads the airport data in to a list for easy access.
with open('airports-big.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        LatLongDict[row['LocationID']] = [row['Latitude'], row['Longitude']]

fieldnames = []
fieldnames.append('id')
for code1 in LatLongDict:
    fieldnames.append(code1)

with open('airports-distance.csv', 'w') as csvfile:

    writer = csv.DictWriter(csvfile,  delimiter=',', lineterminator='\n', fieldnames=fieldnames)

    # Writes the column headers.
    writer.writeheader()
    
    rowIdx = 0

    for code1 in LatLongDict:

        #Selects the airport row and sets the latitude and longitude for the airport of origin.
        lat1 = radians(float(LatLongDict[code1][0]))
        lon1 = radians(float(LatLongDict[code1][1]))
        row = {}
        row['id'] = code1

        if rowIdx % 100 == 0:
            print("Processing " + str(rowIdx) + " of " + str(len(LatLongDict)) + " airports.")

        rowIdx += 1

        #Selects the destination airport, then calculates the distance between it and the origin using the distance over sphere based on the latitude and longitude.
        for code2 in LatLongDict:

            lat2 = radians(float(LatLongDict[code2][0]))
            lon2 = radians(float(LatLongDict[code2][1]))
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = R * c

            row[code2] = round(distance, 2)

        #writes the row to a file.
        writer.writerow(row)
