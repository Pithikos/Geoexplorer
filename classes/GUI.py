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


   def add_marker(self, lat, lng):
      self.messenger.send("draw:marker:"+lat+","+lng)


   def show_message(self, message):
      self.messenger.send(message)
