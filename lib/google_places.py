'''
Google Places wrapper for Python3
Author: Johan Hanssen Seferidis
Description: This wrapper is lightweight and minimal. It supports RadarSearch,
TextSearch, Search and Details requests

A key should be provided for each search
'''

from urllib.request import *
from urllib.parse import *


# ---------------------------------- Actions -----------------------------------


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
def G_make_textsearch_req(query, key):
   G_base = "https://maps.googleapis.com/maps/api/place/"
   url = G_base + "textsearch/xml?"
   url+= "&query=" + quote(query.replace(" ", "+"))
   url+= "&sensor=" +"false"
   url+= "&key=" + key
   return url


# Search in radius of a location
def G_make_radarsearch_req(location, radius, searchitems, key):
   G_base = "https://maps.googleapis.com/maps/api/place/"
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
   url+= "&sensor=" + "false"
   url+= "&key=" + key
   return url


# Search in radius of a location
def G_make_search_req(location, radius, searchitems, key):
   G_base = "https://maps.googleapis.com/maps/api/place/"
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
   url+= "&sensor=" + "false"
   url+= "&key=" + key
   return url


# Get details for an establishment or other interest location
def G_make_details_req(reference, key):
   G_base = "https://maps.googleapis.com/maps/api/place/"
   url = G_base + "details/xml?"
   url+= "&reference="+ reference
   url+= "&sensor=" + "false"
   url+= "&key=" + key
   return url


# ------------------------------- Google Places --------------------------------


# Search by text query
def G_textsearch(query, key):
   url = G_make_textsearch_req(query, key)
   return G_sendRequest(url)


# Search by using google's radar search
def G_radarsearch(location, radius, searchitems, key):
   url = G_make_radarsearch_req(location, radius, searchitems, key)
   return G_sendRequest(url)


# Search in radius of a location
def G_search(location, radius, searchitems, sensor, key):
   url = G_make_search_req(location, radius, searchitems, key)
   return G_sendRequest(url)


# Get details for an establishment or location of interest
def G_details(reference, sensor, key):
   url = G_make_details_req(reference, key)
   return G_sendRequest(url)
