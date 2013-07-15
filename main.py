from lxml import etree
from time import sleep

import datetime

from classes.Scanner   import *
from classes.Limiter   import *
from classes.Scheduler import *
import webbrowser

# Configs
pathLogs='./log'
saveFilePath='./scraped/scraped_offers_only_ordpris'+datetime.datetime.now().strftime("%Y-%m-%d_%H.%M"); #list with lan and kommun
GUI=False
browserPath="/usrfirefox"

# ---------------------------------- Generic -----------------------------------

'''
   searchitem={"keyword": "grocery", "name": "ica", "types": "grocery_or_supermarket"};
   xml = G_radarsearch(loc, rad, searchitem)
   root = etree.fromstring(xml)
   
   #xml = G_textsearch("grocery in Sweden")
   #xml = G_radarsearch(loc, rad, {"name": "Hemköp"})
'''

# Create the scanner
scanner=Scanner([58.608334, 14.392090, 58.066256, 16.259766])
scanner.show_config()

# 
scanner.start_scanning('textsearch', 'grocery in Sweden')
