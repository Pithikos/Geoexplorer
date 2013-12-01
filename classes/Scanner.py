from lxml import etree

from classes.GUI import *
from classes.Grid import *
from classes.Logger import *
from classes.Service import *

from config import *

from threading import Thread # Needed for Messenger
from time import sleep
import datetime

class Scanner:
   
   # Incapsulated objects
   GUI      = None
   logger   = None
   service  = None
   
   # Stats for overall scanning
   scanStartDatetime  = None
   scanFinishDatetime = None
   boxesN             = 0
   requestsTotal      = 0
   costTotal          = 0
   
   # Current box scan
   currentBox         = None

   # Vars
   bounds    = None    #bounds in latitude and longtitude [x, y, x2, y2]
   
   
   # ---------------------------------------------------------------------------
   
   
   # GUI  -> GUI object
   # Gkey -> Google key
   def __init__(self):

      # Make Messenger
      msn = Messenger('', config['GUI_PORT'])
      msn.setHandler(self.incoming_msg_handler)
      Thread(target=msn.start_server).start()
      
      # GUI
      self.GUI    = GUI(msn)
      
      # Bounds
      self.set_bounds(config['limiter']['BOUNDS'])
      print("Scanning area set to: ", self.bounds)
      
      self.logger = Logger('.'+config['LOG_PATH'],
                           config['LOG_SCAN_FILENAME'],
                           config['LOG_STATS_FILENAME'],
                           config['LOG_RESULT_FILENAME'],
                           self)


   # Set outer bounds for the scanning
   def set_bounds(self, bounds):
      # Sort the bounds so that the left couple
      # is always on top and left of the right couple
      lat1=bounds[0]
      lng1=bounds[1]
      lat2=bounds[2]
      lng2=bounds[3]
      
      if (lat1<lat2) or (lng1>lng2): #swap couples
         bounds=(lat2, lng2, lat1, lng1)
         
      self.bounds=bounds
      self.GUI.center_map(bounds[0], bounds[1], bounds[2], bounds[3])

   def set_for_each_box(self, func):
      self.for_each_box=func
      
   def set_response_handler(self, func):
      self.response_handler=func
      

   # ---------------------------------------------------------------------------


   # Handling incoming messages from GUI
   def incoming_msg_handler(self, msg):
      if (msg == "PAUSE"):
         print("Client asks to pause application")
      elif (msg == "CLOSE"):
         print("Client asks to close application")
        
               
   # ---------------------------------------------------------------------------
   

   # Start scanning
   def start_scanning(self):
      self.scanStartDatetime=datetime.datetime.now()
      logger=self.logger

      # Make a grid of scannable boxes
      grid=Grid(self.bounds) 
      self.GUI.add_grid(grid)
      self.boxesN=len(grid.boxes)
      print("Number of boxes to scan: ", self.boxesN)

      # Search for each box
      toScan=list(grid.boxes)
      consequentReqRetries=0
      while(toScan):
         box=toScan[0]
         self.currentBox=box
         sleep(config['scheduler']['NEXT_SEARCH_WAIT'])
         self.GUI.remove_box(box)
         self.GUI.add_box(box, 'green')

         markers = self.service.search(box, logger) # HERE WE SEARCH BOX

         self.requestsTotal +=1
         self.costTotal += config['costs']['PER_REQUEST']
         logger.update_stats()

         # Add marker on map
         for marker in markers:
            if (len(marker)>=2):
               self.GUI.add_marker(marker[0], marker[1])

         # Remove finished box
         toScan.pop(0)
         consequentReqRetries=0
         
      # Finish
      self.scanFinishDatetime=datetime.datetime.now()
      logger.update_stats()
      print("Scanning finished.")
      print("Press CTRL+C to stop application.")


   def stop_scanning(self):
      pass


   # ----------------- Setters ---------------------


   def set_service(self, service):
      self.service=service
