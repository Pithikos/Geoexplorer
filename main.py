from lxml import etree
from time import sleep
from threading import Thread # Needed for Messenger

import datetime

from classes.Scanner   import *
from classes.GUI import *
from classes.Requester import *
from classes.ResponseParser import *

import webbrowser

# Configs
from config import *

# ---------------------------------- Messenger ---------------------------------


# Handling incoming messages from GUI
def incoming_msg_handler(msg):
   if (msg == "PAUSE"):
      print("Client asks to pause application")
   elif (msg == "CLOSE"):
      print("Client asks to close application")


# ------------------------------------ Main ------------------------------------


# Main thread
'''
while 1:
   sleep(1)
   server.send("uno")
'''

# Make Messenger
msn = Messenger('', config['GUI_PORT'])
msn.setHandler(incoming_msg_handler)
Thread(target=msn.start_server).start()

# Make GUI
GUI=GUI(msn)

# Make Scanner
scanner=Scanner(GUI)
scanner.set_bounds(config['limiter']['BOUNDS'])
print("Scanning area set to: ", scanner.bounds)

# Logger
logger = scanner.logger # reference so that it can be used by user


# ----------------------------------------------------------------------
# ----------------------------- OWN CODE -------------------------------
# ----------------------------------------------------------------------





# What to do with each box
def search(box):
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
   searchitems={"name": "ica", "types": "grocery_or_supermarket"};
   req= {'location': location,
         'radius': radius,
         'searchitems': searchitems}
   googleResponse = googleRequester.send_request(req, 0, 0)
   logger.append('scan', str(box.bounds())+" : "+googleResponse.status)

   # Get the markers from the response
   markers=[]
   for result in googleResponse.results:
      markers.append(result['location'])
   logger.append("result", str(box.bounds())+" : "+str(googleResponse.resultsN))

   return markers

scanner.set_for_each_box(search)





# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

# Start scanning
scanner.start_scanning()
#scanner.start_scanning('textsearch', 'grocery in Sweden')
'''
   searchitem={"keyword": "grocery", "name": "ica", "types": "grocery_or_supermarket"};
   xml = G_radarsearch(loc, rad, searchitem)
   root = etree.fromstring(xml)
   
   #xml = G_textsearch("grocery in Sweden")
   #xml = G_radarsearch(loc, rad, {"name": "Hemköp"})
'''
