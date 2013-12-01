from config import *
from lib.geotools import *
from classes.Requester import *
from classes.ResponseParser import *

# Guidelines for every service:
#   MUST have a 'search' function which takes a 'box' object as parameter
#   MUST return a list of markers(latitude, longitude pairs)


# Makes a google radar search for each box
class GoogleRadarSearch():

   searchItems = None
   
   # Override some config values
   def override_config(self, scanner):
      if scanner.config['box']['MAX_X_DISTANCE'] > 100000:
         scanner.config['box']['MAX_X_DISTANCE'] = 100000  # 50km max radius
      if scanner.config['box']['MAX_Y_DISTANCE'] > 100000:
         scanner.config['box']['MAX_Y_DISTANCE'] = 100000  # 50km max radius
      scanner.config['costs']['PER_REQUEST'] = 5           # 5 cost per google radar

   def __init__(self, key, searchItems):
      self.searchItems=searchItems
      G_set_key(key)

   def search(self, box, logger):

      countryCode=getCountryCode(box.center[0], box.center[1])
      #print("Pos: ", box.bounds())
      #print("Country code: ", countryCode)

      '''
      if (countryCode == 'UNKNOWN'):
         break
      if (countryCode != config['limiter']['country_code']):
         logger.append('scan', str(box.bounds())+" : Skipped because country_code: "+countryCode)
         toScan.pop(0)
         continue
      '''

      # Make the radar search request and send it
      googleRequester=GoogleRequester(logger)
      location=str(box.center[0])+","+str(box.center[1])
      radius=max(box.xMeters, box.yMeters)/2  
      
      req= {'location': location,
            'radius': radius,
            'searchitems': self.searchItems}
      
      googleResponse = googleRequester.send_request(req, 0, 0)
      logger.append('scan', str(box.bounds())+" : "+googleResponse.status)
   
      # Get the markers from the response
      markers=[]
      for result in googleResponse.results:
         markers.append(result['location'])
         print(result['location'])
      logger.append("result", str(box.bounds())+" : "+str(googleResponse.resultsN))
   
      return markers
