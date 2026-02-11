import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="DarFarePredictor", layout="wide")

st.title("🚕 Dar es Salaam Live Ride Navigator")
st.write("Choose your current location and destination to estimate distance and fare.")

map_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />

<style>
body {
  margin: 0;
  font-family: Arial, sans-serif;
}

.controls {
  padding: 10px;
  background: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

button {
  padding: 8px 14px;
  border: none;
  background: #1e90ff;
  color: white;
  cursor: pointer;
  border-radius: 4px;
}

#info {
  font-weight: bold;
}

#map {
  height: 520px;
}
</style>
</head>

<body>

<div class="controls">
  <button onclick="setPickup()">Use Current Location</button>
  <span id="info">Select destination on map</span>
</div>

<div id="map"></div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<script>
var map = L.map('map').setView([-6.8, 39.25], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap'
}).addTo(map);

var pickupMarker = null;
var destinationMarker = null;
var routeLine = null;

// Haversine distance (km)
function haversine(lat1, lon1, lat2, lon2) {
  const R = 6371;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a =
    Math.sin(dLat/2) ** 2 +
    Math.cos(lat1 * Math.PI/180) *
    Math.cos(lat2 * Math.PI/180) *
    Math.sin(dLon/2) ** 2;

  return 2 * R * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

function updateRoute() {
  if (pickupMarker && destinationMarker) {
    var p = pickupMarker.getLatLng();
    var d = destinationMarker.getLatLng();

    var distance = haversine(p.lat, p.lng, d.lat, d.lng).toFixed(2);

    document.getElementById("info").innerText =
      "Distance: " + distance + " km";

    if (routeLine) {
      map.removeLayer(routeLine);
    }

    routeLine = L.polyline([p, d], { dashArray: '5,10' }).addTo(map);
  }
}

// Pickup using GPS
function setPickup() {
  navigator.geolocation.getCurrentPosition(function(position) {
    var lat = position.coords.latitude;
    var lng = position.coords.longitude;

    if (pickupMarker) {
      map.removeLayer(pickupMarker);
    }

    pickupMarker = L.marker([lat, lng], { draggable: true })
      .addTo(map)
      .bindPopup("Pickup Location")
      .openPopup();

    pickupMarker.on('dragend', updateRoute);
    map.setView([lat, lng], 16);
    updateRoute();
  }, function() {
    alert("Location permission denied");
  });
}

// Destination by map click
map.on('click', function(e) {
  if (destinationMarker) {
    map.removeLayer(destinationMarker);
  }

  destinationMarker = L.marker(e.latlng, { draggable: true })
    .addTo(map)
    .bindPopup("Destination")
    .openPopup();

  destinationMarker.on('dragend', updateRoute);
  updateRoute();
});
</script>

</body>
</html>
"""

html(map_html, height=600)