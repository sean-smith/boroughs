from flask import Flask, Response, request, render_template, redirect, url_for
import json
from pprint import pprint
import geojson
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/get_borough', methods=['POST'])
def get_borough():
	lat = float(request.form['lat'])
	lng = float(request.form['long'])
	print "lat = %f" % (lat)
	print "long = %f" % (lng)
	return borough(lat, lng, 'static/nyc_boroughs.json')["BoroName"]


def borough(lat, lng, path):
	with open(path) as data_file:
		data = json.load(data_file)
		geo = geojson.FeatureCollection(data["features"])
		for feature in geo['features']:
			multipolygon = feature["geometry"]["coordinates"]
			is_multipolygon = feature["geometry"]["type"] == "MultiPolygon"
			if in_polygon(lat, lng, multipolygon, is_multipolygon):
				return feature["properties"]
	return "Not found."

def x(lnglat):
	return lnglat[0]

def y(lnglat):
	return lnglat[1]

def in_polygon(lat, lng, polygon, is_multipolygon):
	for coord in polygon:
		if is_multipolygon:
			coord = coord[0]
		c = False
		j = len(coord) - 1;
		for i in range(len(coord)):
			px = lng
			py = lat
			if ( ((y(coord[i])>py) != (y(coord[j])>py)) and 
				(px < (x(coord[j])-x(coord[i])) * (py-y(coord[i])) / (y(coord[j])-y(coord[i])) + x(coord[i])) ):
				c = not c
			j = i
		if c:
			return True
	return False


def test():
	# lat, long 
	# 40.707438, -74.006302
	# Assuming lat = Y and long = X
	print "Staten Island (%f, %f)" % (40.6306300839918, -74.08407211303711)
	print(borough(40.6306300839918, -74.08407211303711, 'static/nyc_boroughs.json')["BoroName"])

	print "Manhattan (%f, %f)" % (40.7189000170401, -73.99171829223633)
	print(borough(40.7189000170401, -73.99171829223633, 'static/nyc_boroughs.json')["BoroName"])

	print "Bronx (%f, %f)" % (40.822383381646446, -73.91275405883789)
	print(borough(40.822383381646446, -73.91275405883789, 'static/nyc_boroughs.json')["BoroName"])

	print "Brooklyn (%f, %f)" % (40.68948969132278, -73.98347854614258)
	print(borough(40.68948969132278, -73.98347854614258, 'static/nyc_boroughs.json')["BoroName"])

	print "Queens (%f, %f)" % (40.748037258302986, -73.88279914855957)
	print(borough(40.748037258302986, -73.88279914855957, 'static/nyc_boroughs.json')["BoroName"])

	print "Fenway/Kenmore (%f, %f)" % (42.348688, -71.102873)
	print(borough(42.348688, -71.102873, 'static/boston.geojson')["name"])

# test()
