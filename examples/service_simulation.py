import _bootstrap_

from classes.Scanner import *
from classes.services.ServiceSimulation import *

#
# In this example we simulate a service for demonstration purposes.
# 
# The simulated service will generate random markers for the area being searched.
#

scanner = Scanner()
service = ServiceSimulationSearch()
scanner.set_service(service)
scanner.start_scanning()
