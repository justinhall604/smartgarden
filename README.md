# smartgarden
Collects enviromental information using low powered sensors and ble beacon technology. Stores on a Raspberry Pi and let a user view information and graphs using a touch screen and graphical interface.
Smart Garden version 1.0 03/07/2021
-----------------------------------------------------------------------------
General Usage Notes:
- All libraries are supported on Windows, Mac, and Linux OS
- A method to undo data written to the file is not included. Removal of data must be done manually from the file.
- At the moment, all functionality is contained in 1 file, HomePage.py (however this will likely be changed, as it's just too much at this point, and design-
  wise, is deeply frowned upon)
- Thus, to test the program, your environment simply needs two things in the same package: a txt file, "HistoricalReadings.txt", and "HomePage.py."
- You will also need an active BLE device with a 16-bit UUID.
- Currently, the timer is set to record data every 6 minutes. In order to change this, go to the HomeScreen class, line 81, and change "600" to 
whatever interval you want (in seconds).
-Also, the code currently contains MUCH duplication... don't judge me!!  
- The issue that the graph/scrollview stems from is commented (the function beginning in line 128). The current readings screen is also having layout issues, but I haven't wrestled with it for as
long as I have wrestled the graph view issue.
- Lastly, I originally set up the basic screens using the kv language, but shifted the majority of it to Python.  
------------------------------------------------------------------------------
Required Libraries to Import:
from adafruit_ble.advertising import to_bytes_literal
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
import time
from adafruit_ble import BLERadio
import binascii
from kivy_garden.graph import Graph, MeshLinePlot
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
