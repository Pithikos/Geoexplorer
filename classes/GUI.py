class GUI:


   messenger = None


   def __init__(self, messenger):
      self.messenger=messenger


   def init_index():
      pass


   def add_box(self, lat1, lng1, lat2, lng2, color):
      colorhex='#000000'
      if (color=='red'):
         colorhex='#FF0000'
      elif (color=='green'):
         colorhex='#00FF00'
      self.messenger.send("draw:box:"+str(lat1)+","+str(lng1)+","+str(lat2)+","+str(lng2)+","+colorhex)


   def remove_box(self, lat1, lng1, lat2, lng2):
      self.messenger.send("remove:box:"+str(lat1)+","+str(lng1)+","+str(lat2)+","+str(lng2))


   def add_marker(self, lat, lng):
      self.messenger.send("draw:marker:"+lat+","+lng)


   def center_map(self, lat, lng, lat2, lng2):
      self.messenger.send("change:view:"+str(lat)+","+str(lng)+","+str(lat2)+","+str(lng2))


   def show_message(self, message):
      self.messenger.send(message)


   def add_grid(self, grid):
      for box in grid.boxes:
         self.add_box(box[0], box[1], box[2], box[3], 'red')
