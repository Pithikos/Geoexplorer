import datetime

import os
from config import *

class Logger:
   
   scanner = None # Let's logger access all scanner's information

   fScanning = None # Keeps info about each box scans
   fSession  = None # Keeps info about the scansning session
   fResults  = None # Keeps info about each single results
   
   resultsPath = None # Path used for results log

   def __init__(self, logpath, scansfile, sessionfile, resultsfile, scanner):
      self.scanner=scanner
      if (config['NEW_FOLDER_EACH_SESSION'] == True):
         logpath+= '/' + datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
      if not os.path.exists(logpath):
         os.makedirs(logpath)
            
      scanspath   = logpath + '/' +   scansfile
      sessionpath  = logpath + '/' +  sessionfile
      resultspath = logpath + '/' + resultsfile
      
      # Remove old files
      if os.path.isfile(scanspath):
         os.remove(scanspath)
      if os.path.isfile(sessionpath):
         os.remove(sessionpath)
      if os.path.isfile(resultspath):
         os.remove(resultspath)

      self.fScanning   = open(scanspath,   "a", 1)
      self.fSession  = open(sessionpath,  "w", 1)
      self.fResults = open(resultspath, "a", 1)
         
      self.resultsPath = resultspath

   # Append text as a new line to a log file
   def append(self, type, text):
      timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      if   (type=='scanning'):
         self.fScanning.write(timestamp+" : "+text+"\n")
      elif (type=='results'):
         if text not in open(self.resultsPath).read(): # ¤This might become a hog for huge files
            self.fResults.write(text+"\n")


   # Append a new results to the resultss log file
   def log_result(self, line):
      self.append("results", line);


   # Append a new results to the resultss log file
   def log_scan(self, line):
      self.append("scanning", line);
      

   # Make Google statistics log while erasing the previous one
   def update_session(self):
      scanner=self.scanner
      
      # Remove old file
      self.fSession.seek(0, 0)
      self.fSession.truncate()
      
      if (not scanner.sessionEnd):
         finished='-'
      else:
         finished=str(scanner.sessionEnd.strftime("%Y-%m-%d %H:%M:%S"))
         
      self.fSession.write("Started scanning  : "+str(scanner.sessionStart.strftime("%Y-%m-%d %H:%M:%S"))+"\n")
      self.fSession.write("Finished scanning : "+finished+"\n")
      self.fSession.write("Number of grid boxes initially : "+str(scanner.boxesNinit)+"\n")
      self.fSession.write("Number of grid boxes in the end : "+str(scanner.boxesN)+"\n")
      self.fSession.write("Total requests sent : "    +str(scanner.requestsTotal)+"\n")
      self.fSession.write("Quota used          : "    +str(scanner.costTotal)+"\n")
