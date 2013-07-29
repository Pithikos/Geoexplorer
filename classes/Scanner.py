from lib.google_places import *
from lib.geotools import *
from lxml import etree

from classes.GUI import *

from config import *

class Scanner:
   
   # Incapsulated objects
   limiter   = None
   scheduler = None
   GUI       = None
   
   
   # Vars
   bounds    = None    #bounds in latitude and longtitude [x, y, x2, y2]
   
   
   # ----------------------------------------------
   
   
   # GUI object (MUST)
   # Google KEY (MUST)
   def __init__(self, GUI, Gkey):
      self.GUI = GUI
      G_set_key(Gkey) # Setting passed key



   # Set outer bounds for the scanning
   def set_bounds(self, bounds):
      # Sort the bounds so that the left couple
      # is always on top and left of the right couple
      lat1=bounds[0]
      lng1=bounds[1]
      lat2=bounds[2]
      lng2=bounds[3]
      
      if (lat1<lat2) or (lng1>lng2): #swap couples
         bounds=[lat2, lng2, lat1, lng1]
         
      self.bounds=bounds
      #self.GUI.add_box(bounds[0], bounds[1], bounds[2], bounds[3])
   
   
   # Start scanning
   def start_scanning(self, tool, args):
      if not self.limiter:
         print("Scanning without limiter will not filter out any results")

      print("Distance between points is " + str(dist(self.bounds[0], self.bounds[1], self.bounds[2], self.bounds[3])))

      # Split big box in pieces with max 50000m each piece
      maxDist=config['Grules']['maxScannableDistance']
      boxes=[]
      boxes.append(self.bounds)
      
      def splitBoxIn4(coords):
         lat1=coords[0]
         lng1=coords[1]
         lat2=coords[2]
         lng2=coords[3]
         midLat=round((lat1+lat2)/2, 5)
         midLng=round((lng1+lng2)/2, 5)
         box1=[lat1, lng1, midLat, midLng]
         box2=[lat1, midLng, midLat, lng2]
         box3=[midLat, lng1, lat2, midLng]
         box4=[midLat, midLng, lat2, lng2]
         return box1, box2, box3, box4
         
      def splitBoxHorizontally(coords):
         lat1=coords[0]
         lng1=coords[1]
         lat2=coords[2]
         lng2=coords[3]
         midLat=round((lat1+lat2)/2, 5)
         box1=[lat1, lng1, midLat, lng2]
         box2=[midLat, lng1, lat2, lng2]
         return box1, box2
         
      def splitBoxVertically(coords):
         lat1=coords[0]
         lng1=coords[1]
         lat2=coords[2]
         lng2=coords[3]
         midLng=round((lng1+lng2)/2, 5)
         box1=[lat1, lng1, lat2, midLng]
         box2=[lat1, midLng, lat2, lng2]
         return box1, box2

      # See if splitting is needed     
      def existsTooBigDist():
         for box in boxes:
            x=dist(box[0], box[1], box[0], box[3])
            y=dist(box[0], box[1], box[2], box[1])
            if (x>maxDist) or (y>maxDist):
               return True
         return False
      
      # Split box in minor boxes if needed
      while(existsTooBigDist()):
         for i in range(len(boxes)):
            box=boxes[i]
            x=dist(box[0], box[1], box[0], box[3])
            y=dist(box[0], box[1], box[2], box[1])
            if (x>maxDist) and (y>maxDist):
               b1, b2, b3, b4 = splitBoxIn4(boxes[i])
               boxes.pop(i)
               boxes.append(b1)
               boxes.append(b2)
               boxes.append(b3)
               boxes.append(b4)
            elif (x>maxDist):
               b1, b2 = splitBoxVertically(boxes[i])
               boxes.pop(i)
               boxes.append(b1)
               boxes.append(b2)
            elif (y>maxDist):
               b1, b2 = splitBoxHorizontally(boxes[i])
               boxes.pop(i)
               boxes.append(b1)
               boxes.append(b2)

      # Add boxes on map
      for box in boxes:
         self.GUI.add_box(box[0], box[1], box[2], box[3], 'red')
      
      # FOR EVERY SUB-AREA IN BIG BOX
      if (tool == 'textsearch'):
         print("Textsearch: ", args)
         xml = G_textsearch(args)
         root = etree.fromstring(xml)
         
         # Get location of each result
         #print(etree.tostring(root).decode("utf-8"))
         status = root[0].text
         token  = None

         if (status == 'OK'):
            root.remove(root[0])
         else:
            return

         if (root[-1].tag == "next_page_token"):
            token=root[-1].text
            root.remove(root[-1])
   
         #DO SOMETHING WITH NEXT_TOKEN
         
         # Get locations from results
         for result in root:
            for el in result:
               if (el.tag == 'geometry'):
                  lat=el[0][0].text
                  lng=el[0][1].text
                  #self.GUI.add_marker(lat, lng)


   def stop_scanning(self):
      pass


   # ----------------- Setters ---------------------

 
   def set_scheduler(self, scheduler):
      self.scheduler=scheduler


   def set_limiter(self, limiter):
      self.limiter=limiter

   # ----------------- General ---------------------

   def show_config(self):
      print('Limiter:   ', self.limiter)
      print('Scheduler: ', self.scheduler)
      print('GUI:       ', self.GUI)
      print('Bounds:    ', self.bounds)
