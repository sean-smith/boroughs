# Boroughs

Simple application that determines the polygon that a point is contained in. The main application logic is implemented in `polygon.py` with the routing done in `app.py`.

To run:
	
	export FLASK_APP=app.py
	export FLASK_DEBUG=1
	flask run -h 0.0.0.0

Now type into your web browser: http://localhost:5000

The graphs can be viewed from:

http://localhost:5000/yellow
http://localhost:5000/green
http://localhost:5000/all


### MPC

The multi party computation portion of this application is contained in `mpc/`. The important file to look at is `point_in_poly.py` which is the main Viff application to create the graph output.

### Chord Diagrams

The chord diagrams are generated using d3, the source is in `templates/trips.html` with data coming from `static/data/yellow`, `static/data/green`, and `static/data/nta`.

You'll notice two files in those directories one `matrix.json` file and one `map.json` file. The matrix contains the raw list of edges and the map contains some metadata about the nodes.



