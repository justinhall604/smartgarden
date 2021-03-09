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
import graphs
from kivy.uix.boxlayout import BoxLayout

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
                root.build()
       
               
""")

class HomeScreen(Screen):

    def getAndWrite(self, dt):
        ble = bletooth.bletooth()
        ble.scanForBle()
        self.uuid = ble.getAdvertisement()
        decoder = decodeData.decodeAndWriteData(self.uuid)
        decoder.decodeData(self.uuid)
        self.uuidList = decoder.getData()
        decoder.writeToFile()

    def start(self):
        Clock.schedule_interval(self.getAndWrite, 1000)



class HistoryReadingsScreen(Screen): ##THIS IS THE GRAPH ISSUE
    def build(self): #was on_enter
        self.read_file()
        titleLabel = Label(text="Historical Readings", font_size=24,
                           pos_hint={'x': 0, 'top': 1})  ##this isn't positioned correctly
        self.add_widget(titleLabel)
        homeBtn = Button(text="Home", size_hint=(0.1, 0.1), pos_hint={'x': 0, 'top': .95})
        homeBtn.bind(on_press=self.goHome)
        self.add_widget(homeBtn)

        layout = GridLayout(cols=1, size_hint_y = None) #padding=10, spacing=20,
                            #size_hint=(None, None), width=672)

        layout.bind(minimum_height=layout.setter('height'))

        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height), scroll_distance = Window.height)
                          #pos_hint={'center_x': .5, 'center_y': .5}, do_scroll_x=False)

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
        #Graphs = [self.tempGraph(), self.humidGraph(), self.moistureGraph(), self.lightGraph(), self.batteryGraph(), self.picoGraph(), self.rainGraph()]
#PI IS 4.33in (416 pixels) height by 7" wide (672 pixels)
        # for i in range(len(Graphs)):
        #     #view = ModalView(size_hint=(1,1))
        #     graph = Graphs[i]
        #     #view.add_widget(graph)
        #     #layout.add_widget(view)
        #     layout.add_widget(graph)



    def goHome(self, *args):
        self.manager.current = 'Home'

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


        fileLength = len(self.fileData) #size_hint = (0.5,0.5),
        plot = None
        graph = Graph(size_hint = (.5,.5), ylabel='Outside Temperature', xlabel = 'Time', x_ticks_major = 1, y_ticks_minor = 1, y_ticks_major = 1, #size and pos not working
                  y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                  xmin=0, xmax=20, ymin=0, ymax=200, pos_hint = {'x': .24, 'y': .2} )

        plot = MeshLinePlot(color = [1,0,0,1])

        plot.points = [(int(i), int(tempY[i])) for i in range(1, len(self.fileData)-1)]
        graph.add_plot(plot)
        return graph

    def humidGraph(self):
        humidY = []

        for i in range(1, len(self.fileData)):
            humidY.append(self.fileData[i][6])

        humidityPlot = None
        humidityGraph = Graph(size_hint = (0.5,0.5), pos_hint = {'x': .24, 'y': 0}, ylabel='Humidity', xlabel='Time', x_ticks_major=1, y_ticks_minor=1, y_ticks_major=1,
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
        graph = Graph(size_hint = (0.5,0.5), pos_hint = {'x': .24, 'y': 0}, ylabel='Moisture Level', xlabel='Time', x_ticks_major=1, y_ticks_minor=1,
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
        graph = Graph(size_hint = (0.5,0.5), pos_hint = {'x': .24, 'y': 0}, ylabel='Battery Level', xlabel='Time', x_ticks_major=1, y_ticks_minor=1,
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
        graph = Graph(size_hint = (0.5,0.5), pos_hint = {'x': .24, 'y': 0}, ylabel='Light Level', xlabel='Time', x_ticks_major=1, y_ticks_minor=1,
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
        graph = Graph(size_hint = (0.5,0.5), pos_hint = {'x': .24, 'y': 0}, ylabel='Pico Temperature', xlabel='Time', x_ticks_major=1, y_ticks_minor=1,
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
        graph = Graph(size_hint = (0.5,0.5), pos_hint = {'x': .24, 'y': 0}, ylabel='Rain Events', xlabel='Time', x_ticks_major=1, y_ticks_minor=1,
                      y_ticks_major=1,
                      y_grid_label=True, x_grid_label=True, padding=5, x_grid=True, y_grid=True,
                      xmin=0, xmax=50, ymin=0, ymax=200)

        plot = MeshLinePlot(color=[1, 2, 3, 4])
        plot.points = [(int(i), int(rainY[i])) for i in range(1, len(self.fileData) - 1)]
        graph.add_plot(plot)

        return graph

class CurrentReadingsScreen(Screen):
    def pre_enter(self):
        ble = bletooth.bletooth() ##scanning twice and saving to file twice...
        ble.scanForBle()
        self.uuid = ble.getAdvertisement()


    def on_entered(self):
        print("scan done")
        decoder = decodeData.decodeAndWriteData(self.uuid)
        decoder.decodeData(self.uuid)
        self.uuidList = decoder.getData()
        decoder.writeToFile()
        self.displayCurrentReadings()

    def displayCurrentReadings(self): ##LAYOUT NOT IN CORRECT POSITION
        layout = GridLayout(cols=2, padding = 1, spacing=4,
                            size_hint=(None, None), width=500, rows = 7, orientation = 'lr-tb')

        tempLabel = Label(text = "Outside Temperature: " + str(self.uuidList[0]))
        layout.add_widget(tempLabel)
        humidLabel = Label(text = "Humidity: " + str(self.uuidList[1]) + '%')
        layout.add_widget(humidLabel)
        moistureLabel = Label(text = "Soil Moisture: " + str(self.uuidList[2]))
        layout.add_widget(moistureLabel)

        battLabel = Label(text = 'Battery Voltage: ' + str(self.uuidList[3]))
        layout.add_widget(battLabel)
        lightLabel = Label(text = 'Light Level: ' + str(self.uuidList[4]))
        layout.add_widget(lightLabel)
        picoLabel = Label(text = 'Pico Temperature: ' + str(self.uuidList[5]))
        layout.add_widget(picoLabel)
        rainLabel = Label(text = 'Rain Events: ' + str(self.uuidList[6]))
        layout.add_widget(rainLabel)

        self.add_widget(layout)



class TestApp(App):

    def build(self):
       # self.size = (Window.size)
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='Home'))
        sm.add_widget(CurrentReadingsScreen(name='Current Readings'))
        sm.add_widget(HistoryReadingsScreen(name='History'))
        return sm



if __name__ == "__main__":

    HomePage = TestApp()
    HomePage.run()
