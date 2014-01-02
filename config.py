#
# These configuration values act as the default values
# no matter which service you use.
#
# Still some services will override these values if
# the given values are not between the service's
# limitations.
#

config={

   # Port for GUI
   'GUI_PORT' : 9017,

   # Log files
   'LOG_PATH'             : '/log',       # Directory where to store the log files
   'LOG_SCAN_FILENAME'    : 'scan.log',   # Name of log for the scanning process
   'LOG_STATS_FILENAME'   : 'stats.log',  # Name of log for statistics
   'LOG_RESULT_FILENAME'  : 'result.log', # Name of log for results acquired from the scanning
   'NEW_FOLDER_EACH_SCAN' :  False,       # True if you want a new folder to be created for each scanning session

   # Scanning area
   'SCANNING_AREA' : (57, 11, 58, 13),      #Stockholm

   # Scanning box options
   'box':
   {
      'X_DISTANCE' : 200000,   # desirable width of box in m.
      'Y_DISTANCE' : 200000,   # desirable height of box in m.
      'AUTOSPLIT' : True      # autosplit the box if needed
   },

   # Timing different events
   'scheduler':
   {
      'NEXT_SEARCH_WAIT'    :   0, # Seconds to wait before going to next box
      'ON_QUERY_LIMIT_WAIT' :   3, # Seconds to wait when service hits query limit
   },
   
   
   # ------------------------------------------------------------------------- #
   
   
   # These are the options and their values for the services which
   # are very permissive by default.
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
