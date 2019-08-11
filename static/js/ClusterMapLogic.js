
console.log('begin Java script');

document.getElementById('map');

// document.getElementById('olportmap').innerHTML = "<div id='map'></div>";
// Creating map object
var myMap = L.map("map", {
    center: [44.9, -93.0],
    zoom: 4
  });
  
  // Adding tile layer to the map
  L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.streets",
    accessToken: API_KEY
  }).addTo(myMap);
  
  // Grab data from API:
  // var baseURL = "https://data.cityofnewyork.us/resource/fhrw-4uyv.json?";
  // var url = baseURL;
  // d3.json(url, function(response)

// or

// grab data from json file
// d3.json("../static/js/GeoDataJsonFile.json", 

  var URL = `/Geodata`;
  d3.json(URL, function(response)


  {
  console.log(response[0]);
    // Create a new marker cluster group
    var markers = L.markerClusterGroup();
  
    // Loop through data
    for (var i = 0; i < response.length; i++) {
  
      // Set the data location property to a variable
      var lat = response[i].latitude;
      var lon = response[i].longitude;
      var img=response[i].FileAddress;
  
      // Check for location property
      if (location) {
  
        // Add a new marker to the cluster group and bind a pop-up
        markers.addLayer(L.marker([lat, lon])
          .bindPopup( '<div class="ppcont"> <img style="max-height:200px;max-width:200px;" img src=' + img + "/>"
          ,));
      }
  
    }
  
    // Add our marker cluster layer to the map
    myMap.addLayer(markers);
  
  });
  // ,{maxWidth: 800, closeOnClick: true}));
  // working code: .bindPopup( '<img style="max-height:200px;max-width:200px;" img src=' + img + "/>"
  // <div class='ppcont'><img src='yourimg.jpg' /></div>