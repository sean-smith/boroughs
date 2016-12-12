import pandas as pd
import numpy as np
import json
from pprint import pprint
import geojson

with open('static/nyc_census_tracts.json') as data_file:
	data = json.load(data_file)
	geo = geojson.FeatureCollection(data["features"])

def borough(lat, lng, path):
	for feature in geo['features']:
		multipolygon = feature["geometry"]["coordinates"]
		is_multipolygon = feature["geometry"]["type"] == "MultiPolygon"
		if in_polygon(lat, lng, multipolygon, is_multipolygon):
			return feature["properties"]
	return {'NTACode': 'Not Found', 'BoroName': 'Not Found'}

def create_nta_map(inpath, outpath):
	d = {}
	i = 0
	colors = ["#3b76de", "#5fba7d", "#f4b400", "#CF3300", "#F781BF"]
	with open(path) as data_file:
		data = json.load(data_file)
		geo = geojson.FeatureCollection(data["features"])
		for feature in geo['features']:
			if not feature['properties']['NTACode'] in d:
				d[feature['properties']['NTACode']] = {
				"NTACode": feature['properties']['NTACode'], 
				"NTAName": feature['properties']['NTAName'],
				"BoroCode": feature['properties']['BoroCode'],
				"BoroName": feature['properties']['BoroName'],
				"id": i,
				"color": colors[int(feature['properties']['BoroCode']) - 1]
				}
				i += 1
	pprint(d)
	print "len = %d" % (len(d))
	with open(outpath, 'w') as outfile:
		json.dump(d, outfile)

def create_borough_map(inpath, outpath):
	d = {}
	i = 0
	colors = ["#3b76de", "#5fba7d", "#f4b400", "#CF3300", "#F781BF"]
	with open(inpath) as data_file:
		data = json.load(data_file)
		features = geojson.FeatureCollection(data["features"])
		for feature in features['features']:
			if not feature['properties']['BoroName'] in d:
				d[feature['properties']['BoroName']] = {
				"BoroCode": feature['properties']['BoroCode'],
				"BoroName": feature['properties']['BoroName'],
				"id": i,
				"color": colors[int(feature['properties']['BoroCode']) - 1]
				}
				i += 1
	pprint(d)
	print "len = %d" % (len(d))
	with open(outpath, 'w') as outfile:
		json.dump(d, outfile)
	
def create_matrix(skip_rows,n_rows, csvpath, geojson, trip_map, trip_matrix):
	# l = [[0]* 195] * 195
	i = 0
	with open(trip_matrix, 'r+') as tripmatrix:
		l = json.load(tripmatrix)
		with open(trip_map, 'r') as data_file:
			tripmap = json.load(data_file)
			df = pd.read_csv(csvpath, nrows=n_rows, skiprows=[j for j in range(1, skip_rows)], index_col=0)
			for row in df.itertuples():
				start_lng = row.Pickup_longitude
				start_lat = row.Pickup_latitude
				end_lng = row.Dropoff_longitude
				end_lat = row.Dropoff_latitude
				start_nta_code = borough(start_lat, start_lng, geojson)['NTACode']
				end_nta_code = borough(end_lat, end_lng, geojson)['NTACode']
				if start_nta_code == 'Not Found' or end_nta_code == 'Not Found':
					continue
				start_index = tripmap[start_nta_code]['id']
				end_index = tripmap[end_nta_code]['id']
				l[start_index][end_index] += 1
				i += 1
				print "%s (%f, %f) %d" % (start_nta_code, start_lat, start_lng, start_index)
				print "%s (%f, %f) %d" % (end_nta_code, end_lat, end_lng, end_index)
				if (i % 100) == 0:
					tripmatrix.seek(0);
					json.dump(l, tripmatrix)
					print "======= Done %d ======" % (i)
		tripmatrix.seek(0);
		json.dump(l, tripmatrix)
		print "======= Done %d ======" % (i)

def create_borough_matrix(skip_rows,n_rows, csvpath, geojson, trip_map, trip_matrix):
	l = [[0]* 5] * 5
	i = 0
	with open(trip_matrix, 'w') as tripmatrix:
		# l = json.load(tripmatrix)
		with open(trip_map, 'r') as data_file:
			tripmap = json.load(data_file)
			df = pd.read_csv(csvpath, nrows=n_rows, index_col=0)
			for row in df.itertuples():
				start_lng = row.pickup_longitude
				start_lat = row.pickup_latitude
				end_lng = row.dropoff_longitude
				end_lat = row.dropoff_latitude
				start_nta_code = borough(start_lat, start_lng, geojson)['BoroName']
				end_nta_code = borough(end_lat, end_lng, geojson)['BoroName']
				if start_nta_code == 'Not Found' or end_nta_code == 'Not Found':
					continue
				start_index = tripmap[start_nta_code]['id']
				end_index = tripmap[end_nta_code]['id']
				l[start_index][end_index] += 1
				i += 1
				print "%s (%f, %f) %d" % (start_nta_code, start_lat, start_lng, start_index)
				print "%s (%f, %f) %d" % (end_nta_code, end_lat, end_lng, end_index)
				if (i % 100) == 0:
					tripmatrix.seek(0);
					json.dump(l, tripmatrix)
					print "======= Done %d ======" % (i)
		tripmatrix.seek(0);
		json.dump(l, tripmatrix)
		print "======= Done %d ======" % (i)

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

if __name__ == '__main__':
	# test()
	create_borough_map('static/nyc_census_tracts.json', 'static/data/yellow/borough-map.json')
	# create_map('static/nyc_census_tracts.json', 'static/data/trip-map.json')
	create_borough_matrix(skip_rows=0, 
		n_rows=1000, 
		csvpath='static/data/yellow_tripdata_2016-01.csv', 
		geojson='static/nyc_census_tracts.json', 
		trip_map='static/data/yellow/borough-map.json', 
		trip_matrix='static/data/yellow/borough-matrix.json')
	# create_matrix(skip_rows=4000, n_rows=6000, csvpath='static/data/green_tripdata_2016-01.csv', geojson='static/nyc_census_tracts.json', trip_map='static/data/trip-map.json', trip_matrix='static/data/trip-matrix.json')