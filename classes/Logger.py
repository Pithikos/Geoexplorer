import datetime

import os
from config import *

class Logger:
   
   scanner = None # Let's logger access all scanner's information

   fScan   = None # Keeps info about each box scan
   fStats  = None # Keeps info about the scanning session
   fResult = None # Keeps info about each single result
   
   resultPath = None # Path used for result log

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
         os.remove(scanpath)
      if os.path.isfile(statspath):
         os.remove(statspath)
      if os.path.isfile(resultpath):
         os.remove(resultpath)

      self.fScan   = open(scanpath,   "a", 1)
      self.fStats  = open(statspath,  "w", 1)
      self.fResult = open(resultpath, "a", 1)
         
      self.resultPath = resultpath

   # Append text as a new line to a log file
   def append(self, type, text):
      timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      if   (type=='scan'):
         self.fScan.write(timestamp+" : "+text+"\n")
      elif (type=='result'):
         if text not in open(self.resultPath).read(): # ¤This might become a hog for huge files
            self.fResult.write(text+"\n")


   # Append a new result to the results log file
   def log_result(self, line):
      self.append("result", line);


   # Append a new result to the results log file
   def log_scan(self, line):
      self.append("scan", line);
      

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
      self.fStats.write("Number of grid boxes initially : "+str(scanner.boxesNinit)+"\n")
      self.fStats.write("Number of grid boxes in the end : "+str(scanner.boxesN)+"\n")
      self.fStats.write("Requests sent : "    +str(scanner.requestsTotal)+"\n")
      self.fStats.write("Quota used    : "    +str(scanner.costTotal)+"\n")
