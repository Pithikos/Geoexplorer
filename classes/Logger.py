import datetime

from os import remove
import os
from config import *

class Logger:
   
   scanner = None # Let's logger access all scanner's information

   fScan   = None # Keeps track of each step in the scanning process
   fStats  = None # Keeps track of google quota for each scan
   fResult = None # Makes a record of the findings from the scan


   def __init__(self, logpath, scanfile, statsfile, resultfile, scanner):
      self.scanner=scanner
      if (config['NEW_FOLDER_EACH_SCAN'] == True):
         logpath+= '/' + datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
      if not os.path.exists(logpath):
         os.makedirs(logpath)
            
      scanpath   = logpath + '/' +   scanfile
      statspath  = logpath + '/' +  statsfile
      resultpath = logpath + '/' + resultfile
      
      # Remove old files
      if os.path.isfile(scanpath):
         remove(scanpath)
      if os.path.isfile(statspath):
         remove(statspath)
      if os.path.isfile(resultpath):
         remove(resultpath)

      self.fScan=open(scanpath, "a", 1)
      self.fStats=open(statspath, "w", 1)
      self.fResult=open(resultpath, "a", 1)


   # Append text as a new line to a log file
   def append(self, type, text):
      timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      if   (type=='scan'):
         self.fScan.write(timestamp+" : "+text+"\n")
      elif (type=='result'):
         self.fResult.write(text+"\n")


   # Make Google statistics log while erasing the previous one
   def update_stats(self):
      scanner=self.scanner
      
      # Remove old file
      self.fStats.seek(0, 0)
      self.fStats.truncate()
      
      if (not scanner.scanFinishDatetime):
         finished='-'
      else:
         finished=str(scanner.scanFinishDatetime.strftime("%Y-%m-%d %H:%M:%S"))
         
      self.fStats.write("Started scanning  : "+str(scanner.scanStartDatetime.strftime("%Y-%m-%d %H:%M:%S"))+"\n")
      self.fStats.write("Finished scanning : "+finished+"\n")
      self.fStats.write("Number of grid boxes : "+str(scanner.boxesN)+"\n")
      self.fStats.write("Requests sent : "    +str(scanner.requestsTotal)+"\n")
      self.fStats.write("Quota used    : "    +str(scanner.costTotal)+"\n")
