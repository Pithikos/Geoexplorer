from lxml import etree
from time import sleep
from threading import Thread # Needed for Messenger

import datetime

from classes.Scanner   import *
from classes.Limiter   import *
from classes.Scheduler import *
from classes.Messenger import *
import webbrowser

# Configs
pathLogs='./log'
saveFilePath='./scraped/scraped_offers_only_ordpris'+datetime.datetime.now().strftime("%Y-%m-%d_%H.%M"); #list with lan and kommun
GUI=False
browserPath="/usrfirefox"

# ---------------------------------- Messenger ---------------------------------


# Handling incoming messages
def handler(msg):
   if (msg == "PAUSE"):
      print("Client asks to pause application")
   elif (msg == "CLOSE"):
      print("Client asks to close application")


server = Messenger('', 9017)
server.setHandler(handler)
Thread(target=server.start_server).start()




# ------------------------------------ Main ------------------------------------


# Main thread
while 1:
   sleep(1)
   server.send("uno")

# Create the scanner
scanner=Scanner([58.608334, 14.392090, 58.066256, 16.259766])
scanner.show_config()

# 
scanner.start_scanning('textsearch', 'grocery in Sweden')

'''
   searchitem={"keyword": "grocery", "name": "ica", "types": "grocery_or_supermarket"};
   xml = G_radarsearch(loc, rad, searchitem)
   root = etree.fromstring(xml)
   
   #xml = G_textsearch("grocery in Sweden")
   #xml = G_radarsearch(loc, rad, {"name": "Hemköp"})
'''
