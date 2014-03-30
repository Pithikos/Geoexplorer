import _bootstrap_

from classes.Scanner import *
from classes.services.ServiceSimulation import *

#
# In this example we simulate a service for demonstration purposes.
# 
#
# For the full options for the Radar Search you can check the
# "Optional paremeters" here:
# https://developers.google.com/places/documentation/search#RadarSearchRequests
#

scanner = Scanner()
service = ServiceSimulationSearch()
scanner.set_service(service)
scanner.start_scanning()
