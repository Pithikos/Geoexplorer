# Configuration values for application
config={

   # Port for GUI
   'GUI_PORT': 9017,

   # Log files
   'LOG_PATH'             : '/log',
   'LOG_SCAN_FILENAME'    : 'scan.log',   # Name of log for the scanning process
   'LOG_STATS_FILENAME'   : 'stats.log',  # Name of log for statistics
   'LOG_RESULT_FILENAME'  : 'result.log', # Name of log for results acquired from the scanning
   'NEW_FOLDER_EACH_SCAN' : False,        # True if you want a new folder to be created for each scan

   # Service
   'service':
   {
      'KEY'       : 'AIzaSyCMHNMC8ijFWXQFNrKy5FJ-uYSTZYrdAlM', # if needed by the service
   },

   # Box rules
   'box':
   {
      'MAX_X_DISTANCE'   : 100000,        # max x distance in m
      'MAX_Y_DISTANCE'   : 100000,        # max x distance in m
   },

   # Costs. This is used as a multiplier for each request
   'costs':
   {
      'PER_REQUEST' :  5, # Cost per request, 5 for Google's radar search
   },

   # Limit the results from scanning
   'limiter':
   {
      #'bounds':  (85, 10, 0, 65), # Lat, Lng, Lat2, Lng2
      #'bounds':  (-30, 10.0, 30, 0.0),
      #'bounds':  (66, 11, 57, 27),  #scandinavia
      #'bounds':  (66, 11, 57, 14),  #norway - sweden
      #'bounds':  (-10, 0, 75, -0.5),#vertical line
      'BOUNDS':  (60, 17, 59, 19), #stockholm 4x4
      #'bounds':  (60, 17, 57, 19), #stockholm+gotland
      #'bounds':  (59.5, 17.38, 58.9, 18.7), # Don't scan outside these bounds
      'COUNTRY_CODE': 'se',                  # Scan only inside specific country
      'COUNTRY_CHECK_METHOD': 'NOMINATIM', # Should be either FROMRADARSEARCH or NOMINATIM
   },

   # Schedule the timings of the scanning
   'scheduler':
   {
      'NEXT_SEARCH_WAIT'    :   1, # Seconds to wait before going to next box
      'ON_QUERY_LIMIT_WAIT' :   3, # Seconds to wait when query limit
   }

}
