import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(page_title="DarTaxAI", layout="wide")

# ---------------- Dashboard Header ----------------
st.markdown(
    """
    <style>
    .metric-box {
        background: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🚕 DarFarePredictor Dashboard")
st.write("Live GPS → Route distance → Fare estimation")

col1, col2, col3 = st.columns(3)

col1.markdown("<div class='metric-box'><h3>Base Fare</h3><h2>2000 TZS</h2></div>", unsafe_allow_html=True)
col2.markdown("<div class='metric-box'><h3>Per KM</h3><h2>700 TZS</h2></div>", unsafe_allow_html=True)
col3.markdown("<div class='metric-box'><h3>City</h3><h2>Dar es Salaam</h2></div>", unsafe_allow_html=True)

st.markdown("---")

# ---------------- Live Map + Fare Logic ----------------
map_html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<link rel="stylesheet" href="https://unpkg.com/leaflet-routing-machine@3.2.12/dist/leaflet-routing-machine.css"/>

<style>
#map {
  height: 520px;
  border-radius: 10px;
}

.info-box {
  padding: 10px;
  font-size: 16px;
  font-weight: bold;
}
</style>
</head>

<body>

<div class="info-box" id="info">Allow GPS & click map to select destination</div>
<div id="map"></div>

<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://unpkg.com/leaflet-routing-machine@3.2.12/dist/leaflet-routing-machine.js"></script>

<script>
var BASE_FARE = 2000;
var COST_PER_KM = 700;

var map = L.map('map').setView([-6.8, 39.25], 13);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap'
}).addTo(map);

var userLat, userLng;
var routingControl = null;

// Get GPS location
navigator.geolocation.getCurrentPosition(
  function(pos) {
    userLat = pos.coords.latitude;
    userLng = pos.coords.longitude;

    L.marker([userLat, userLng])
      .addTo(map)
      .bindPopup("Your Location")
      .openPopup();

    map.setView([userLat, userLng], 15);
  },
  function() {
    alert("GPS permission denied");
  }
);

// Select destination by clicking map
map.on('click', function(e) {

  if (!userLat) {
    alert("Waiting for GPS location");
    return;
  }

  if (routingControl) {
    map.removeControl(routingControl);
  }

  routingControl = L.Routing.control({
    waypoints: [
      L.latLng(userLat, userLng),
      L.latLng(e.latlng.lat, e.latlng.lng)
    ],
    routeWhileDragging: false,
    addWaypoints: false,
    draggableWaypoints: false,
    show: false
  }).addTo(map);

  routingControl.on('routesfound', function(event) {
    var route = event.routes[0];
    var distanceKm = (route.summary.totalDistance / 1000).toFixed(2);
    var fare = Math.round(BASE_FARE + (distanceKm * COST_PER_KM));

    document.getElementById("info").innerHTML =
      "Distance: " + distanceKm + " km | Estimated Fare: " + fare + " TZS";
  });
});
</script>

</body>
</html>
"""

html(map_html, height=600)

st.markdown("---")
st.caption("⚠️ Fare is an estimate for demonstration purposes only.")
