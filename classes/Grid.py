from lib.geotools import *

# Grid is made out of box instances
class Grid:
   
   
   # GUI is used to reflect changes made on the grid
   GUI = None
   
   boxes=[]
   maxBoxX = None
   maxBoxY = None 



   # Creates a rectangle grid between two points
   def __init__(self, bounds, scanner, GUI):

      self.GUI = GUI
      self.maxBoxX = scanner.config['box']['X_DISTANCE']
      self.maxBoxY = scanner.config['box']['Y_DISTANCE']
      self.boxes.append(Box(bounds))
      self.GUI.add_boxes(self.boxes, 'red')
      
      # Split grid into smaller boxes if needed
      while(self.existsTooBigBox()):
         for box in self.boxes:
            if (box.xMeters>self.maxBoxX) and (box.yMeters>self.maxBoxY):
               self.splitBoxIn4(box)
            elif (box.xMeters>self.maxBoxX):
               self.splitBoxVertically(box)
            elif (box.yMeters>self.maxBoxY):
               self.splitBoxHorizontally(box)
      
      # Sort boxes
      self.sortBoxes()



   # Split a box into 4 equal boxes (in place)
   def splitBoxIn4(self, box):
      lat1=box.WN[0]
      lng1=box.WN[1]
      lat2=box.SE[0]
      lng2=box.SE[1]
      midLat=middleLat(lat1, lat2)
      midLng=middleLng(lng1, lng2)
      b1=Box((lat1, lng1, midLat, midLng))
      b2=Box((lat1, midLng, midLat, lng2))
      b3=Box((midLat, lng1, lat2, midLng))
      b4=Box((midLat, midLng, lat2, lng2))
      boxes = [b1, b2, b3, b4]
      oldbox = self.boxes.pop(self.boxes.index(box))
      self.boxes.extend(boxes)
      
      # GUI
      self.GUI.remove_box(oldbox)
      self.GUI.add_boxes(boxes, 'red')

      return boxes
      

   # Split a box horizontally in two equal boxes (in place)
   def splitBoxHorizontally(self, box):
      lat1=box.WN[0]
      lng1=box.WN[1]
      lat2=box.SE[0]
      lng2=box.SE[1]
      midLat=round((lat1+lat2)/2, 5)
      b1=Box((lat1, lng1, midLat, lng2))
      b2=Box((midLat, lng1, lat2, lng2))
      boxes=[b1, b2]
      oldbox = self.boxes.pop(self.boxes.index(box))
      self.boxes.extend(boxes)
      
      # GUI
      self.GUI.remove_box(oldbox)
      self.GUI.add_boxes(boxes, 'red')
      
      return boxes



   # Split a box vertically in two equal boxes (in place)
   def splitBoxVertically(self, box):
      lat1=box.WN[0]
      lng1=box.WN[1]
      lat2=box.SE[0]
      lng2=box.SE[1]
      midLng=round((lng1+lng2)/2, 5)
      b1=Box((lat1, lng1, lat2, midLng))
      b2=Box((lat1, midLng, lat2, lng2))
      boxes=[b1, b2]
      oldbox = self.boxes.pop(self.boxes.index(box))
      self.boxes.extend(boxes)
      
      # GUI
      self.GUI.remove_box(oldbox)
      self.GUI.add_boxes(boxes, 'red')

      return boxes



   # See if box has x or y bigger than limit
   def existsTooBigBox(self):
      for box in self.boxes:
         if (box.xMeters>self.maxBoxX) or (box.yMeters>self.maxBoxY):
            return True
      return False


   # Sort boxes in style 1:
   # 1 2 3
   # 4 5 6
   # 7 8 ..
   def sortBoxes(self):
      self.boxes=sorted(self.boxes, key=lambda x: x.WN[1])#by lng
      self.boxes=sorted(self.boxes, key=lambda x: x.WN[0], reverse=True)#by lat




# --------------------------------- public API ---------------------------------



'''
WN  N  NE
W   c   E
WS  S  SE
yMeters
xMeters
'''
# Box is a rectangle or square, part of the grid
class Box:
   
   N  = None
   E  = None
   S  = None
   W  = None
   
   center = None
   
   WN = None
   NE = None
   WS = None
   SE = None
   
   xMeters  = None
   yMeters  = None
   
   # Creates a rectangle grid between two points
   def __init__(self, bounds):

      self.WN = (bounds[0], bounds[1])
      self.NE = (bounds[0], bounds[3])
      self.SE = (bounds[2], bounds[3])
      self.WS = (bounds[2], bounds[1])
      
      midLat=middleLat(bounds[0], bounds[2])
      midLng=middleLng(bounds[1], bounds[3])
      self.N  = (bounds[0], midLng)
      self.E  = (midLat, bounds[3])
      self.S  = (bounds[2], midLng)
      self.W  = (midLat, bounds[1])
      
      self.center=(midLat, midLng)
      
      self.xMeters=dist(bounds[0], bounds[1], bounds[0], bounds[3])
      self.yMeters=dist(bounds[0], bounds[1], bounds[2], bounds[1])

   def bounds(self):
      return self.WN[0], self.WN[1], self.SE[0], self.SE[1]

   def length_lat(self):
      return abs(self.WN[0]-self.SE[0])
      
   def length_lng(self):
      return abs(self.WN[1]-self.SE[1])
