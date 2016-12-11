// Adds a map with a clickable marker

var marker = null;
var map = null;
var infowindow = null;

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
		zoom: 12,
		center: {lat: 40.707438, lng: -74.006302}
	});
	google.maps.event.addListener(map, 'click', function(event) {
		if (marker) {
			marker.setMap(null);
			marker = null;
		}
		addMarker(event.latLng, map);
	});
	load_geojson()
}

function load_geojson() {
	map.data.loadGeoJson('static/nyc_boroughs.json');
	map.data.setStyle(function(feature) {
		var num = feature.getProperty('BoroCode') - 1;
		var colors = ['red', 'green', 'blue', 'yellow', 'purple'];
		return {
			fillColor: colors[num],
			strokeWeight: 1
		};
	});
}