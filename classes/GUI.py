class GUI:


   messenger = None


   def __init__(self, messenger):
      self.messenger=messenger


   def init_index():
      pass


   def draw_box(self, bounds):
      #Send message to socket
      #messenger.send("draw:box:"+bounds)
      pass


   def add_marker(self, coords):
      #Send message to socket
      #messenger.send("draw:marker:"+position)
      print(position)


   def show_message(self, message):
      self.messenger.send(message)
