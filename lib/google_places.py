'''
Google Places wrapper for Python3
Author: Johan Hanssen Seferidis
Description: This wrapper is lightweight and minimal. It supports RadarSearch,
TextSearch, Search and Details requests

NOTES: For usage, check the README

'''

from urllib.request import *
from urllib.parse import *

# ---------------------------------- Configs -----------------------------------

G_API_key=None;
G_base="https://maps.googleapis.com/maps/api/place/";
G_sensor="false";


# ---------------------------------- Actions -----------------------------------

def G_set_key(newkey):
   global G_API_key
   G_API_key=newkey

def G_sendRequest(url):
   try:
      response=urlopen(url)
      doc=response.read()
      return doc
   except HTTPError:
      print("404: Is the link correct?")
      return None
   except URLError:
      print("Domain in URL doesn't exist")
      return None


# ------------------------------- Make Requests --------------------------------


# Search by text query
def G_make_textsearch_req(query):
   url = G_base + "textsearch/xml?"
   url+= "&query=" + quote(query.replace(" ", "+"))
   url+= "&sensor=" + G_sensor
   url+= "&key=" + G_API_key
   return url


# Search in radius of a location
def G_make_radarsearch_req(location, radius, searchitems):
   url = G_base + "radarsearch/xml?"
   url+= "location=" + location
   url+= "&radius=" + str(radius)
   try:
      url+="&keyword="+ quote(searchitems["keyword"])
   except:
      pass
   try:
      url+="&name=" + quote(searchitems["name"])
   except:
      pass
   try:
      url+="&types=" + quote(searchitems["types"])
   except:
      pass
   url+= "&sensor=" + G_sensor
   url+= "&key=" + G_API_key
   return url


# Search in radius of a location
def G_make_search_req(location, radius, searchitems):
   url = G_base + "search/xml?"
   url+= "location=" + location
   url+= "&radius=" + str(radius)
   try:
      url+="&keyword="+ quote(searchitems["keyword"])
   except:
      pass
   try:
      url+="&name=" + quote(searchitems["name"])
   except:
      pass
   try:
      url+="&types=" + quote(searchitems["types"])
   except:
      pass
   url+= "&sensor=" + G_sensor
   url+= "&key=" + G_API_key
   return url


# Get details for an establishment or other interest location
def G_make_details_req(reference):
   url = G_base + "details/xml?"
   url+= "&reference="+ reference
   url+= "&sensor=" + G_sensor
   url+= "&key=" + G_API_key
   return url


# ------------------------------- Google Places --------------------------------


# Search by text query
def G_textsearch(query):
   url = G_make_textsearch_req(query)
   return G_sendRequest(url)


# Search by using google's radar search
def G_radarsearch(location, radius, searchitems):
   url = G_make_radarsearch_req(location, radius, searchitems)
   return G_sendRequest(url)


# Search in radius of a location
def G_search(location, radius, searchitems):
   url = G_make_search_req(location, radius, searchitems)
   return G_sendRequest(url)


# Get details for an establishment or location of interest
def G_details(reference):
   url = G_make_details_req(reference)
   return G_sendRequest(url)
