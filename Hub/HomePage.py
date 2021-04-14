from kivy.config import Config

# 0 being off 1 being on as in true / false
# you can use 0 or 1 && True or False
Config.set('graphics', 'resizable', '1')

# fix the width of the window
Config.set('graphics', 'width', '700')

# fix the height of the window
Config.set('graphics', 'height', '450')
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
from kivy.uix.boxlayout import BoxLayout
import math
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.floatlayout import FloatLayout
TEMP_MODE = 'C'

Builder.load_string("""
<HomeScreen>:
        on_enter:
                root.start()
        FloatLayout:
                canvas.before:
                        Rectangle:
                                pos: self.pos
                                size: self.size
                                source: "background3.png"
                                
        
                Label:   
                        id: HSlabel
                        text:'Smart Garden'
                        pos_hint: {"x":0, "y":.1}
                        font_size: 54
                        color: 1, 1, 0, 1
                Button:
                        
                        text: 'Settings'
                        background_color: 0, .8, 0, 1
                        size_hint: 0.1, 0.1
                        pos_hint: {"x": 0.85, 'top': .95}
                        #on_press: root.manager.current = 'Settings'
                        on_touch_down: root.manager.current = 'Settings'

                Button:
                        id: current
                        text: 'Recent Readings'
                        size_hint: .2, .1
                        background_color: 0, .8, 0, 1
                        on_press: root.manager.current = 'Current Readings'
                        pos_hint:{"x":0.4, "top":.4}
                        #on_touch_down: root.manager.current = 'Current Readings'
                Button:
                        id: history
                        text: 'Past Readings'
                        size_hint: .2, .1
                        background_color: 0, .8, 0, 1
                        on_press: root.manager.current = 'History'
                        #on_touch_down: root.manager.current = 'History'
                        pos_hint: {"x":0.4, "top": 0.3}


<CurrentReadingsScreen>:

        on_enter:
                root.on_entered()
        on_leave:
                root.on_leave()

<HistoryReadingsScreen>:

        on_enter:
                root.build()
        FloatLayout:
                Label:
                        size: self.texture_size
                        #text_size: cm(6), cm(4)
                        font_size: 30
                        pos_hint: {"x": 0, "y": 0.4} 
                        text: 'Past Readings'
                Button:
                        id: home
                        size_hint: .1, .1
                        text:  "Home"
                        background_color: 0,.8,0.5
                        
                        pos_hint: {"x":.01, "top":1}
                        #on_press: root.manager.current = 'Home'
                        on_touch_down: root.manager.current = 'Home'
                
<SettingsScreen>:
        on_enter:
                root.build()
               
""")

class SettingsScreen(Screen):
    def build(self):
        with self.canvas.before:
            self.rect = Rectangle(size=self.size, pos=self.pos, source='background5.png')

        layout = FloatLayout()

        homeButton = Button(text='Home', size_hint = (.1,.09), pos_hint = {'x': .89, 'y': .9}, background_color = [0,.8, 0, 1])
        homeButton.bind(on_press=self.goHome)
        #homeButton.bind(on_touch_down = self.goHome)
        titleLabel = Label(text = "Settings", font_size = 50, pos_hint = {'x': 0, 'y': .4}, color=[1,1,0,1])

        layout.add_widget(homeButton)
        layout.add_widget(titleLabel)

        modeLabel = Label(text = "Temperature Mode", pos_hint = {'x': 0, 'y': .2}, font_size = 30, color = [.44,.1,.1310,1])
        layout.add_widget(modeLabel)

        fahrenheitButton = ToggleButton(text = 'Fahrenheit', group = 'temp', size_hint = (.15,.1), size = (.15,.1), pos_hint = {'x': 0.35, 'y': .55}, background_color = [0,.8, 0, 1])#, size_hint = (.2,.2))
        fahrenheitButton.bind(on_press = self.fCallback)

        celsiusButton = ToggleButton(text='Celsius', group='temp', size_hint = (.15,.1), size = (.15,.1), pos_hint = {'x': 0.5, 'y': 0.55}, background_color = [0,.8, 0, 1])
        celsiusButton.bind(on_press=self.cCallback)

        layout.add_widget(fahrenheitButton)
        layout.add_widget(celsiusButton)

        resetLabel = Label(text = 'Reset', pos_hint = {'x': 0, 'y': -.1}, font_size = 30, color = [.44,.1,.1310,1])
        resetButton = Button(text = 'Reset Readings', size_hint = (.2,.1), size = (.2,.1), pos_hint = {'x': 0.4, 'y': .25}, background_color = [0,.8, 0, 1])

        layout.add_widget(resetLabel)
        layout.add_widget(resetButton)
        self.add_widget(layout)

    def goHome(self, instance):
        self.manager.current = 'Home'

    def cCallback(self, instance):
        global TEMP_MODE
        TEMP_MODE = 'C'

    def fCallback(self, instance):
        global TEMP_MODE
        TEMP_MODE = 'F'

    def resetReadings(self, instance):
        # open file
        f = open("HistoricalReadings.csv", "r+")

        # absolute file positioning
        f.seek(0)

        # to erase all data
        f.truncate()
        f.close()

        readingsFile = open('HistoricalReadings.csv', "w")
        readingsFile.write('Date, Time, Battery Level, MAC Address, RSSI, Packet Type, Humidity, Soil Moisture, Outside Temperature, PICO Temperature, Rain Events, Light Level, Overrun')

