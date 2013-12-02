import _bootstrap_
from classes.Scanner import *

#
# In this example we will use the google radar search service
# to look for all groceries or supermarkets with the name "ICA".
# 
#
# For the full options for the Radar Search you can check the
# "Optional paremeters" here:
# https://developers.google.com/places/documentation/search#RadarSearchRequests
#

scanner = Scanner()
searchitems={"name": "ica", "types": "grocery_or_supermarket"};
key="" # Insert your Google key here
service = GoogleRadarSearch(key, searchitems)
service.override_config(scanner)
scanner.set_service(service)
scanner.start_scanning()
