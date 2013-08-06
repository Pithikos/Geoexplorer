from lxml import etree
from time import sleep
from threading import Thread # Needed for Messenger

import datetime

from classes.Scanner   import *
from classes.Messenger import *
import webbrowser

# Configs
from config import config

# ---------------------------------- Messenger ---------------------------------


# Handling incoming messages from GUI
def handler(msg):
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
msn = Messenger('', config['GUI_port'])
msn.setHandler(handler)
Thread(target=msn.start_server).start()

# Make GUI
GUI=GUI(msn)

# Make Scanner
scanner=Scanner(GUI, config['Gkey'])
scanner.set_bounds(config['limiter']['bounds'])
scanner.show_config()

# Start scanning
searchitems={"name": "ica", "types": "grocery_or_supermarket"};
scanner.start_scanning('radarsearch', searchitems)
#scanner.start_scanning('textsearch', 'grocery in Sweden')
'''
   searchitem={"keyword": "grocery", "name": "ica", "types": "grocery_or_supermarket"};
   xml = G_radarsearch(loc, rad, searchitem)
   root = etree.fromstring(xml)
   
   #xml = G_textsearch("grocery in Sweden")
   #xml = G_radarsearch(loc, rad, {"name": "Hemköp"})
'''
