Geoexplorer
========================================================================

Author:        Johan Hanssen Seferidis
Created:       2013-06-20

Description:   Geoexplorer is a framework meant to be used for black-box-testing
               and/or scraping data from geographic services like Google Places
               and Foursquare.
             
Documentation: Full documentation both for developers and users can be
               found in the doc folder.



Install dependencies
========================================================================

Ubuntu 13.10:
Works out of the box.

Ubuntu 12.04:
sudo apt-get install python3 python3-lxml

Windows 7:
  1. Download and install python3.2 from http://www.python.org/download/releases/3.2.5
  2. Edit windows path:
     a. Control Panel -> System -> Advanced system settings
     b. Click the Environment variables... button
     c. Edit PATH and append ;C:\python32\
  3. Install the lxml3.2 from http://pypi.python.org/pypi/lxml/3.2.4


Usage
========================================================================

  1. Run "python3 examples/<example>.py", substituting <example> with one
     of the example files
  2. Open /GUI/index.html with a webbrowser to see live what is going on

A folder called *log* will be created at the current directory. This
folder with be populated with log files on-the-fly.


Configuration
========================================================================

The config.py keeps all the applicable options for Geoexplorer in a single file.
Each option is described bellow:
 
      GUI_PORT                -> Port being used for the communication with the
                                 GUI
      
      LOG_PATH                -> Folder name where logs should be stored
      LOG_SCANNING_FILENAME   -> Name of file for logging scanning steps
      LOG_SESSION_FILENAME    -> Name of file for logging statistics fom each
                                 scanning session
      LOG_RESULTS_FILENAME    -> Name of file for logging every single result
      NEW_FOLDER_EACH_SESSION -> Should a new folder be created on each scanning
                                 session?
      
      BOUNDS                  -> The coordinates lat, lng, lat2, lng2 for
                                 scanning. 
      
      'box'
      X_DISTANCE              -> Desirable distance in m. for a box' x axis
      Y_DISTANCE              -> Desirable distance in m. for a box' y axis

      'scheduler'
      NEXT_SEARCH_WAIT        -> Seconds to wait before going scanning next box

The 'service' entry is used as a template by the services and should not
be altered.


Logging
========================================================================

There are three files for logging different things.

      SESSION:  Different statistics for the whole scanning session
      SCANNING: This is the main debugging log file. Every scanning step is recorded
                in this file.
      RESULTS:  This keeps all the results extracted during the scanning session


Troubleshooting
========================================================================

The map in the GUI doesn't show any boxes.
A. Try to install the latest firefox web browser. The GUI will not work
   for old browsers(IE8 for example).
