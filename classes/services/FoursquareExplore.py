from urllib.request import urlopen
from lxml import etree
from time import sleep
import json
import re

# MAX PROBLEM:
# Use 'SCANNING_AREA' : (59.625, 16.5, 59.59375, 16.625) for demonstration.
# In the area there are two MAX reastaurants. Both are logged to the results
# log file. However only one of the two has a marker on the map.
# furthermore, as the results count on the Scanner is depended on the amount of
# markers, we get one less count than what we have in the results log file.
#
#
# Possible solution:
# -
#

class FoursquareSearch():
   
   # SERVICE RULES
   service = {
      'authentication':{
         'REQUIRED'    : False
      },
      'response': {
         'MAX_RESULTS' : 30
      },
      'box': {
         'MAX_X_DISTANCE' : 50000,  # max width  in real m.
         'MAX_Y_DISTANCE' : 50000,  # max height in real m.
      }
   }

   keyword = None

   def __init__(self, keyword):
      self.keyword=keyword

   def search(self, box, logger):
      # Send request
      requester=FoursquareRequester(logger)
      location=str(box.center[0])+","+str(box.center[1])
      req= {'ne': box.NE,
            'sw': box.WS,
            'q' : self.keyword}
      response = requester.send_request(req, 0, 0)
      resp = ResponseParser(response, logger)
      logger.log_scan(str(box.bounds())+" : "+ str(resp.resultsN) +" results")
      
      # Get markers from response
      markers=[]
      for result in resp.results:
         markers.append(result[1])
         logger.log_result(result[0]+" : "+str(result[1]))

      return markers


# results: [ (Name, (lat, lng), Address, Country), .. ]
class ResponseParser():
   
   results  = None
   resultsN = 0

   # Returns status of response
   def __init__(self, response, logger):
      self.results = []
      root = etree.HTML(response)
      
      script  = root.find("body//script").text
      patErr     = r"(fourSq.config.explore.errorMeta = {)(.*?)(};)"
      patResults = r"(fourSq.config.explore.response = {)(.*?)(};)"
      error      = re.search(patErr, script)
      results    = re.search(patResults, script)
      
      if error:
         print("Response gave error:", error.group(2))
         logger.log_scan("Response gave error: "+error.group(2))
         logger.log_scan("Response was: "+str(response))
         logger.log_scan("Script extracted from response: "+script)
         print("Logged response")
      else:
         jsonObj='{' + results.group(2) + '}'

         for item in json.loads(jsonObj)['groups'][0]['items']:
            venue    = item['venue']
            name     = venue['name']
            lat      = venue['location']['lat']
            lng      = venue['location']['lng']
            address  = venue['location']['address'] if 'address' in venue['location'] else ""
            country  = venue['location']['country'] if 'country' in venue['location'] else ""
            self.results.append((name, (lat, lng), address, country))
            self.resultsN+=1

         '''for venue in root.findall("body//div[@class='venueBlock']"):
            index   = venue.find(".//span[@class='venueIndex']").text
            name    = venue.find(".//div[@class='venueName']/a").text
            address = venue.find(".//div[@class='venueAddress']").text
            print(index, name, address)
         '''


class FoursquareRequester():
   
   logger = None

   # Returns status of response
   def __init__(self, logger):
      self.logger=logger

   def send_request(self, request, maxRetries, retryInterval):
      logger=self.logger
      
      ne = request['ne']
      sw = request['sw']
      q = request['q']

      # Send the request
      url = "https://foursquare.com/explore?mode=url" +\
            "&ne=" + str(ne[0]) + "%2C" + str(ne[1]) +\
            "&sw=" + str(sw[0]) + "%2C" + str(sw[1]) +\
            "&q=" + q
      print(url)
      try:
         return urlopen(url).read()
      except HTTPError:
         print("404: Is the link correct?")
         print("Link given was:", url)
         return None
      except URLError:
         print("Domain in URL doesn't exist")
         print("Url was:", url)
         return None
