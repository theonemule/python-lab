import csv
import flask
import os
import sys
from collections import defaultdict
from flask import Flask
from flask import send_from_directory
from heapq import *


#This is a Python implementation of Dijkstra's algorithm that is using a heap instead of recursion. 
#Many implementations use recursion, but the scope of this app with millions of possible edges made using recursion impractical.
def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c, r))

    q, seen = [(0, f, ())], set()
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t: return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 not in seen:
                    heappush(q, (cost+c, v2, path))

    return float("inf")



#Sets the app up for running static content.
app = Flask(__name__, static_folder='static')


#This is the route for static content used by Flask
@app.route('/<path:filename>')
def send_file(filename):
    return send_from_directory(app.static_folder, filename)

#This route takes an airport code and returns information for that code as JSON
#The <code> paramter is passed in the URL so Altanta (ATL) would be /airport/ATL
@app.route("/airport/<code>")
def airport(code):

    with open('airports-big.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['LocationID'] == code:
                return flask.jsonify(row)


    return flask.jsonify(None)

#This method searches the airport list for a match for the search string.
#The <search> paramter is passed in the URL so Altanta (ATL) would be /search/ATL
@app.route("/search/<search>")
def search(search):

    results = []
    with open('airports-big.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if search.upper() in row['LocationID']:
                results.append(row)
                if len(results) == 10: #Max of 10 results
                    return flask.jsonify(results)

    return flask.jsonify(results)

#This route takes two airport codes a -- The origin and destination -- and a range and returns the route information.
#For Atlanta to New Orleans with a range of 200 miles, the url would be /route/ATL/MSY/200.
@app.route("/route/<origin>/<destination>/<int:range>")
def route(origin, destination, range):

    airportCount = 4515
    rowIdx = 0

    edges = []
    with open('airports-distance.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            rowIdx += 1
            if rowIdx % 100 == 0:
                print("Creating graph for range " + str(range) + "... " + str(round((rowIdx / airportCount) * 100, 2)) + "%" , file=sys.stderr)
            for code in row:
                if code != 'id' and float(row[code]) < range: #compares the distance between two airports. If less than the range, it adds this as a possible segment in a route in the graph.
                    edges.append((row['id'], code, float(row[code])))

    print("Calculating Route from " + origin + " to " + destination + " for range " + str(range) + " miles...", file=sys.stderr)
    rt = dijkstra(edges, origin, destination) #Calls the Dijkstra's algorithm to calculate the shortest route.


    print("Route from " + origin + " to " + destination + " for range " + str(range) + " miles."  , file=sys.stderr)

    return flask.jsonify(rt)


#This boot straps the application.
if __name__ == "__main__":
    app.run(threaded=True)
