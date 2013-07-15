'''
Google Places Scanner
Author: Johan Hanssen Seferidis
Description: Use Google Places searches on big areas like countries
'''

from urllib.request import *
from google_places import *
from lxml import etree
import webbrowser

# Takes the root of the tree and gives back the status
def getStatus(root):
   return root[0].text

G_language="se"
G_region="se"

htmlFilePath="./index.html"

html='''<!DOCTYPE html>
<html>
<head>
   <meta charset="utf-8" />
   <script type="text/javascript" src="http://maps.googleapis.com/maps/api/js?libraries=places&amp;sensor=false&amp;language=se&amp;region=se">return;</script>
   <script></script>
</head>
<body>
   <div id="map"></div>
</body>
</html>'''

js='''
var initLocation = new google.maps.LatLng(58.406119,15.581703);
var map = new Map(initLocation);
'''

#def appendJs(id, code):
#   lxml.get


tree = etree.fromstring(html)
root = tree.getroottree()

#add Google Maps
script=tree[0][-1]
script.text="alert('test');"

str = etree.tostring(root, pretty_print=True).decode("utf-8")
f=open(htmlFilePath, "w")
f.write(str);
print(str)

bounds={}
bounds["lat1"]=59.400365
bounds["lng1"]=14.326172
bounds["lat2"]=57.704147
bounds["lng2"]=16.787109
