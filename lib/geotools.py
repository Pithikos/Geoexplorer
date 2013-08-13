from math import radians, sqrt, sin, cos, atan2

from lxml import etree       # used for nominatim.openstreetmap
from urllib.request import * # used for nominatim.openstreetmap


# Get distance between two points
# Returns distance in meters
def dist(lat1, lon1, lat2, lon2):
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon1 - lon2

    #EARTH_R = 6372.8
    EARTH_R = 6378.2 #close to Google's numbers

    y = sqrt(
        (cos(lat2) * sin(dlon)) ** 2
        + (cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dlon)) ** 2
        )
    x = sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(dlon)
    c = atan2(y, x)
    return EARTH_R * c * 1000


def middleLat(lat1, lat2):
   return round((lat1+lat2)/2, 5)


def middleLng(lng1, lng2):
   return round((lng1+lng2)/2, 5)


# Returns the country code at given coordinates
def getCountryCode(lat, lng):
   req="http://nominatim.openstreetmap.org/reverse?format=xml&lat="+str(lat)+"&lon="+str(lng)+"&zoom=5"
   try:
      response=urlopen(req)
      xml=response.read()
      root = etree.fromstring(xml)
      #print(etree.tostring(root).decode("utf-8"))
      tags = root.findall('.//country_code')
      if (tags):
         return tags[0].text
      else:
         return 'UNKNOWN'
   except HTTPError:
      print("404: Is the link correct?")
      return None
   except URLError:
      print("Domain in URL doesn't exist")
      return None
