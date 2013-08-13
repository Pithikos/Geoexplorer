from lib.google_places import *
from lxml import etree
from time import sleep
from config import *
from classes.ResponseParser import GoogleResponse

class GoogleRequester():
   
   logger = None

   # Returns status of response
   def __init__(self, logger):
      G_set_key(config["SERVICE_KEY"])
      self.logger=logger

   def send_request(self, request, maxRetries, retryInterval):
      logger=self.logger
      location    = request['location']
      radius      = request['radius']
      searchitems = request['searchitems']

      retries = -1
      googleResponse= None
      
      # Send the request
      while (retries!=maxRetries):
         resp=G_radarsearch(location, radius, searchitems)
         googleResponse=GoogleResponse(resp)
         status=googleResponse.status
         
         if (status == 'OK'):
            break
            
         elif (status == 'ZERO_RESULTS'):
            print("Zero results")
            break
            
         elif (status == 'OVER_QUERY_LIMIT'):
            if (retries == maxRetries):
               print("Query limit exceeded for today. Scanning stopped.")
               # EXIT PROGRAM HERE
            print("Query limit exceeded. Will wait a bit and retry.")
            sleep(config['scheduler']['ON_QUERY_LIMIT_WAIT'])
            retries+=1
            continue

         elif (status == 'INVALID_REQUEST'):
            print("Invalid request")
            # EXIT PROGRAM HERE
            
         elif (status == 'REQUEST_DENIED'):
            print("Request denied. Is the Google key correct?")
            # EXIT PROGRAM HERE
            
         else:
            logger.append('scan', 'Unknown error in response from Google server')
            print("Unknown error in response from Google server")
            print("Page received from Google: \n", etree.tostring(googleResponse.root).decode("utf-8"))
            # EXIT PROGRAM HERE

      return googleResponse
