from lib.geotools import *
from lib.google_places import *

from config import *

class Grid:

   '''
   Grid is made out of boxes of type [lat, lng, lat2, lng2]
   '''
   boxes=[]
   maxDist=config['Grules']['maxScannableDistance']


   # Creates a rectangle grid between two points
   def __init__(self, bounds):
      lat1=bounds[0]
      lng1=bounds[1]
      lat2=bounds[2]
      lng2=bounds[3]
      self.boxes.append(bounds)
      
      # Split grid into smaller boxes if needed
      while(self.existsTooBigBox()):
         for i in range(len(self.boxes)):
            box=self.boxes[i]
            x=dist(box[0], box[1], box[0], box[3])
            y=dist(box[0], box[1], box[2], box[1])
            if (x>self.maxDist) and (y>self.maxDist):
               b1, b2, b3, b4 = self.splitBoxIn4(self.boxes[i])
               self.boxes.pop(i)
               self.boxes.extend((b1, b2, b3, b4))
            elif (x>self.maxDist):
               b1, b2 = self.splitBoxVertically(self.boxes[i])
               self.boxes.pop(i)
               self.boxes.extend((b1, b2))
            elif (y>self.maxDist):
               b1, b2 = self.splitBoxHorizontally(self.boxes[i])
               self.boxes.pop(i)
               self.boxes.extend((b1, b2))

      # Sort boxes
      self.sort1Boxes()


   def getBoxCenter(self, box):
      latCenter=middleLat(box[0],box[2])
      lngCenter=middleLng(box[1],box[3])
      return latCenter, lngCenter

   #Returns distance of box of x-axis in meters
   def getBoxDistx(self, box):
      return dist(box[0], box[1], box[0], box[3])

   #Returns distance of box of x-axis in meters
   def getBoxDisty(self, box):
      return dist(box[0], box[1], box[2], box[1])
   
   # Split a box into 4 equal boxes
   def splitBoxIn4(self, coords):
      lat1=coords[0]
      lng1=coords[1]
      lat2=coords[2]
      lng2=coords[3]
      midLat=middleLat(lat1, lat2)
      midLng=middleLng(lng1, lng2)
      box1=(lat1, lng1, midLat, midLng)
      box2=(lat1, midLng, midLat, lng2)
      box3=(midLat, lng1, lat2, midLng)
      box4=(midLat, midLng, lat2, lng2)
      return box1, box2, box3, box4


   # Split a box horizontally in two equal boxes
   def splitBoxHorizontally(self, coords):
      lat1=coords[0]
      lng1=coords[1]
      lat2=coords[2]
      lng2=coords[3]
      midLat=round((lat1+lat2)/2, 5)
      box1=(lat1, lng1, midLat, lng2)
      box2=(midLat, lng1, lat2, lng2)
      return box1, box2


   # Split a box vertically in two equal boxes
   def splitBoxVertically(self, coords):
      lat1=coords[0]
      lng1=coords[1]
      lat2=coords[2]
      lng2=coords[3]
      midLng=round((lng1+lng2)/2, 5)
      box1=(lat1, lng1, lat2, midLng)
      box2=(lat1, midLng, lat2, lng2)
      return box1, box2


   # See if box has x or y bigger than limit
   def existsTooBigBox(self):
      for box in self.boxes:
         x=dist(box[0], box[1], box[0], box[3])
         y=dist(box[0], box[1], box[2], box[1])
         if (x>self.maxDist) or (y>self.maxDist):
            return True
      return False


   # Sort boxes in style 1:
   # 1 2 3
   # 4 5 6
   # 7 8 ..
   def sort1Boxes(self):
      self.boxes=sorted(self.boxes, key=lambda x: x[1])#by lng
      self.boxes=sorted(self.boxes, key=lambda x: x[0], reverse=True)#by lat


   # Sort boxes in style 2:
   # 7 8 ..
   # 4 5 6
   # 1 2 3
   def sort2Boxes(self):
      self.boxes=sorted(self.boxes)
