/*-----------------------------------------------------------------------------
 Needs http://maps.googleapis.com/maps/api/js?libraries=places&sensor=false
 -----------------------------------------------------------------------------*/
/* Globals:
 * map   : google map
 * boxes : array of google rectangles
 * */

"use strict"


function addMarker(lat, lng) {
   var loc=new google.maps.LatLng(lat, lng)
   var marker = new google.maps.Marker({
      map: map,
      position: loc,
   });
}


// Add box on map
function addBox(lat1, lng1, lat2, lng2, color) {
   var loc1=new google.maps.LatLng(lat1, lng1)
   var loc2=new google.maps.LatLng(lat2, lng2)
   var rectangle = new google.maps.Rectangle({
      strokeColor: color,
      strokeOpacity: 0.7,
      strokeWeight: 1,
      fillColor: color,
      fillOpacity: 0.19,
      map: map,
      bounds: new google.maps.LatLngBounds(loc1, loc2)
  });
  var index = makeIndex(lat1, lng1, lat2, lng2)
  boxes[index] = rectangle
}


// Removes box from map
function removeBox(lat1, lng1, lat2, lng2) {
   var index = makeIndex(lat1, lng1, lat2, lng2)
   boxes[index].setMap(null);
   boxes[index] = null
}


// Center map to specific location
function centerMap(lat1, lng1, lat2, lng2) {
   var loc1=new google.maps.LatLng(lat1, lng1)
   var loc2=new google.maps.LatLng(lat2, lng2)
   var bounds=new google.maps.LatLngBounds(loc1, loc2)
   map.fitBounds(bounds)
}


// Make an index to be used for the boxes hash table
function makeIndex(lat1, lng1, lat2, lng2) {
   return lat1+", "+lng1+", "+lat2+", "+lng2
}


// ------------------- Debugging tools --------------------

// Gives the bounds of a box in string
function boxBoundsStr(box) {
   var lt1=box.getBounds().getNorthEast().lat()
   var lg1=box.getBounds().getNorthEast().lng()
   var lt2=box.getBounds().getSouthWest().lat()
   var lg2=box.getBounds().getSouthWest().lng()
   return lt1+", "+lg1+", "+lt2+", "+lg2
}

// Prints all boxes
function showBoxes() {
   var line = ''
   for (var key in boxes)
      var box = boxes[key]
      line += "("+boxBoundsStr(box)+"), "
   msg("Boxes: "+line)
}
