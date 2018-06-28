// Mapbox API
var mapbox = "https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiaHAtbnVuZXMiLCJhIjoiY2ppZHQzcHZ3MDZhNTNrbngzaXkza29jaCJ9.yJRB2I7604kQwNLwgBsqvg";

// Creating map object
var myMap = L.map("map", {
  center: [37.76,  -122.43],
  zoom: 11
});

// Adding tile layer to the map
L.tileLayer(mapbox).addTo(myMap);

// // Building API query URL
// var baseURL = "https://data.sfgov.org/api/views/956q-2t7k/rows.json?";
// // var date = "$where=created_date between'2018-01-10T12:00:00' and '2018-06-01T14:00:00'";
// var complaint = "&complaint_type=Rodent";
// var limit = "&$limit=10000";

// // Assembling API query URL
// var url = baseURL + date + complaint + limit;

// Grabbing the data with d3..
d3.json(dataset.js, function(features) {

  // Creating a new marker cluster group
  var markers = L.markerClusterGroup();

  // Loop through our data...
  for (var i = 0; i < features.length; i++) {
    // set the data location property to a variable
    var location = features[i].geometry;

    // If the data has a location property...
    if (location) {

      // Add a new marker to the cluster group and bind a pop-up
      markers.addLayer(L.marker([location.coordinates[1], location.coordinates[0]])
        .bindPopup(features[i].Description));
    }

  }

  // Add our marker cluster layer to the map
  myMap.addLayer(markers);

});
