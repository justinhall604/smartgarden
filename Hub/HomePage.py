from adafruit_ble.advertising import to_bytes_literal
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock
import asyncio
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
import binascii
from kivy_garden.graph import Graph, MeshLinePlot

Builder.load_string("""
<HomeScreen>:
        on_enter:
                root.start()
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
                
        on_enter:
                root.on_entered()
        
        FloatLayout:
                Label:
                        size: self.texture_size
                        text_size: cm(6), cm(4)
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
                Label:
                        text: 'Historical Readings'
                        pos_hint: {"x":.0, "y":.45}
                        font_size: 30
                Button:
                        id: home
                        size_hint: .1, .1
                        text: 'Home'
                        on_press: root.manager.current = 'Home'
                        pos_hint: {"x":.01, "top":1}
    
""")


class HomeScreen(Screen):
    def getAndWrite(self, dt):
        ble = bletooth()
        ble.scanForBle()
        self.uuid = ble.getAdvertisement()
        self.decode_data()
        self.writeToFile()

    def start(self):
        Clock.schedule_interval(self.getAndWrite, 600)

    def decode_data(self):
        uuidDecoded = self.uuid.decode()
        uuid = []
        for i in range(len(uuidDecoded)):
            try:
                int(uuidDecoded[i])
                uuid.append(uuidDecoded[i])

            except:
                if uuidDecoded[i] == 'a':
                    uuid.append(10)
                elif uuidDecoded[i] == 'b':
                    uuid.append(11)
                elif uuidDecoded[i] == 'c':
                    uuid.append(12)
                elif uuidDecoded == 'd':
                    uuid.append(13)
                elif uuidDecoded == 'e':
                    uuid.append(14)
                else:
                    uuid.append(15)

        self.outsideTemp = int(uuid[0])*16 + int(uuid[1])
        self.humidity = int(uuid[2])*16+int(uuid[3])
        self.moistureLevel = int(uuid[4])*16+int(uuid[5])
        self.battVoltage = int(uuid[6])*16+int(uuid[7])
        self.lightLevel = int(uuid[8])*16+int(uuid[9])
        self.picoTemp = int(uuid[10])*16+int(uuid[11])
        self.rainEvents = int(uuid[12])*16+int(uuid[13])

    def writeToFile(self):
        readingsFile = open("HistoricalReadings.txt", 'a')
        readTime = time.asctime()
        readingsFile.write(readTime + "\t")
        readingsFile.write(str(self.outsideTemp) + "\t\t\t\t\t\t\t")  # 'Outside Temperature: ' +
        readingsFile.write(str(self.humidity) + "\t\t\t\t")  # 'Humidity:  ' +
        readingsFile.write(str(self.moistureLevel) + "\t\t\t\t\t\t\t")  # 'Soil Moisture Level: ' +
        readingsFile.write(str(self.battVoltage) + "\t\t\t\t\t")  # 'Battery Voltage: ' +
        readingsFile.write(str(self.lightLevel) + "\t\t\t\t\t")  # 'Light Level: ' +
        readingsFile.write(str(self.picoTemp) + "\t\t\t\t\t\t")  # 'PICO Temperature: ' +
        readingsFile.write(str(self.rainEvents) + "\n")  # 'Rain Events: ' +
        readingsFile.close()


