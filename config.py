# Configuration values for Google Places Plus
config={

   # Google KEY
   'Gkey':        'AIzaSyCMHNMC8ijFWXQFNrKy5FJ-uYSTZYrdAlM',

   # Port for GUI
   'GUI_port': 9017,

   # Log files
   'log_path'             : '/log',
   'log_scan_filename'    : 'scan.log',
   'log_gstics_filename'  : 'gstics.log',
   'log_result_filename'  : 'result.log',

   # Rules from Google
   'Grules':
   {
      'maxScannableDistance': 50000,        # max radius distance for scanning in m
      'maxLat': 89,
      'max_quota_per_day': 1000, # The number of Google Places requests per 24h for non-verified key
      'cost_textsearch' : 10,
      'cost_radarsearch': 5,
      'cost_details'    : 1,
      'cost_search'     : 1,
   },
   
   
   # Limit the results from scanning
   'limiter':
   {
      #'bounds':  [85, 10, 0, 65], # Lat, Lng, Lat2, Lng2
      #'bounds':  [-30, 10.0, 30, 0.0],
      #'bounds':  [66, 11, 57, 27],  #scandinavia
      'bounds':  [66, 11, 57, 14],  #norway - sweden
      #'bounds':  [-10, 0, 75, -0.5],#vertical line
      #'bounds':  [60, 17, 59, 19], #stockholm 4x4
      #'bounds':  [60, 17, 57, 19], #stockholm+gotland
      #'bounds':  [59.5, 17.38, 58.9, 18.7], # Don't scan outside these bounds
      'country_code': 'se'                   # Scan only inside specific country
   },


   # Schedule the timings of the scanning
   'scheduler':
   {
      'next_search_wait'    :  1, # Seconds to wait before going to next box
      'on_query_limit_wait' :  3, # Seconds to wait when query limit
      'max_quota_per_day'   : 900 # Stop if quota exceeds this limit
   }
   
}
