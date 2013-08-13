import select
from lib.websocket import WebSocketServer

# GUI is the outmost layer that the scanner has access to
class GUI:

   messenger = None

   def __init__(self, messenger):
      self.messenger=messenger


   def init_index():
      pass


   def add_box(self, box, color):
      lat1=box.WN[0]
      lng1=box.WN[1]
      lat2=box.SE[0]
      lng2=box.SE[1]
      colorhex='#000000'
      if (color=='red'):
         colorhex='#FF0000'
      elif (color=='green'):
         colorhex='#00FF00'
      self.messenger.send("draw:box:"+str(lat1)+","+str(lng1)+","+str(lat2)+","+str(lng2)+","+colorhex)


   def remove_box(self, box):
      lat1=box.WN[0]
      lng1=box.WN[1]
      lat2=box.SE[0]
      lng2=box.SE[1]
      self.messenger.send("remove:box:"+str(lat1)+","+str(lng1)+","+str(lat2)+","+str(lng2))


   def add_marker(self, lat, lng):
      self.messenger.send("draw:marker:"+str(lat)+","+str(lng))


   def center_map(self, lat, lng, lat2, lng2):
      self.messenger.send("change:view:"+str(lat)+","+str(lng)+","+str(lat2)+","+str(lng2))


   def show_message(self, message):
      self.messenger.send(message)


   def add_grid(self, grid):
      for box in grid.boxes:
         self.add_box(box, 'red')
         
         
# Used by the GUI class
class Messenger(WebSocketServer):

    buffer_size = 8096
    queueOut=[]
    handler=None
    
    # Once a client connects
    def new_client(self):

        c_pend = 0
        cpartial = ""
        rlist = [self.client]
        
        while True:
            
            wlist = []

            if self.queueOut or c_pend: wlist.append(self.client)
            ins, outs, excepts = select.select(rlist, wlist, [], 1)
            if excepts: raise Exception("Socket exception")

            # Sending
            if self.client in outs and not self.client in ins:
                c_pend = self.send_frames(self.queueOut)
                self.queueOut = []
            
            # Receiving
            if self.client in ins:
                frames, closed = self.recv_frames()
                self.handler(frames[0].decode('utf8'))
                if closed:
                    self.send_close()
                    raise self.EClose(closed)
            
    # Sends a message to client
    def send(self, msg):
        self.queueOut.append(bytes(msg, 'utf8'))

    # Sets a handler for incoming messages
    def setHandler(self, handler):
        self.handler=handler

# WORKING EXAMPLE (needs to import time)
'''
# Handling incoming messages
def handler(msg):
   if (msg == "PAUSE"):
      print("Client asks to pause application")
   elif (msg == "CLOSE"):
      print("Client asks to close application")

server = Messenger('', 9017)
server.setHandler(handler)
Thread(target=server.start_server).start()


# Main thread
while 1:
   sleep(1)
   server.send("uno")
'''

# ------------------------------------------------------------------------------
