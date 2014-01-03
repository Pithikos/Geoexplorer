from datetime import datetime
import os

class Logger:
   
   scanner = None # Let's logger access all scanner's information

   fScanning = None # Keeps info about each box scans
   fSession  = None # Keeps info about the scansning session
   fResults  = None # Keeps info about each single results
   
   resultsPath = None # Path used for results log

   def __init__(self, logpath, scansfile, sessionfile, resultsfile, scanner):
      self.scanner=scanner
      if (scanner.config['NEW_FOLDER_EACH_SESSION'] == True):
         logpath+= '/' + datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
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
      timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
      
      # Time elapsed
      started = str(scanner.sessionStart.strftime("%Y-%m-%d %H:%M:%S"))
      if (not scanner.sessionEnd):
         finished='-'
         timeElapsed = datetime.now() - scanner.sessionStart
      else:
         finished=str(scanner.sessionEnd.strftime("%Y-%m-%d %H:%M:%S"))
         timeElapsed = scanner.sessionEnd - scanner.sessionStart
      
      # Statistics
      if scanner.requestsTotal > 1:
         avgInterval = scanner.sumIntervalsSecs/(scanner.requestsTotal-1)
      else:
         avgInterval = scanner.sumIntervalsSecs
      
      
      
      self.fSession.write("============ Session information ============\n\n")
      self.fSession.write("Started scanning  : "+started +"\n")
      self.fSession.write("Finished scanning : "+finished+"\n")
      self.fSession.write("Time elapsed      : "+str(timeElapsed)+"\n")
      self.fSession.write("\n\n")
      self.fSession.write("----------------- Grid boxes -----------------\n")
      self.fSession.write("Number of boxes initially: "+str(scanner.boxesNinit)+"\n")
      self.fSession.write("Number of boxes in the end: "+str(scanner.boxesN)+"\n")
      self.fSession.write("Quota used         : "+str(scanner.costTotal)+"\n")
      self.fSession.write("\n\n")
      self.fSession.write("------------------ Requests ------------------\n")
      self.fSession.write("Total requests sent: "+str(scanner.requestsTotal)+"\n")
      self.fSession.write("Min interval (secs): "+str(scanner.minTimeInterval)+"\n")
      self.fSession.write("Max interval (secs): "+str(scanner.maxTimeInterval)+"\n")
      self.fSession.write("Avg interval (secs): "+str(avgInterval) +"\n")
      self.fSession.write("\n\n")
      self.fSession.write("------------------ Results -------------------\n")
      self.fSession.write("Total results generated: "+str(scanner.resultsTotal)+"\n")
