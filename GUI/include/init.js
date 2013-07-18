/*-----------------------------------------------------------------------------
 Needs http://maps.googleapis.com/maps/api/js?libraries=places&sensor=false
 -----------------------------------------------------------------------------*/
"use strict"

function init() {
   
   // Make map
   var mapOptions = {
      center: new google.maps.LatLng(59.3695880, 18.0633610),
      //disableDoubleClickZoom: false,
      zoom: 12,
      mapTypeId: google.maps.MapTypeId.ROADMAP
   };
   
   var map = new google.maps.Map(document.getElementById('map'), mapOptions)
  
   // Connect to server
   connect();
  
}
google.maps.event.addDomListener(window, 'load', init);