class HomeScreen(Screen):
    def on_entered(self):
        print("scan done")
        decoder = decodeData.decodeAndWriteData(self.uuid)
        decoder.decodeData(self.uuid)#, TEMP_MODE)
        self.uuidList = decoder.getData()
        decoder.writeToFile(self.newestMac, self.rssi)

    def getAndWrite(self, dt):
        try:
            ble = bletooth.bletooth()
            ble.scanForBle()
            self.uuid = ble.getAdvertisement()
            self.mac = str(ble.getAddress())
            newMac = self.mac.replace('Address(string="', '')
            self.newestMac = newMac.replace('")', '')
            self.rssi = str(ble.getRssi())
            decoder = decodeData.decodeAndWriteData(self.uuid)
            decoder.decodeData(self.uuid)
            self.uuidList = decoder.getData()
            decoder.writeToFile(self.newestMac, self.rssi)
        except:
                popup = Popup(title='Uh oh',
                    content=Label(text='BLE beacon is out of range.'),
                    size_hint=(None, None), size=(200, 200))
                popup.open()
    def start(self):
        Clock.schedule_interval(self.getAndWrite, 30)

class HistoryReadingsScreen(Screen):
    def build(self):
        with self.canvas.before:
            #Color(.06, .4, .07, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos, source='gm.png')
        self.read_file()

        layout = GridLayout(cols=1, size_hint_y = None)

        layout.bind(minimum_height=layout.setter('height'))

        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height-90), scroll_distance = Window.height-90)

        box1 = BoxLayout(size_hint = (None, None), size = (Window.width, Window.height))
        box1.add_widget(self.tempGraph())
        layout.add_widget(box1)

        box2 = BoxLayout(size_hint = (None, None), size = (Window.width, Window.height))

        box2.add_widget(self.humidGraph())
        layout.add_widget(box2)

        box3 = BoxLayout(size_hint=(None, None), size=(Window.width, Window.height))
        box3.add_widget(self.moistureGraph())
        layout.add_widget(box3)

        box4 = BoxLayout(size_hint=(None, None), size=(Window.width, Window.height))
        box4.add_widget(self.lightGraph())
        layout.add_widget(box4)

        box5 = BoxLayout(size_hint=(None, None), size=(Window.width, Window.height))
        box5.add_widget(self.rainGraph())
        layout.add_widget(box5)

        box6= BoxLayout(size_hint=(None, None), size=(Window.width, Window.height))
        box6.add_widget(self.picoGraph())
        layout.add_widget(box6)

        box7 = BoxLayout(size_hint=(None, None), size=(Window.width, Window.height))
        box7.add_widget(self.batteryGraph())
        layout.add_widget(box7)

        root.add_widget(layout)
        self.add_widget(root)

    def read_file(self):
        self.historicalData = open("HistoricalReadings.csv", "r")
        self.fileData = []

        with open("HistoricalReadings.csv") as f:
            for line in f:
                self.fileData.append(line.split(','))
        self.historicalData.close()

    def tempGraph(self):

        tempY =[]

        for i in range(len(self.fileData) - 19, len(self.fileData)):
            tempY.append(str(math.floor((float(self.fileData[i][8]) * 100) / 255)))

        plot = None
        graph = Graph(size_hint = (.5,.8), ylabel='Outside Temperature (C)', xlabel = 'Time', x_ticks_major = 1, y_ticks_minor = 1, y_ticks_major = 1,
                  y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                  xmin=0, xmax=20, ymin=-10, ymax=50, pos_hint = {'x': .24, 'y': .2}, background_color = [1,1,1,.2])

        plot = MeshLinePlot(color = [1,1,1,1])

        plot.points = [(int(i), int(tempY[i])) for i in range(0, 19)]
        graph.add_plot(plot)
        return graph

    def humidGraph(self):
        humidY = []

        for i in range(len(self.fileData) - 19, len(self.fileData)):
            humidY.append(str(math.floor((float(self.fileData[i][6]) * 100) / 255)))

        humidityPlot = None
        humidityGraph = Graph(size_hint = (0.5,0.8), pos_hint = {'x': .24, 'y': 0}, ylabel='% Humidity', xlabel='Time', x_ticks_major=1, y_ticks_minor=1, y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                      xmin=0, xmax=20, ymin=0, ymax=100, background_color = [1,1,1,.2])

        humidityPlot = MeshLinePlot(color=[.5,0 ,.5, 1])
        humidityPlot.points = [(int(i), int(humidY[i])) for i in range(0, 19)]
        humidityGraph.add_plot(humidityPlot)

        return humidityGraph

    def moistureGraph(self):
        moistY = []
        for i in range(len(self.fileData) - 19, len(self.fileData)):
            moistY.append(str(math.floor((float(self.fileData[i][7]) * 100) / 255)))

        plot = None
        graph = Graph(size_hint = (0.5,0.8), pos_hint = {'x': .24, 'y': 0}, ylabel='% Moisture Level', xlabel='Time', x_ticks_major=1, y_ticks_minor=1,
                              y_ticks_major=1,
                              y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                              xmin=0, xmax=20, ymin=0, ymax=100, background_color = [1,1,1,.2])

        plot = MeshLinePlot(color=[1, 1, 1, 1])
        plot.points = [(int(i), int(moistY[i])) for i in range(0, 19)]
        graph.add_plot(plot)

        return graph

    def batteryGraph(self):
        battY = []
        for i in range(len(self.fileData) - 19, len(self.fileData)):
            battY.append(str(math.floor((float(self.fileData[i][2]) * 100) / 255)))

        plot = None
        graph = Graph(size_hint = (0.5,0.8), pos_hint = {'x': .24, 'y': 0}, ylabel='% Battery Level', xlabel='Time', x_ticks_major=1, y_ticks_minor=1,
                      y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                      xmin=0, xmax=20, ymin=0, ymax=100, background_color = [1,1,1,.2])

        plot = MeshLinePlot(color=[.5, 0, .5, 1])
        plot.points = [(int(i), int(battY[i])) for i in range(0, 19)]
        graph.add_plot(plot)

        return graph

    def lightGraph(self):
        lightY = []
        for i in range(len(self.fileData) - 19, len(self.fileData)):
            lightY.append(str(math.floor((float(self.fileData[i][11]) * 100) / 255)))

        plot = None
        graph = Graph(size_hint = (0.5,0.8), pos_hint = {'x': .24, 'y': 0}, ylabel='% Light Level', xlabel='Time', x_ticks_major=1, y_ticks_minor=1,
                       y_ticks_major=1,
                       y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                       xmin=0, xmax=20, ymin=0, ymax=100, background_color = [1,1,1,.2])

        plot = MeshLinePlot(color=[.5, 0, .5, 1])
        plot.points = [(int(i), int(lightY[i])) for i in range(0, 19)]
        graph.add_plot(plot)

        return graph

    def picoGraph(self):
        picoY = []
        for i in range(len(self.fileData) - 19, len(self.fileData)):
            picoY.append(str(math.floor((float(self.fileData[i][9]) * 100) / 255)))

        plot = None
        graph = Graph(size_hint = (0.5,0.8), pos_hint = {'x': .24, 'y': 0}, ylabel='Pico Temperature (C)', xlabel='Time', x_ticks_major=1, y_ticks_minor=1,
                      y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                      xmin=0, xmax=20, ymin=-10, ymax=50, background_color = [1,1,1,.2])

        plot = MeshLinePlot(color=[.5,0,.5, 1])
        plot.points = [(int(i), int(picoY[i])) for i in range(0, 19)]
        graph.add_plot(plot)

        return graph

    def rainGraph(self):
        rainY = []
        for i in range(len(self.fileData) - 19, len(self.fileData)):
            rainY.append(str(math.floor((float(self.fileData[i][10]) * 100) / 255)))
        plot = None
        graph = Graph(size_hint = (0.5,0.8), pos_hint = {'x': .24, 'y': 0}, ylabel='Rain Events', xlabel='Time', x_ticks_major=1, y_ticks_minor=1,
                      y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                      xmin=0, xmax=20, ymin=0, ymax=50, background_color = [1,1,1,.2])

        plot = MeshLinePlot(color=[.5, 0, .5, 1])
        plot.points = [(int(i), int(rainY[i])) for i in range(0, 19)]
        graph.add_plot(plot)

        return graph

