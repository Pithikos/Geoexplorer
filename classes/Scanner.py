from lib.google_places import *
from lxml import etree

from classes.GUI import *
from classes.Grid import *

from config import *

from time import sleep

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
      self.GUI.add_box(bounds[0], bounds[1], bounds[2], bounds[3], "red")
      self.GUI.center_map(bounds[0], bounds[1], bounds[2], bounds[3])
      print(bounds)
   
   # ----------------------------------------------------------------------------------------------
   
   # Start scanning
   def start_scanning(self, tool, args):
      if not self.limiter:
         print("Scanning without limiter will not filter out any results")

      print("Distance between points is " + str(dist(self.bounds[0], self.bounds[1], self.bounds[2], self.bounds[3])))

      # Make a grid of scannable boxes
      grid=Grid(self.bounds) 
      self.GUI.add_grid(grid)

      # SHOW INFO
      if (tool == 'textsearch'):
         print("Textsearch: ", args)
      elif (tool == 'radarsearch'):
         print("Radarsearch: ", args)

      print(grid.boxes)
      print("Number of boxes: ", len(grid.boxes))
      # Search for each box
      for box in grid.boxes:
         sleep(3)
         print(box)
         #self.GUI.add_box(box[0], box[1], box[2], box[3], 'green')
         self.GUI.remove_box(box[0], box[1], box[2], box[3])
         print("Remove: ", box)
         # FOR EVERY SUB-AREA IN BIG BOX
         '''if (tool == 'textsearch'):
            xml = G_textsearch(args)
         elif (tool == 'radarsearch'):
            lat, lng = grid.getBoxCenter(box)
            location=str(lat)+','+str(lng)
            print("Searching at: ", location)
            print("Coords: ", box)
            xdist=grid.getBoxDistx(box)
            ydist=grid.getBoxDisty(box)
            radius=max(xdist, ydist)/2
            self.GUI.add_box(box[0], box[1], box[2], box[3], 'green')
            xml = G_radarsearch(location, radius, args)
         
         root = etree.fromstring(xml)
         
         # Get location of each result
         print(etree.tostring(root).decode("utf-8"))
         status = root[0].text
         token  = None
   
         if (status == 'OK'):
            root.remove(root[0])
         elif (status == 'ZERO_RESULTS'):
            continue
         else:
            continue
   
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
                  self.GUI.add_marker(lat, lng)
         '''

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
