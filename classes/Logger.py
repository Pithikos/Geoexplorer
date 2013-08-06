import datetime
from os import remove

class Logger:
   
   scanner = None # Let's logger access all scanner's information
   
   fScan   = None # Keeps track of each step in the scanning process
   fGstics = None # Keeps track of google quota for each scan
   fResult = None # Makes a record of the findings from the scan


   # scanpath -> full path to logfile
   #
   def __init__(self, scanpath, gsticspath, resultpath, scanner):
      self.scanner=scanner

      # Remove old files
      try:
         with open(scanpath):
            remove(scanpath)
      except IOError:
         pass
      try:
         with open(gsticspath):
            remove(gsticspath)
      except IOError:
         pass
      try:
         with open(resultpath):
            remove(resultpath)
      except IOError:
         pass
      self.fScan=open(scanpath, "a", 1)
      self.fGstics=open(gsticspath, "w", 1)
      self.fResult=open(resultpath, "a", 1)


   # Append text as a new line to a log file
   def append(self, type, text):
      if   (type=='scan'):
         self.fScan.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" : "+text+"\n")
      elif (type=='result'):
         self.fResult.write(text+"\n")


   # Update Google statistics log
   def Gstics(self):
      scanner=self.scanner
      
      # Remove old file
      self.fGstics.seek(0, 0)
      self.fGstics.truncate()
      
      if (not scanner.scanFinishDatetime):
         finished='-'
      else:
         finished=str(scanner.scanFinishDatetime.strftime("%Y-%m-%d %H:%M:%S"))
         
      self.fGstics.write("Started scanning : "+str(scanner.scanStartDatetime.strftime("%Y-%m-%d %H:%M:%S"))+"\n")
      self.fGstics.write("Finished scanning: "+finished+"\n")
      self.fGstics.write("Requests sent    : "+str(scanner.GrequestsTotal)+"\n")
      self.fGstics.write("Quota used       : "+str(scanner.GquotaUsed)+"\n")


   #---------------------------- State messages from the scanner ---------------------------


   def finished_scanning_box(self):
      pass

   def finished_scanning(self):
      self.Gstics()

   def received_google_respond(self):
      pass

   def sent_google_request(self):
      self.Gstics()
