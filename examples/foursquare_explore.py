import _bootstrap_
from classes.Scanner import *
from classes.services.FoursquareExplore import *

#
# In this example we will use the foursquare.com website to look for restaurants.
# Foursquare.com lets you search for specific types of stores on the whole globe.
#

scanner = Scanner()
service = FoursquareSearch("restaurant")
scanner.set_service(service)
scanner.start_scanning()
