# smartgarden
Collects enviromental information using low powered sensors and ble beacon technology. Stores on a Raspberry Pi and let a user view information and graphs using a touch screen and graphical interface.
Smart Garden version 1.0 03/07/2021

__author__ = Kirsten Hernquist & Justin Hall
__copyright__ = Attribution-NonCommercial-NoDerivs CC-BY-NC-ND 2021 Kirsten Hernquist and Justin Hall"
__version__ = "1.0"

-----------------------------------------------------------------------------
General Usage Notes:
- All libraries are supported on Windows, Mac, and Linux OS (HOWEVER there have been issues downloading adafruit-circuitpython and adafruit-blinka-bleio on any OS apart from Raspbian)
- Thus, to test the program, your environment simply needs four files in the same package: a txt file, "HistoricalReadings.csv", "HomePage.py", "decodeData.py", and "bletooth.py". 
- You will also need an active BLE device with a 16-bit UUID.
- Currently, the timer is set to record data every 10 minutes. In order to change this, go to the HomeScreen class, line 81, and change "600" to 
whatever interval you want (in seconds).
- In order for the code to work, the length of the bluetooth advertisement MUST be known by the program. This can be changed by going into the
bletooth.py file and changing the number at the end of the statement 'if len(adBytes) == 27:' (line 31)
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
from adafruit_ble import BLERadio (must install adafruit-circuitpython-ble and adafruit-blinka-bleio)
import binascii

Image credits:
"daisy wallpaper" by .robbie is licensed under CC BY-SA 2.0
"6981579-flowers-background" by thinhalvin1996hp is licensed under CC BY-SA 2.0
"Premade Background" by rubyblossom. is licensed under CC BY-NC 2.0