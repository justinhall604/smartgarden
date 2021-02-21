import kivy
import time
import bluetooth
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import BLE_GATT
from beacontools import parse_packet
import struct
import kivy
import bluetooth
from kivy.app import App
from kivy.lang import Builder
import asyncio
from bleak import BleakScanner
from beacontools import parse_packet
from kivy.uix.gridlayout import Layout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
import time
from adafruit_ble import BLERadio
import datetime

Builder.load_string("""
<HomeScreen>:
        FloatLayout:
                Label:   
                        id: HSlabel
                        text:'Smart Garden'
                        pos_hint: {"x":0, "y":.2}
                        font_size: 54

                Button:
                        id: current
                        text: 'Current Readings'
                        size_hint: .2, .1
                        background_color: 1, 2, 3, 4
                        on_press: root.manager.current = 'Current Readings'
                        pos_hint:{"x":0.4, "top":.5}
                Button:
                        id: history
                        text: 'History'
                        size_hint: .2, .1
                        on_press: root.manager.current = 'History'
                        pos_hint: {"x":0.4, "top": 0.4}


<CurrentReadingsScreen>:
        on_pre_enter:
                root.pre_enter()
                
                Label: 'Connecting to device...'
                
        on_enter:
                root.on_entered()
        
        FloatLayout:

                Button:
                        id: home
                        size_hint: .1, .1
                        text: 'Home'
                        pos_hint: {"x":.01, "top":1}
                        on_press: root.manager.current = 'Home'


<HistoryReadingsScreen>:
        on_enter:
                root.on_enter()
        FloatLayout:
                Button:
                        id: home
                        size_hint: .1, .1
                        text: 'Home'
                        on_press: root.manager.current = 'Home'
                        pos_hint: {"x":.01, "top":1}
""")


class HomeScreen(Screen):
    pass

class CurrentReadingsScreen(Screen):
    def pre_enter(self):
        #print('Connecting to device')
        #self.beacon = blueTooth(BLE_GATT.Central('AC:BC:32:AC:F8:B4'), '00002222-0000-1000-8000-00805F9B34FB')
        ble = BLERadio()
        print("scanning")
        found = set()
        scan_responses = set()
        for advertisement in ble.start_scan():
            addr = advertisement.address
            if advertisement.scan_response and addr not in scan_responses:
                scan_responses.add(addr)
            elif not advertisement.scan_response and addr not in found:
                found.add(addr)
            else:
                continue
            print(addr, advertisement)
            print("\t" + repr(advertisement))
            print()

        print("scan done")

    def on_entered(self):


        print("scan done")
        #self.beacon.readFromDevice()
        #self.beacon.parseData()
        #self.writeToFile()

    def writeToFile(self):
        readingsFile = open("HistoricalReadings.txt", 'a')
        readTime = time.asctime()
        #PARSE AND GET INFO

        readingsFile.write(readTime + " ")
        readingsFile.write('Temperature ')
        readingsFile.write('pH "')
        readingsFile.write('Water Level ')
        readingsFile.write('Humidity ')
        readingsFile.write('\n\n\n\n')

        readingsFile.close()



class HistoryReadingsScreen(Screen):
    def on_enter(self):
        # self.open_file()
        self.readFile()

    def readFile(self):
        historicalData = open("HistoricalReadings.txt", 'r')
        historicalData.read()
        print(historicalData.read())


class TestApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='Home'))
        sm.add_widget(CurrentReadingsScreen(name='Current Readings'))
        sm.add_widget(HistoryReadingsScreen(name='History'))
        return sm

class blueTooth(object):
    def __init__(self, my_device, my_uuid):
        self.my_device = my_device
        self.my_uuid = my_uuid

    def readFromDevice(self):
        self.my_device.connect()
        self.value = self.my_device.char_read(self.my_uuid)
        print(self.value)
        #print(type(self.value))
        self.my_device.disconnect()

    #def parseData(self):
        #print(int.from_bytes(self.value[0:2], byteorder='little', signed=False))



if __name__ == "__main__":
    HomePage = TestApp()
    HomePage.run()



#if __name__ == "__main__":

    #run()
       # bt = blueTooth(BLE_GATT.Central('AC:BC:32:AC:F8:B4'), '00002222-0000-1000-8000-00805F9B34FB')
       #  bt.readFromDevice()
        #bt.parseData()

       #  my_device = BLE_GATT.Central('AC:BC:32:AC:F8:B4')
       #  my_uuid = '00002222-0000-1000-8000-00805F9B34FB'
       #  my_device.connect()
       #  value = my_device.char_read(my_uuid)
       #  print(value)
       # # print(type(value))
       #  my_device.disconnect()
# async def run():
#     devices = await BleakScanner.discover()
#     for d in devices:
#         print(d)

#loop = asyncio.get_event_loop()
#loop.run_until_complete(run())



ble = BLERadio()
print("scanning")
found = set()
scan_responses = set()
for advertisement in ble.start_scan():
    addr = advertisement.address
    if advertisement.scan_response and addr not in scan_responses:
        scan_responses.add(addr)
    elif not advertisement.scan_response and addr not in found:
        found.add(addr)
    else:
        continue
    print(addr, advertisement)
    print("\t" + repr(advertisement))
    print()

print("scan done")

