from lib.geotools import *
from lib.google_places import *

from config import *


# Grid is made out of box instances
class Grid:

   boxes=[]
   maxBoxX=config['box']['MAX_X_DISTANCE']
   maxBoxY=config['box']['MAX_Y_DISTANCE']

   # Creates a rectangle grid between two points
   def __init__(self, bounds):
      box=Box(bounds)
      self.boxes.append(box)
      
      # Split grid into smaller boxes if needed
      while(self.existsTooBigBox()):
         for i in range(len(self.boxes)):
            box=self.boxes[i]
            if (box.xMeters>self.maxBoxX) and (box.yMeters>self.maxBoxY):
               b1, b2, b3, b4 = self.splitBoxIn4(self.boxes[i])
               self.boxes.pop(i)
               self.boxes.extend((b1, b2, b3, b4))
            elif (box.xMeters>self.maxBoxX):
               b1, b2 = self.splitBoxVertically(self.boxes[i])
               self.boxes.pop(i)
               self.boxes.extend((b1, b2))
            elif (box.yMeters>self.maxBoxY):
               b1, b2 = self.splitBoxHorizontally(self.boxes[i])
               self.boxes.pop(i)
               self.boxes.extend((b1, b2))

      # Sort boxes
      self.sortBoxes()


   def getBoxCenter(self, box):
      pass

   # Split a box into 4 equal boxes
   def splitBoxIn4(self, box):
      lat1=box.WN[0]
      lng1=box.WN[1]
      lat2=box.SE[0]
      lng2=box.SE[1]
      midLat=middleLat(lat1, lat2)
      midLng=middleLng(lng1, lng2)
      box1=(lat1, lng1, midLat, midLng)
      box2=(lat1, midLng, midLat, lng2)
      box3=(midLat, lng1, lat2, midLng)
      box4=(midLat, midLng, lat2, lng2)
      return Box(box1), Box(box2), Box(box3), Box(box4)


   # Split a box horizontally in two equal boxes
   def splitBoxHorizontally(self, box):
      lat1=box.WN[0]
      lng1=box.WN[1]
      lat2=box.SE[0]
      lng2=box.SE[1]
      midLat=round((lat1+lat2)/2, 5)
      box1=(lat1, lng1, midLat, lng2)
      box2=(midLat, lng1, lat2, lng2)
      return Box(box1), Box(box2)


   # Split a box vertically in two equal boxes
   def splitBoxVertically(self, box):
      lat1=box.WN[0]
      lng1=box.WN[1]
      lat2=box.SE[0]
      lng2=box.SE[1]
      midLng=round((lng1+lng2)/2, 5)
      box1=(lat1, lng1, lat2, midLng)
      box2=(lat1, midLng, lat2, lng2)
      return Box(box1), Box(box2)


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