from kivy.uix.modalview import ModalView
class HistoryReadingsScreen(Screen):

    def on_enter(self):
        self.read_file()
        #box = BoxLayout(orientation= "horizontal", padding = [0,15,15,10])
        Graphs = [self.tempGraph(), self.humidGraph(), self.moistureGraph(), self.lightGraph(), self.batteryGraph(), self.picoGraph(), self.rainGraph()]
        for i in range(len(Graphs)):
            view = ModalView(size_hint=(0.5,0.5))
            graph = Graphs[i]
            view.add_widget(graph)
            #view.open()
            self.add_widget(view)

    def read_file(self):
        self.historicalData = open("HistoricalReadings.txt", 'r')
        self.fileData = []

        with open("HistoricalReadings.txt") as f:
            for line in f:
                self.fileData.append(line.split())

        self.historicalData.close()

    def tempGraph(self):

        tempY =[] ##graph y values, all data self.tempY

        for i in range(1, len(self.fileData)):
            tempY.append(self.fileData[i][5])


        fileLength = len(self.fileData)
        plot = None
        graph = Graph(ylabel='Outside Temperature', xlabel = 'Time', x_ticks_major = 1, y_ticks_minor = 1, y_ticks_major = 1,
                  y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                  xmin=0, xmax=50, ymin=0, ymax=200)

        plot = MeshLinePlot(color = [1,2,3,4])
        print(len(self.fileData))
        print(tempY)
        print(len(tempY))
        plot.points = [(int(i), int(tempY[i])) for i in range(1, len(self.fileData)-1)]
        graph.add_plot(plot)
        return graph

    def humidGraph(self):
        humidY = []

        for i in range(1, len(self.fileData)):
            humidY.append(self.fileData[i][6])

        humidityPlot = None
        humidityGraph = Graph(ylabel='Humidity', xlabel='Time', x_ticks_major=1, y_ticks_minor=1, y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                      xmin=0, xmax=50, ymin=0, ymax=200)

        humidityPlot = MeshLinePlot(color=[1, 2, 3, 4])
        humidityPlot.points = [(int(i), int(humidY[i])) for i in range(1, len(self.fileData) - 1)]
        humidityGraph.add_plot(humidityPlot)

        return humidityGraph

    def moistureGraph(self):
        moistY = []
        for i in range(1, len(self.fileData)):
            moistY.append(self.fileData[i][7])

        plot = None
        graph = Graph(ylabel='Moisture Level', xlabel='Time', x_ticks_major=1, y_ticks_minor=1,
                              y_ticks_major=1,
                              y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                              xmin=0, xmax=50, ymin=0, ymax=200)

        plot = MeshLinePlot(color=[1, 2, 3, 4])
        plot.points = [(int(i), int(moistY[i])) for i in range(1, len(self.fileData) - 1)]
        graph.add_plot(plot)

        return graph

    def batteryGraph(self):
        battY = []
        for i in range(1, len(self.fileData)):
            battY.append(self.fileData[i][8])

        plot = None
        graph = Graph(ylabel='Battery Level', xlabel='Time', x_ticks_major=1, y_ticks_minor=1,
                      y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                      xmin=0, xmax=50, ymin=0, ymax=200)

        plot = MeshLinePlot(color=[1, 2, 3, 4])
        plot.points = [(int(i), int(battY[i])) for i in range(1, len(self.fileData) - 1)]
        graph.add_plot(plot)

        return graph

    def lightGraph(self):
        lightY = []
        for i in range(1, len(self.fileData)):
            lightY.append(self.fileData[i][9])


        plot = None
        graph = Graph(ylabel='Light Level', xlabel='Time', x_ticks_major=1, y_ticks_minor=1,
                      y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                      xmin=0, xmax=50, ymin=0, ymax=200)

        plot = MeshLinePlot(color=[1, 2, 3, 4])
        plot.points = [(int(i), int(lightY[i])) for i in range(1, len(self.fileData) - 1)]
        graph.add_plot(plot)

        return graph

    def picoGraph(self):
        picoY = []
        for i in range(1, len(self.fileData)):
            picoY.append(self.fileData[i][10])

        plot = None
        graph = Graph(ylabel='Pico Temperature', xlabel='Time', x_ticks_major=1, y_ticks_minor=1,
                      y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                      xmin=0, xmax=50, ymin=0, ymax=200)

        plot = MeshLinePlot(color=[1, 2, 3, 4])
        plot.points = [(int(i), int(picoY[i])) for i in range(1, len(self.fileData) - 1)]
        graph.add_plot(plot)

        return graph

    def rainGraph(self):
        rainY = []
        for i in range(1, len(self.fileData)):
            rainY.append(self.fileData[i][11])
        plot = None
        graph = Graph(ylabel='Rain Events', xlabel='Time', x_ticks_major=1, y_ticks_minor=1,
                      y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                      xmin=0, xmax=50, ymin=0, ymax=200)

        plot = MeshLinePlot(color=[1, 2, 3, 4])
        plot.points = [(int(i), int(rainY[i])) for i in range(1, len(self.fileData) - 1)]
        graph.add_plot(plot)

        return graph


