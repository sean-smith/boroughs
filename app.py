from flask import Flask, Response, request, render_template, redirect, url_for
from polygon import borough
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/green')
def green():
	return render_template('trips.html', 
		matrix="data/green/borough-matrix.json",
		map="data/green/borough-map.json")

@app.route('/yellow')
def yellow():
	return render_template('trips.html', 
		matrix="data/yellow/borough-matrix.json", 
		map="data/yellow/borough-map.json")

@app.route('/all')
def all():
	return render_template('nta.html', 
		matrix="data/nta/trip-matrix.json", 
		map="data/nta/trip-map.json")

@app.route('/get_borough', methods=['POST'])
def get_borough():
	lat = float(request.form['lat'])
	lng = float(request.form['long'])
	print "lat = %f" % (lat)
	print "long = %f" % (lng)
	props = borough(lat, lng, 'static/nyc_census_tracts.json');
	return "CT Code: %s<br>NTA Name: %s<br>Borough Name: %s" % (props['CTLabel'], props['NTAName'], props['BoroName'])


