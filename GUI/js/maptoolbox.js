/*-----------------------------------------------------------------------------
 Needs http://maps.googleapis.com/maps/api/js?libraries=places&sensor=false
 -----------------------------------------------------------------------------*/
/* Globals:
 * map
 * */

"use strict"

function addMarker(lat, lng) {
   msg("Will add marker at: "+lat+", "+lng)
   
   var loc=new google.maps.LatLng(lat, lng)
   
   var marker = new google.maps.Marker({
      map: map,
      position: loc,
   });
   
}

function addBox(lat1, lng1, lat2, lng2) {
   msg("Boundaries set to: "+lat1+", "+lng1+", "+lat2+", "+lng2)
   
   var loc1=new google.maps.LatLng(lat1, lng1)
   var loc2=new google.maps.LatLng(lat2, lng2)
   
   var rectangle = new google.maps.Rectangle({
      strokeColor: '#FF0000',
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: '#FF0000',
      fillOpacity: 0.35,
      map: map,
      bounds: new google.maps.LatLngBounds(loc1, loc2)
  });

}
