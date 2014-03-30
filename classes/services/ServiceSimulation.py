from time import sleep
import random

# Makes a search for each box
class ServiceSimulationSearch():
   
   # SERVICE RULES
   service = {
      'request': {
         'COST_PER_REQUEST' : 1,
         'MAX_COST_DAY'     : 1000
      },
      'response': {
         'MAX_RESULTS' : 40
      },
      'box': {
         'MAX_X_DISTANCE' : 50000,  # 50km max radius
         'MAX_Y_DISTANCE' : 50000,  # 50km max radius
      }
   }

   resultsN    = 0

   def search(self, box, logger):

      # Get the markers from the response
      markers=[]
      sleep(0.2)
      for each in range(1, random.randrange(0, 50, 1)):
         self.resultsN+=1
         latOffset = random.randrange(0, int(box.length_lat()*100000))
         lngOffset = random.randrange(0, int(box.length_lng()*100000))
         lat = box.WN[0] - (latOffset/100000)
         lng = box.WN[1] + (latOffset/100000)
         print("Box bounds            :", box.bounds())
         print("Box lengths           :", box.length_lat(), box.length_lng())
         print("Box offsets for marker:", latOffset, lngOffset)
         print("Marker                :", lat, lng)
         markers.append((lat, lng))
         logger.log_result("Result at: "+str((lat, lng)))
      
      logger.log_scan(str(box.bounds())+" : Results: "+str(self.resultsN))
      
      return markers
