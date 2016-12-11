// Adds a map with a clickable marker

var marker = null;
var map = null;
var infowindow = null;

var boston = {
	name: "Boston",
	loc: {lat: 40.7189000170401, lng: -73.99171829223633},
	zoom: 12,
	geojson: 'static/boston.geojson'
};

var nyc = {
	name: "NYC",
	loc: {lat: 42.348688, lng: -71.102873},
	zoom: 12,
	geojson: 'static/nyc_boroughs.json'
};

$(document).ready(function() {
	$("#data").change(function(data) {
		console.log($(this).val());
		map.data.setStyle({});
		load_geojson($(this).val());
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
	var location = boston;
	map = new google.maps.Map(document.getElementById('map'), {
		zoom: location.zoom,
		center: location.loc
	});
	google.maps.event.addListener(map, 'click', function(event) {
		if (marker) {
			marker.setMap(null);
			marker = null;
		}
		addMarker(event.latLng, map);
	});
	load_geojson(location.geojson);
}

function load_geojson(path) {
	map.data.loadGeoJson(path);
	map.data.setStyle(function(feature) {
		return get_nyc_style(feature);
	});
}

function get_nyc_style(feature) {
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

function get_boston_style(feature) {
	return {
		fillColor: feature.getProperty('fill'),
		title: feature.getProperty('name'),
		strokeWeight: 1,
		fillOpacity: feature.getProperty('fill-opacity'),
		clickable: false
	};
}
