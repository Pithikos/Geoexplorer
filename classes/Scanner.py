from classes.GUI import *
from classes.Grid import *
from classes.Logger import *

from config import *

from threading import Thread # Needed for Messenger
from time import sleep
from sys import exit
from datetime import datetime, date
import copy


class Scanner:
   
   # Incapsulated objects
   GUI       = None
   logger    = None
   service   = None
   config    = None
   msnThread = None
   
   # Stats for overall scanning
   sessionStart    = None
   sessionEnd      = None
   boxesNinit      = 0
   boxesN          = 0
   requestsTotal   = 0
   resultsTotal    = 0
   costTotal       = 0
   minTimeInterval = 'INF'
   maxTimeInterval = 0
   sumIntervalsSecs = 0
   
   # Vars
   bounds    = None    #bounds in latitude and longtitude [x, y, x2, y2]
   
   
   # ---------------------------------------------------------------------------
   
   
   def __init__(self):
      
      # Load configuration file
      self.config=config

      # Make Messenger
      msn = Messenger('', self.config['GUI_PORT'])
      msn.setHandler(self.incoming_msg_handler)
      self.msnThread = Thread(target=msn.start_server)
      self.msnThread.start()
      
      # GUI
      self.GUI = GUI(msn)
      
      # Bounds
      self.set_bounds(self.config['SCANNING_AREA'])
      print("Scanning area set to: ", self.bounds)
      
      self.logger = Logger('.'+self.config['LOG_PATH'],
                           self.config['LOG_SCANNING_FILENAME'],
                           self.config['LOG_SESSION_FILENAME'],
                           self.config['LOG_RESULTS_FILENAME'],
                           self)


   # Set outer bounds for the scanning
   def set_bounds(self, bounds):
      # Sort the bounds so that the left couple
      # is always on top and left of the right couple
      lat1=bounds[0]
      lng1=bounds[1]
      lat2=bounds[2]
      lng2=bounds[3]
      
      if (lat1<lat2):
         bounds=(lat2, lng1, lat1, lng2)
         lat1cp = lat1
         lat1 = lat2
         lat2 = lat1cp
      if (lng1>lng2):
         lng1cp = lng1
         lng1 = lng2
         lng2 = lng1cp
         
      bounds=(lat1, lng1, lat2, lng2)
         
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
      self.sessionStart=datetime.now()
      logger=self.logger

      # Make a grid of scannable boxes
      grid=Grid(self.bounds, self, self.GUI) 
      self.boxesN     = len(grid.boxes)
      self.boxesNinit = len(grid.boxes)
      print("Number of boxes to scan(initially): ", self.boxesN)

      # Scan each box
      toScan=list(grid.boxes)
      boxScanStart = None
      isFirstScan    = True
      while(toScan):
         box=toScan[0]
         self.GUI.remove_box(box)
         self.GUI.add_box(box, 'yellow')

         # Timing interval between last box scan
         if isFirstScan:
            boxScanStart = datetime.now()
            isFirstScan  = False
         else:
            boxScanPrev  = copy.deepcopy(boxScanStart)
            boxScanStart = datetime.now()
            tdelta = boxScanStart - boxScanPrev
            secs   = tdelta.total_seconds()
            if (secs > self.maxTimeInterval):
               self.maxTimeInterval = secs
            if (self.minTimeInterval=='INF' or secs < self.minTimeInterval):
               self.minTimeInterval = secs
            self.sumIntervalsSecs+=secs
         waitTime = self.config['scheduler']['NEXT_SEARCH_WAIT']
         sleep(waitTime)
         
         # Scan box
         markers = self.service.search(box, logger)

         # Update costs after scan
         self.requestsTotal +=1
         self.costTotal += self.config['service']['request']['COST_PER_REQUEST']
         logger.update_session()

         # Max cost reached
         max_cost_day = self.config['service']['request']['MAX_COST_DAY']
         if max_cost_day!='INF' and self.costTotal > max_cost_day:
            print("max cost per day reached")
         
         # Autosplit
         max_results = self.config['service']['response']['MAX_RESULTS']
         if self.config['box']['AUTOSPLIT'] and max_results!='INF' and\
                                             len(markers) >= max_results:
            logger.log_scan("Response had max possible results. Autosplitting..")
            boxes=grid.splitBoxIn4(box)
            self.boxesN-=1
            toScan.pop(0)
            self.boxesN+=4
            toScan.insert(0, boxes[0])
            toScan.insert(1, boxes[1])
            toScan.insert(2, boxes[2])
            toScan.insert(3, boxes[3])
            continue

         # Add markers on map
         for marker in markers:
            if (len(marker)>=2):
               self.GUI.add_marker(marker[0], marker[1])
               self.resultsTotal+=1

         # Remove finished box
         self.GUI.remove_box(box)
         self.GUI.add_box(box, 'green')
         toScan.pop(0)

      # Finish
      self.sessionEnd=datetime.now()
      logger.update_session()
      print("Scanning finished.")
      print("Press CTRL+C to stop application.")


   def stop_scanning(self):
      pass


   # ----------------- Setters ---------------------

   # Sets the service to be used for scanning
   def set_service(self, service):
      self.service = service
      
      # Override config with service values
      rules = service.service
      if (rules):
         for subject in rules:
            for key in rules[subject]:

               # KEY required
               if subject=='authentication' and key=='REQUIRED':
                  if rules['authentication']['REQUIRED']==True and\
                        (not service.key or len(service.key)<1):
                     print("The service requires a key, but none was provided.")
                     print("Press CTRL+Z to exit.")
                     exit()
               
               # Box limits
               elif subject=='box' and (key=='MAX_X_DISTANCE' or key=='MAX_Y_DISTANCE'):
                  if self.config['box']['X_DISTANCE'] > rules['box']['MAX_X_DISTANCE']:
                     self.config['box']['X_DISTANCE'] = rules['box']['MAX_X_DISTANCE']
                  if self.config['box']['Y_DISTANCE'] > rules['box']['MAX_Y_DISTANCE']:
                     self.config['box']['Y_DISTANCE'] = rules['box']['MAX_Y_DISTANCE']

               # Min sleep between requests
               elif subject=='request' and key=='MIN_REQUEST_INTERVAL':
                  if self.config['scheduler']['NEXT_SEARCH_WAIT'] < rules['request']['MIN_REQUEST_INTERVAL']:
                     self.config['scheduler']['NEXT_SEARCH_WAIT'] = rules['request']['MIN_REQUEST_INTERVAL']
               
               # Just copy rest of options
               else:
                  self.config['service'][subject][key] = rules[subject][key]

