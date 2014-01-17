#
# These configuration values affect the behaviour of
# the framework no matter which service you use.
#

config={

   # Port for GUI
   'GUI_PORT' : 9017,

   # Log files
   'LOG_PATH'                : '/log',         # Directory where to store the log files
   'LOG_SCANNING_FILENAME'   : 'scanning.log', # Main log file used for debugging
   'LOG_SESSION_FILENAME'    : 'session.log',  # Keeps statistics for each scanning session
   'LOG_RESULTS_FILENAME'    : 'results.log',  # All the results extracted from the scanning session
   'NEW_FOLDER_EACH_SESSION' :  False,        # True if you want a new folder to be created for each scanning session

   # Scanning area
   #'SCANNING_AREA' : (61.5, 19, 59, 14),              # Central Sweden
   #'SCANNING_AREA' : (59.35, 18.05, 59.34, 18.07),    # Stockholm
   'SCANNING_AREA' : (60, 15, 59, 18),                # Big area

   # Scanning box options
   'box':
   {
      'X_DISTANCE' : 1000000,   # desirable width of box in m.
      'Y_DISTANCE' : 1000000,   # desirable height of box in m.
      'AUTOSPLIT'  : True      # autosplit the box if needed
   },

   # Timing different events
   'scheduler':
   {
      'NEXT_SEARCH_WAIT' :   0, # Seconds to wait before scanning next box
   },
   
   
   # ------------------------------------------------------------------------- #
   
   
   # These are the options and their values for the services
   # which are very permissive by default.
   # Most of these will be overdriven by the service being used. The ones not
   # overdriven, will remain permissive.
   'service':
   {
      'authentication':
      {
         'REQUIRED'         : False,
      },
      
      'box':
      {
         'MAX_X_DISTANCE'   : 'INF',  # max width in real m.
         'MAX_Y_DISTANCE'   : 'INF',  # max height in real m.
      },
      
      'request':
      {
         'MAX_COST_DAY'         : 'INF', # The max cost per day
         'COST_PER_REQUEST'     :     0, # The cost of a single request
         'MIN_REQUEST_INTERVAL' :     0, # The min time waiting between requests
      },
      
      'response':
      {
         'MAX_RESULTS'          : 'INF', # The max number of results a respone
                                         # can give
      }

   }
   
}
