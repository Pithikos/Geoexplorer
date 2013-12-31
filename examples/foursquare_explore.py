import _bootstrap_
from classes.Scanner import *
from classes.services.FoursquareExplore import *

#
# In this example we will use the foursquare.com website.
# Foursquare.com lets you search for specific types of store on the whole globe.
#

scanner = Scanner()
service = FoursquareSearch("grocery")
service.override_config(scanner)
scanner.set_service(service)
scanner.start_scanning()
