/*-----------------------------------------------------------------------------
 Needs http://maps.googleapis.com/maps/api/js?libraries=places&sensor=false
 -----------------------------------------------------------------------------*/
/* Globals:
 * map
 * */

"use strict"


function addMarker(lat, lng) {
   //msg("Will add marker at: "+lat+", "+lng)
   
   var loc=new google.maps.LatLng(lat, lng)
   
   var marker = new google.maps.Marker({
      map: map,
      position: loc,
   });
   
}


// General box
function addBox(lat1, lng1, lat2, lng2, color) {
   //msg("Boundaries set to: "+lat1+", "+lng1+", "+lat2+", "+lng2)
   
   var loc1=new google.maps.LatLng(lat1, lng1)
   var loc2=new google.maps.LatLng(lat2, lng2)
   
   var rectangle = new google.maps.Rectangle({
      strokeColor: color,
      strokeOpacity: 0.7,
      strokeWeight: 1,
      fillColor: color,
      fillOpacity: 0.09,
      map: map,
      bounds: new google.maps.LatLngBounds(loc1, loc2)
  });
}

// Center map to specific location
function centerMap(lat1, lng1, lat2, lng2) {
   var loc1=new google.maps.LatLng(lat1, lng1)
   var loc2=new google.maps.LatLng(lat2, lng2)
   var bounds=new google.maps.LatLngBounds(loc1, loc2)
   map.fitBounds(bounds)
}
