from lib.google_places import *
from lxml import etree

from classes.GUI import *
from classes.Grid import *
from classes.Logger import *

from config import *

from time import sleep
import datetime

class Scanner:
   
   # Incapsulated objects
   GUI       = None
   logger    = None
   
   # Variables
   scanStartDatetime  = None
   scanFinishDatetime = None
   GrequestsTotal     = 0
   GquotaUsed         = 0
   
   # Vars
   bounds    = None    #bounds in latitude and longtitude [x, y, x2, y2]
   
   
   # ----------------------------------------------
   
   
   # GUI object (MUST)
   # Google KEY (MUST)
   def __init__(self, GUI, Gkey):
      self.GUI = GUI
      self.logger = Logger('.'+config['log_path']+'/'+config['log_scan_filename'],
                           '.'+config['log_path']+'/'+config['log_gstics_filename'],
                           '.'+config['log_path']+'/'+config['log_result_filename'],
                           self)
      G_set_key(Gkey) # Setting passed key


   # Set outer bounds for the scanning
   def set_bounds(self, bounds):
      # Sort the bounds so that the left couple
      # is always on top and left of the right couple
      lat1=bounds[0]
      lng1=bounds[1]
      lat2=bounds[2]
      lng2=bounds[3]
      
      if (lat1<lat2) or (lng1>lng2): #swap couples
         bounds=(lat2, lng2, lat1, lng1)
         
      self.bounds=bounds
      self.GUI.add_box(bounds[0], bounds[1], bounds[2], bounds[3], "red")
      self.GUI.center_map(bounds[0], bounds[1], bounds[2], bounds[3])
      print(bounds)


   # ----------------------------------------------------------------------------------------------


   # Start scanning
   def start_scanning(self, tool, args):
      self.scanStartDatetime=datetime.datetime.now()
      logger=self.logger

      print("Distance between points is " + str(dist(self.bounds[0], self.bounds[1], self.bounds[2], self.bounds[3])))

      # Make a grid of scannable boxes
      grid=Grid(self.bounds) 
      self.GUI.add_grid(grid)
      print("Boxes to scan: ", grid.getN)

      # SHOW INFO
      if (tool == 'textsearch'):
         print("Textsearch: ", args)
      elif (tool == 'radarsearch'):
         print("Radarsearch: ", args)


      # Search for each box
      toScan=list(grid.boxes)
      consequentReqRetries=0
      while(toScan):
         box=toScan[0]
         
         sleep(config['scheduler']['next_search_wait'])
         self.GUI.remove_box(box[0], box[1], box[2], box[3])
         self.GUI.add_box(box[0], box[1], box[2], box[3], 'green')
         # FOR EVERY SUB-AREA IN BIG BOX
         if (tool == 'textsearch'):
            xml = G_textsearch(args)
         elif (tool == 'radarsearch'):
            lat, lng = grid.getBoxCenter(box)
            location=str(lat)+','+str(lng)
            print("Searching at: ", location)
            print("Coords: ", box)
            xdist=grid.getBoxDistx(box)
            ydist=grid.getBoxDisty(box)
            radius=max(xdist, ydist)/2
            self.GUI.add_box(box[0], box[1], box[2], box[3], 'green')
            #xml = G_radarsearch(location, radius, args)
            xml = '''<PlaceSearchResponse>
 <status>OK</status>
 <result>
  <name>Tetsuya's</name>
  <type>restaurant</type>
  <type>food</type>
  <type>establishment</type>
  <formatted_address>529 Kent Street, Sydney NSW, Australia</formatted_address>
  <geometry>
   <location>
    <lat>-33.8750460</lat>
    <lng>151.2052720</lng>
   </location>
  </geometry>
  <rating>4.3</rating>
  <icon>http://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png</icon>
  <reference>CnRmAAAANRC46osWIWF63JgsOdM2XGk22I0x4HxtfL9F_XWMmF3s-ayUyIwvnySqckNlMreu53OqSrX3YsffYOxQh7PYKV2KzI19EqVcBe50qBwmy_vSXoJ3L6ehFYDJTvpHhwAH3b4BFwM8spTOwjOSMeTqhhIQ3LhryZnC4k2F7nKkT9f-8RoUVBwA9UV-C8hHNZh44YkvVOxxtK0</reference>
  <id>827f1ac561d72ec25897df088199315f7cbbc8ed</id>
 </result>
 <result>
  <name>Quay</name>
  <type>cafe</type>
  <type>bar</type>
  <type>restaurant</type>
  <type>food</type>
  <type>establishment</type>
  <formatted_address>Upper Level, Overseas Passenger Terminal/5 Hickson Road, The Rocks NSW, Australia</formatted_address>
  <geometry>
   <location>
    <lat>-33.8583790</lat>
    <lng>151.2100270</lng>
   </location>
  </geometry>
  <rating>4.1</rating>
  <icon>http://maps.gstatic.com/mapfiles/place_api/icons/cafe-71.png</icon>
  <reference>CnRiAAAAeNd3Vvz1j9dvz1deiDQWd96zoKYOFMBVhXYbhbZf4A5zfHmMsolsTAH5pd_AJ2jZYOAfCG82yFJLMTMY5-C_Jnic1bsTVud_uTBnJ0JUzD5Q-p0_7_7qYTRfVqBcCKktQ8PGrQquPEl4LfgDa1j3AhIQfkhCpHR9bgfqawWNkbzpqRoUkd7Qatt_OFkX3KKa9K_fxwE2bc4</reference>
  <id>f181b872b9bc680c8966df3e5770ae9839115440</id>
 </result>
 <result>
  <name>Rockpool</name>
  <type>restaurant</type>
  <type>food</type>
  <type>establishment</type>
  <formatted_address>107 George Street, The Rocks NSW, Australia</formatted_address>
  <geometry>
   <location>
    <lat>-33.8597750</lat>
    <lng>151.2085920</lng>
   </location>
  </geometry>
  <rating>4.0</rating>
  <icon>http://maps.gstatic.com/mapfiles/place_api/icons/restaurant-71.png</icon>

<reference>CnRlAAAALuyHKpRN_oLCCfTJZ-uIA7YdJCe3zEhsSf0RZ25GnX6UhQ66gTeVJdGAyfS2bwB3XPvocWSGBfxF-De6bXC3P_Cvezr9kAEW9jBKvazwyyYZoUaZqVwuy4sGlzKOSCse5qDR7snP63sDD1bkV60OGxIQ2zfuqWNJmtiiSXeNFqSgQhoUthzNiDC86p2SIXdpcarNFXRgBLk</reference>
  <id>7beacea28938ae42bcac04faf79a607bf84409e6</id>
  <event>
    <summary>Google Maps Developer Meetup: Rockin' out with the Places API</summary>
    <event_id>7lH_gK1GphU</event_id>
    <url>https://developers.google.com/places</url>
  </event>
 </result>
 <result>
  <name>Chinatown Sydney</name>
  <type>city_hall</type>
  <type>park</type>
  <type>restaurant</type>
  <type>doctor</type>
  <type>train_station</type>
  <type>local_government_office</type>
  <type>food</type>
  <type>health</type>
  <type>establishment</type>
  <formatted_address>483 George Street, Sydney NSW, Australia</formatted_address>
  <geometry>
   <location>
    <lat>-33.8731950</lat>
    <lng>151.2063380</lng>
   </location>
  </geometry>
  <rating>7.0</rating>
 <icon>http://maps.gstatic.com/mapfiles/place_api/icons/civic_building-71.png</icon>  <reference>CnRuAAAAiC5vFoN7Y_uh9092KqN1O1KEgihp845nP1IGIj3eDOzfOT_RPdrTmCv4wrNcwMUvMfR2NhTyWd1g2W11V6HPrYlH_gXJQyohh6iHgQmDCXUESusetpMRPfob1GnBk2ylXq-oQz_85mEyqzBFFMICshIQuDEafdNuT1HpAx5suyTUeBoUWx0qvhqfUxl0F37Qae2RlLgdk0c</reference>
  <id>017049cb4e82412aaf0efbde890e82b7f2987c16</id>
 </result>
 <html_attribution>Listings by <a href="http://www.yellowpages.com.au/">Yellow Pages</a></html_attribution>
</PlaceSearchResponse>
'''
            self.GrequestsTotal+=1
            self.GquotaUsed+=config['Grules']['cost_radarsearch']
            logger.sent_google_request()
         
         root = etree.fromstring(xml)
         
         # Get location of each result
         #print(etree.tostring(root).decode("utf-8"))
         status = root[0].text
         token  = None
   
         # Log answer
         logger.append('scan', str(box)+" : "+status)
         
         # Take care of response from Google
         if (status == 'OK'):
            root.remove(root[0])
         elif (status == 'ZERO_RESULTS'):
            print("Zero results for box: ", box)
            continue
         elif (status == 'OVER_QUERY_LIMIT'):
            if (consequentReqRetries == 4):
               print("Query limit exceeded for today. Scanning stopped.")
               break
            print("Query limit exceeded. Will wait a bit and retry.")
            sleep(config['scheduler']['on_query_limit_wait'])
            consequentReqRetries+=1
            continue
         elif (status == 'INVALID_REQUEST'):
            print("Invalid request for box: ", box)
            continue
         else:
            print("Error for box: ", box)
            print("Page received from Google: ", etree.tostring(root).decode("utf-8"))
            break
   
         if (root[-1].tag == "next_page_token"):
            token=root[-1].text
            root.remove(root[-1])
            print("Received a token for box: ", box)
            
         #DO SOMETHING WITH NEXT_TOKEN
         
         # Get locations from results
         resultsN = int(root.xpath('count(//result)'))
         self.logger.append('result', str(box)+" : "+str(resultsN))

         for result in root:
            for el in result:
               if (el.tag == 'geometry'):
                  lat=el[0][0].text
                  lng=el[0][1].text
                  self.GUI.add_marker(lat, lng)
                  
         # Remove finished box
         toScan.pop(0)
         consequentReqRetries=0
         
      # Finish
      self.scanFinishDatetime=datetime.datetime.now()
      print("Scanning finished.")
      logger.finished_scanning()

   def stop_scanning(self):
      pass


   # ----------------- Setters ---------------------

 
   def set_scheduler(self, scheduler):
      self.scheduler=scheduler


   def set_limiter(self, limiter):
      self.limiter=limiter

   # ----------------- General ---------------------

   def show_config(self):
      print('GUI:       ', self.GUI)
      print('Bounds:    ', self.bounds)
