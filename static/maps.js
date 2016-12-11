// Adds a map with a clickable marker

var marker = null;
var map = null;
var infowindow = null;

var boston = {
	name: "Boston",
	loc: {lat: 42.348688, lng: -71.102873},
	zoom: 12,
	geojson: 'static/boston.geojson',
	style: get_boston_style
};

var nyc_boroughs = {
	name: "NYC Boroughs",
	loc: {lat: 40.7189000170401, lng: -73.99171829223633},
	zoom: 10,
	geojson: 'static/nyc_boroughs.json',
	style: get_nyc_borough_style
};

var nyc_tracts = {
	name: "NYC Tracts",
	loc: {lat: 40.7189000170401, lng: -73.99171829223633},
	zoom: 12,
	geojson: 'static/nyc_census_tracts.json',
	style: get_nyc_tracts_style
};

var nyc_blocks = {
	name: "NYC Blocks",
	loc: {lat: 40.7189000170401, lng: -73.99171829223633},
	zoom: 10,
	geojson: 'static/nyc_census_blocks.json',
	style: get_nyc_blocks_style
};

var place = nyc_boroughs;

$(document).ready(function() {
	$("#data").change(function(data) {
		var option = $(this).val();
		console.log(option);
		map.data.setStyle({});
		if (option == 'static/nyc_census_tracts.json') {
			place = nyc_tracts;
		} else if (option == 'static/nyc_boroughs.json') {
			place = nyc_boroughs;
		} else if (option == 'static/nyc_census_blocks.json') {
			place = nyc_blocks;
		} else {
			place = boston;
		}
		initMap();
	});
});


function openWindow(data) {
	infowindow = new google.maps.InfoWindow({
		content: data
  	});
	infowindow.open(map, marker);
}

function addMarker(location, map) {
	marker = new google.maps.Marker({
		position: location,
		map: map
	});
	document.getElementById('lat').value = location.lat();
	document.getElementById('long').value = location.lng();
	$.post( "get_borough", {'lat': location.lat(), 'long': location.lng()}, function( data ) {
  		openWindow(data);
	});
}

function initMap() {
	map = new google.maps.Map(document.getElementById('map'), {
		zoom: place.zoom,
		center: place.loc
	});
	google.maps.event.addListener(map, 'click', function(event) {
		if (marker) {
			marker.setMap(null);
			marker = null;
		}
		addMarker(event.latLng, map);
	});
	load_geojson(place.geojson);
}

function load_geojson(path) {
	map.data.loadGeoJson(path);
	map.data.setStyle(function(feature) {
		return place.style(feature);
	});
}

function get_nyc_borough_style(feature) {
	var num = feature.getProperty('BoroCode') - 1;
	var colors = ['red', 'green', 'blue', 'yellow', 'orange'];
	return {
		fillColor: colors[num],
		title: feature.getProperty('BoroName'),
		strokeWeight: 1,
		fillOpacity: .1,
		clickable: false
	};
}

function get_nyc_tracts_style(feature) {
	var num = feature.getProperty('NTACode') - 1;
	var colors = ['red', 'green', 'blue', 'yellow', 'orange'];
	return {
		fillColor: colors[Math.abs(feature.getProperty('NTAName').hashCode()) % 5],
		title: feature.getProperty('NTAName'),
		strokeWeight: 1,
		fillOpacity: .1,
		clickable: false
	};
}

function get_nyc_blocks_style(feature) {
	var num = feature.getProperty('NTACode') - 1;
	var colors = ['red', 'green', 'blue', 'yellow', 'orange'];
	return {
		fillColor: colors[Math.abs(feature.getProperty('CB2010').hashCode()) % 5],
		title: feature.getProperty('NTAName'),
		strokeWeight: 1,
		fillOpacity: .1,
		clickable: false
	};
}

function get_boston_style(feature) {
	return {
		fillColor: feature.getProperty('fill'),
		title: feature.getProperty('name'),
		strokeWeight: 1,
		fillOpacity: feature.getProperty('fill-opacity'),
		clickable: false
	};
}

String.prototype.hashCode = function() {
  var hash = 0, i, chr, len;
  if (this.length === 0) return hash;
  for (i = 0, len = this.length; i < len; i++) {
    chr   = this.charCodeAt(i);
    hash  = ((hash << 5) - hash) + chr;
    hash |= 0; // Convert to 32bit integer
  }
  return hash;
};
