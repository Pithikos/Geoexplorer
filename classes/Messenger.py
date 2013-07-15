import select
from lib.websocket import WebSocketServer
#from time import sleep

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


# ------------------------------------------------------------------------------

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
