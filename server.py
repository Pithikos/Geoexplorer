#!/usr/bin/env python

import select
from lib.websocket import WebSocketServer
from threading import Thread
from time import sleep
import queue 

class WebSocketEcho(WebSocketServer):

    buffer_size = 8096
    cqueue=[]
    
    # Once a client connects
    def new_client(self):

        c_pend = 0
        cpartial = ""
        rlist = [self.client]
        
        while True:
            
            wlist = []
            
            sleep(2)
            print("server queue: ", self.cqueue)

            if self.cqueue or c_pend: wlist.append(self.client)
            ins, outs, excepts = select.select(rlist, wlist, [], 1)
            if excepts: raise Exception("Socket exception")

            if self.client in outs and not self.client in ins:
                # Send queued target data to the client
                c_pend = self.send_frames(self.cqueue)
                self.cqueue = []

            if self.client in ins:
                # Receive client data, decode it, and send it back
                frames, closed = self.recv_frames()
                self.cqueue.extend(frames)
                print("Received: ", self.cqueue)
                if closed:
                    self.send_close()
                    raise self.EClose(closed)
                    
    def send(self, msg):
        self.cqueue.append(bytes(msg, 'utf8'))


server = WebSocketEcho('', 9017)
Thread(target=server.start_server).start()


# Thread 1
while 1:
   sleep(1)
   server.send("uno")
   print("Added 'uno' to queue")
   print("global queue: ", server.cqueue)
