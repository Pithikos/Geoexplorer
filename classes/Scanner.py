from lib.google_places import *
from lxml import etree

from classes.GUI import *


class Scanner:
   
   # Incapsulated objects
   limiter   = None
   scheduler = None
   GUI       = None
   
   current_loc = None
   
   
   # Vars
   bounds    = None    #bounds in latitude and longtitude [x, y, x2, y2]
   
   
   def __init__(self, bounds):
      self.bounds=bounds
      self.GUI = GUI()


   def start_scanning(self, tool, args):
      if not self.limiter:
         print("Scanning without limiter will not filter out any results")
      
      # FOR EVERY SUB-AREA IN BIG BOX
      if (tool == 'textsearch'):
         print("Textsearch: ", args)
         loc="58.4,15.58"
         rad= 10000
         xml = G_textsearch(args)
         root = etree.fromstring(xml)
         
     # Get location of each result
      #while root
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
      for child in root:
         print(child.tag)

      # SEND EVERY POSITION TO GUI
      self.GUI.add_marker(loc)


   def stop_scanning(self):
      pass
      
      
   def set_scheduler(self, scheduler):
      self.scheduler=scheduler
      
      
   def set_limiter(self, limiter):
      self.limiter=limiter
      
      
   def show_config(self):
      print('Limiter:   ', self.limiter)
      print('Scheduler: ', self.scheduler)
      print('Bounds:    ', self.bounds)
