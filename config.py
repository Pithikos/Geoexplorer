# Configuration values for Google Places Plus
config={

   # Google KEY
   'Gkey':        'AIzaSyCMHNMC8ijFWXQFNrKy5FJ-uYSTZYrdAlM',

   # Paths
   'browserPath': '/usrfirefox',

   # Port for GUI
   'GUIport': 9017,
   
   # Rules from Google
   'Grules':
   {
      'maxScannableDistance': 50000,        # max radius distance for scanning in m
      'maxLat': 89
   },
   
   
   # Limit the results from scanning
   'limiter':
   {
      #'bounds':  [85, 10, 0, 65], # Lat, Lng, Lat2, Lng2
      #'bounds':  [-30, 10.0, 30, 0.0],
      #'bounds':  [66, 11, 57, 27],  #scandinavia
      #'bounds':  [-10, 0, 75, -0.5],#vertical line
      'bounds':  [60, 17, 57, 19], #stockholm+gotland
      #'bounds':  [59.5, 17.38, 58.9, 18.7], # Don't scan outside these bounds
      'country': 'se'                        # Scan only inside specific country
   },
   
   
   # Schedule the timings of the scanning
   'scheduler':
   {
      
   }
   
}