class CurrentReadingsScreen(Screen):
    def pre_enter(self):
        ble = bletooth()
        ble.scanForBle()
        self.uuid = ble.getAdvertisement()


    def on_entered(self):
        print("scan done")
        self.decode_data()

        #self.writeToFile()
        ##display information

    def decode_data(self):
        uuidDecoded = self.uuid.decode()
        uuid = []
        for i in range(len(uuidDecoded)):
            try:
                int(uuidDecoded[i])
                uuid.append(uuidDecoded[i])

            except:
                if uuidDecoded[i] == 'a':
                    uuid.append(10)
                elif uuidDecoded[i] == 'b':
                    uuid.append(11)
                elif uuidDecoded[i] == 'c':
                    uuid.append(12)
                elif uuidDecoded == 'd':
                    uuid.append(13)
                elif uuidDecoded == 'e':
                    uuid.append(14)
                else:
                    uuid.append(15)

        self.outsideTemp = int(uuid[0])*16 + int(uuid[1])
        self.humidity = int(uuid[2])*16+int(uuid[3])
        self.moistureLevel = int(uuid[4])*16+int(uuid[5])
        self.battVoltage = int(uuid[6])*16+int(uuid[7])
        self.lightLevel = int(uuid[8])*16+int(uuid[9])
        self.picoTemp = int(uuid[10])*16+int(uuid[11])
        self.rainEvents = int(uuid[12])*16+int(uuid[13])

    def writeToFile(self):
        readingsFile = open("HistoricalReadings.txt", 'a')
        readTime = time.asctime()
        readingsFile.write(readTime + "\t")
        readingsFile.write(str(self.outsideTemp) + "\t\t\t\t\t\t\t")#'Outside Temperature: ' +
        readingsFile.write(str(self.humidity) + "\t\t\t\t")#'Humidity:  ' +
        readingsFile.write(str(self.moistureLevel) + "\t\t\t\t\t\t\t")#'Soil Moisture Level: ' +
        readingsFile.write(str(self.battVoltage) + "\t\t\t\t\t")#'Battery Voltage: ' +
        readingsFile.write(str(self.lightLevel) + "\t\t\t\t\t")#'Light Level: ' +
        readingsFile.write(str(self.picoTemp) + "\t\t\t\t\t\t")#'PICO Temperature: ' +
        readingsFile.write(str(self.rainEvents) + "\n")#'Rain Events: ' +
        readingsFile.close()


class bletooth():
    def scanForBle(self):
        ble = BLERadio()
        print("scanning")
        found = set()

        self.byteList = []
        scan_responses = set()
        for advertisement in ble.start_scan():
            self.byteList.append(bytes(advertisement))
            addr = advertisement.address
            if advertisement.scan_response and addr not in scan_responses:
                scan_responses.add(addr)
            elif not advertisement.scan_response and addr not in found:
                found.add(addr)
                found.add(advertisement)
            else:
                continue
            print()
            ble.stop_scan()

    def getAdvertisement(self):
        for adBytes in self.byteList:
            #print(len(adBytes))
            print()
            print()
            if len(adBytes) == 39:  ##length of nrfBlinky advertisement
                self.targetBytes = binascii.b2a_hex(adBytes)
                self.targetButes = to_bytes_literal(adBytes)
                print("target: ", self.targetButes)
                break
        print("target: ", self.targetBytes)
        bArray = bytearray(self.targetBytes)
        self.uuid = bArray[12:44]
        return self.uuid

class TestApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='Home'))
        sm.add_widget(CurrentReadingsScreen(name='Current Readings'))
        sm.add_widget(HistoryReadingsScreen(name='History'))
        return sm


if __name__ == "__main__":

    #timer = TimeApp()
   # timer.run()
    HomePage = TestApp()
    HomePage.run()
