from lxml import etree
from time import sleep
from threading import Thread # Needed for Messenger

import datetime

from classes.Scanner   import *
from classes.GUI import *


# Configs
from config import *

# ---------------------------------- Messenger ---------------------------------


# Handling incoming messages from GUI
def incoming_msg_handler(msg):
   if (msg == "PAUSE"):
      print("Client asks to pause application")
   elif (msg == "CLOSE"):
      print("Client asks to close application")


# ------------------------------------ Main ------------------------------------


# Main thread
'''
while 1:
   sleep(1)
   server.send("uno")
'''

# Make Messenger
msn = Messenger('', config['GUI_PORT'])
msn.setHandler(incoming_msg_handler)
Thread(target=msn.start_server).start()

# Make GUI
GUI=GUI(msn)

# Make Scanner
scanner=Scanner(GUI)
scanner.set_bounds(config['limiter']['BOUNDS'])
print("Scanning area set to: ", scanner.bounds)

# Set service for the scanner
# ================= OWN CODE HERE ======================

searchitems={"name": "ica", "types": "grocery_or_supermarket"};
service = GoogleRadarSearch(searchitems)
scanner.set_service(service)

# ======================================================


# Start scanning
scanner.start_scanning()
