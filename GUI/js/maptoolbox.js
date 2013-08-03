/*-----------------------------------------------------------------------------
 Needs http://maps.googleapis.com/maps/api/js?libraries=places&sensor=false
 -----------------------------------------------------------------------------*/
/* Globals:
 * map   : google map
 * boxes : array of google rectangles
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
      fillOpacity: 0.19,
      map: map,
      bounds: new google.maps.LatLngBounds(loc1, loc2)
  });
  
  boxes.push(rectangle)
}

// Removes ANY box at specific coordinates
function removeBox(lat1, lng1, lat2, lng2) {
   
   for (var i=0; i<boxes.length; i++){
      var lt1=boxes[i].getBounds().getNorthEast().lat()
      var lg1=boxes[i].getBounds().getNorthEast().lng()
      var lt2=boxes[i].getBounds().getSouthWest().lat()
      var lg2=boxes[i].getBounds().getSouthWest().lng()
      
      if ((lt1==lat1 && lg1==lng1 && lt2==lat2 && lg2==lng2) ||
          (lt1==lat2 && lg1==lng2 && lt2==lat1 && lg2==lng1))
      {
         boxes[i].setMap(null);
      }
   }
   
   
   //alert("Removing box ")
}


// Center map to specific location
function centerMap(lat1, lng1, lat2, lng2) {
   var loc1=new google.maps.LatLng(lat1, lng1)
   var loc2=new google.maps.LatLng(lat2, lng2)
   var bounds=new google.maps.LatLngBounds(loc1, loc2)
   map.fitBounds(bounds)
}
