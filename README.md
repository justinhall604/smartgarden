# smartgarden
Collects enviromental information using low powered sensors and ble beacon technology. Stores on a Raspberry Pi and let a user view information and graphs using a touch screen and graphical interface.
Smart Garden version 1.0 03/07/2021
-----------------------------------------------------------------------------
General Usage Notes:
- All libraries are supported on Windows, Mac, and Linux OS
- A method to undo data written to the file is not included. Removal of data must be done manually from the file.
- At the moment, all functionality is contained in 1 file, HomePage.py (however this will likely be changed, as it's just too much at this point, and design-
  wise, is deeply frowned upon)
- Thus, to test the program, your environment simply needs four files in the same package: a txt file, "HistoricalReadings.txt", "HomePage.py", "decodeData.py", and "bletooth.py". Currently,
  graphs.py is empty.
- You will also need an active BLE device with a 16-bit UUID.
- Currently, the timer is set to record data every 10 minutes. In order to change this, go to the HomeScreen class, line 81, and change "600" to 
whatever interval you want (in seconds).
- In order for the code to work, the length of the bluetooth advertisement MUST be known by the program. This can be changed by going into the
bletooth.py file and changing the number at the end of the statement 'if len(adBytes) == 27:' (line 31)
- In order to lessen duplicate code, I wrote the "decodeData.py" file, which contains about 28 lines of code that was used in multiple parts of the program. However,
  the program is now running a scan for a ble device twice and writing the results to the file twice. I am not sure how this happened, and I have not been able to fix it yet.
- The issue that the graph/scrollview stems from is commented. The current readings screen is also having layout issues, but I haven't wrestled with it for as
long as I have wrestled the graph view issue.
- Lastly, I originally set up the basic screens using the kv language, but shifted the majority of it to Python.  
------------------------------------------------------------------------------
Required Libraries to Import for HomePage.py:
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
import decodeData
import bletooth
import graphs **will be required later
from kivy.uix.boxlayout import BoxLayout

Required Libraries to import for decodeDate.py:
import time

Required Libraries to import for bletooth.py:
from adafruit_ble import BLERadio
import binascii