class CurrentReadingsScreen(Screen):
    def on_entered(self):
        with open('HistoricalReadings.csv', 'r') as f:
            for line in f:
                pass
            lastLine = line
        readLine = lastLine.split(',')
        self.data = readLine
        self.displayCurrentReadings()

    def getTempMode(self):
        return self.tempMode

    def displayCurrentReadings(self):
                layout = GridLayout(cols=2, padding = 110, spacing=5,
                                    size_hint=(None, None),size = (Window.width, Window.height), rows = 4, orientation = 'lr-tb', pos_hint={'center_y':.45})
                with self.canvas.before:
                    Color(1, 1, 1, .3)
                    self.rect = Rectangle(size=self.size, pos=self.pos, source = 'background6.png')

                homeBtn = Button(text = "Home", size_hint = (.1,.1), background_color = [0,.8, .5, 1], pos_hint = {'x': 0, 'top': 1})
                homeBtn.bind(on_press = self.goHome)
                self.add_widget(homeBtn)

                titleLabel= Label(text = 'Recent Readings', font_size = 30, pos_hint = {'x':0, 'top': 1.4})
                self.add_widget(titleLabel)

                timeAndDateLabel = Label(text = "Time Read: " + self.data[0] + " " + " " + self.data[1], font_size = 17, pos_hint = {'x': 0, 'top': 1.3})
                self.add_widget(timeAndDateLabel)

                if TEMP_MODE == 'F':
                    uncalculatedoTemp = (math.floor(float(self.data[8])*1.8) + 32)
                    uncalculatedpTemp = (math.floor(float(self.data[9])*1.8) + 32)
                    oTemp = math.floor((float(uncalculatedoTemp * 100) / 255))
                    pTemp = math.floor((float(uncalculatedpTemp * 100) / 255))
                    self.tempLabel = Label(text = "Outside Temperature: " + str(oTemp) + u'\N{DEGREE SIGN}' + 'F', font_size = 18)
                    layout.add_widget(self.tempLabel)
                    self.picoLabel = Label(text='Pico Temperature: ' + str(pTemp) + u'\N{DEGREE SIGN}' + 'F', font_size=18)
                    layout.add_widget(self.picoLabel)

                elif TEMP_MODE == 'C':
                    oTemp = (math.floor((float(self.data[8]) * 100) / 255))
                    pTemp = (math.floor((float(self.data[9]) * 100) / 255))
                    self.tempLabel = Label(text="Outside Temperature: " + str(oTemp) + u'\N{DEGREE SIGN}' + 'C',
                                      font_size=18, color = [1,1,1,1] )#str(self.uuidList[0])
                    layout.add_widget(self.tempLabel)
                    self.picoLabel = Label(text='Pico Temperature: ' + str(pTemp) + u'\N{DEGREE SIGN}' + 'C',
                                      font_size=18, color = [1,1,1,1] )
                    layout.add_widget(self.picoLabel)

                humidLabel = Label(text = "Humidity: " + str(math.floor((float(self.data[6]) * 100) / 255)) + '%', font_size = 18)
                layout.add_widget(humidLabel)

                moistureLabel = Label(text = "Soil Moisture: " + str(math.floor((float(self.data[7]) * 100) / 255)) + '%', font_size = 18)
                layout.add_widget(moistureLabel)

                battLabel = Label(text = 'Battery Voltage: ' + str(math.floor((float(self.data[2]) * 100) / 255)) + '%', font_size = 18)
                layout.add_widget(battLabel)

                rainLabel = Label(text = 'Rain Events: ' + str(math.floor((float(self.data[10]) * 100) / 255)), font_size = 18)
                layout.add_widget(rainLabel)

                rssiLabel = Label(text = "RSSI: " +  self.data[4], font_size = 18)
                layout.add_widget(rssiLabel)

                lightLabel = Label(text = "Light Level: " + str(math.floor((float(self.data[11]) * 100) / 255)) + '%', font_size = 18)
                layout.add_widget(lightLabel)
                print(self.data[11])

                self.add_widget(layout)

    def goHome(self, *args):
        self.manager.current = 'Home'

    def on_leave(self):
        self.clear_widgets()

class SmartGardenApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='Home'))
        sm.add_widget(CurrentReadingsScreen(name='Current Readings'))
        sm.add_widget(HistoryReadingsScreen(name='History'))
        sm.add_widget(SettingsScreen(name = 'Settings'))
        return sm

if __name__ == "__main__":

    HomePage = SmartGardenApp()
    HomePage.run()
