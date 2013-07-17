from lib.google_places import *
from lxml import etree

from classes.GUI import *


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
      self.bounds=bounds
   
   
   
   # Start scanning
   def start_scanning(self, tool, args):
      if not self.limiter:
         print("Scanning without limiter will not filter out any results")
      
      
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
                  self.GUI.add_marker(lat, lng)


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
