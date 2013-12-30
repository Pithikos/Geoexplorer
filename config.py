# This is the configuration for the program
# Some of these options will be overriden by some services
config={

   # Port for GUI
   'GUI_PORT': 9017,

   # Log files
   'LOG_PATH'             : '/log',       # Directory where to store the log files
   'LOG_SCAN_FILENAME'    : 'scan.log',   # Name of log for the scanning process
   'LOG_STATS_FILENAME'   : 'stats.log',  # Name of log for statistics
   'LOG_RESULT_FILENAME'  : 'result.log', # Name of log for results acquired from the scanning
   'NEW_FOLDER_EACH_SCAN' : False,        # True if you want a new folder to be created for each scan

   # Box rules
   'box':
   {
      'MAX_X_DISTANCE'   : 100000,  # max x distance in m.
      'MAX_Y_DISTANCE'   : 100000,  # max y distance in m.
   },

   # Costs
   'costs':
   {
      'PER_REQUEST' :  1, # Overriden by some services
   },

   # Limit the search area
   'limiter':
   {
      #'BOUNDS':  (85, 10, 0, 65), # Lat, Lng, Lat2, Lng2
      #'BOUNDS':  (-30, 10.0, 30, 0.0),
      #'BOUNDS':  (66, 11, 57, 27),  #scandinavia
      #'BOUNDS':  (66, 11, 57, 14),  #norway - sweden
      #'BOUNDS':  (-10, 0, 75, -0.5),#vertical line
      'BOUNDS':  (60, 17, 59, 19), #stockholm 4x4
      #'BOUNDS':  (60, 17, 57, 19), #stockholm+gotland
      #'BOUNDS':  (59.5, 17.38, 58.9, 18.7), # Don't scan outside these bounds
   },

   # Schedule the timings of the scanning
   'scheduler':
   {
      'NEXT_SEARCH_WAIT'    :   1, # Seconds to wait before going to next box
      'ON_QUERY_LIMIT_WAIT' :   3, # Seconds to wait when service hits query limit
   }

}
