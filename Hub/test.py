import kivy
import bluetooth
from kivy.app import App
from kivy.lang import Builder
from beacontools import parse_packet
from kivy.uix.gridlayout import Layout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.graphics.instructions import Canvas
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import ScreenManager, Screen
import time
#from kivy.time import time
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
    def on_entered(self):
        self.scanForBeacon()
        #self.readBeacon()
       # self.writeToFile()
    def scanForBeacon(self):


        devices = bluetooth.discover_devices(lookup_names=True, lookup_class=True)

        number_of_devices = len(devices)
        print(number_of_devices, "devices found");
        for addr, name, device_class in devices:
            self.addr = addr
            print("addr: ",  self.addr)
            self.name = name
            self.device_class = device_class
            print("\n Device: ")
            print("device Name: %s" % (name))
            print("Device MAC Address: %s" % (addr))
            print("\n")
            print("device class: %s " % (device_class))
            print("\n")

        if number_of_devices == 0:
            print("Device is out of range")


    def readBeacon(self):
        #tlm_packet
        # tlm_packet = b"\x02\x01\x06\x03\x03\xaa\xfe\x11\x16\xaa\xfe\x20\x00\x0b\x18\x13\x00\x00\x00" \
        #              b"\x14\x67\x00\x00\x2a\xc4\xe4"
        # tlm_frame = parse_packet(tlm_packet)
        # print("Voltage: %d mV" % tlm_frame.voltage)
        # print("Temperature: %d °C" % tlm_frame.temperature)
        # print("Advertising count: %d" % tlm_frame.advertising_count)
        # print("Seconds since boot: %d" % tlm_frame.seconds_since_boot)
       # print("addr: ", self.addr)
        services = bluetooth.find_service(address = str(self.addr))
        if len(services) <= 0:
            print("No services found on ", self.addr)
        else:
            for serv in services:
                print(serv['name'])
                print("\n")
            return()

    def writeToFile(self):
        readingsFile = open("HistoricalReadings.txt", 'a')


class HistoryReadingsScreen(Screen):
    def on_enter(self):
        #self.open_file()
        self.readFile()

    def readFile(self):
        historicalData = open("HistoricalReadings.txt", 'r')
        historicalData.read()
        print(historicalData.read())


class TestApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='Home'))
        sm.add_widget(CurrentReadingsScreen(name = 'Current Readings'))##='Current Readings'))
        sm.add_widget(HistoryReadingsScreen(name='History'))
        return sm


if __name__ == "__main__":

    HomePage = TestApp()
    HomePage.run()