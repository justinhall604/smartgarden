import time
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import datetime

class decodeAndWriteData(bytearray):

    def decodeData(self, uuid):
        print("in decode")
        self.uuid = uuid
        uuidDecoded = self.uuid.decode()
        print("decoded: " , uuidDecoded)
        uuid = []
        self.dataList = []
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

        print(len(uuid))

        print("new uuid: ", uuid)
        self.battVoltage = int(uuid[0]) * 16 + int(uuid[1])#
        print("batt: " , self.battVoltage)
        self.humidity = int(uuid[2]) * 16 + int(uuid[3])#
        print("humidity: ", self.humidity)
        self.moistureLevel = int(uuid[4]) * 16 + int(uuid[5])#
        print("moisture: ", self.moistureLevel)
        self.outsideTemp = int(uuid[6]) * 16 + int(uuid[7])#
        print("outside temp: ", self.outsideTemp)
        self.picoTemp = int(uuid[8]) * 16 + int(uuid[9])#
        print("pico: " , self.picoTemp)
        self.lightLevel = int(uuid[10])*16 + int(uuid[11])
        print("light: ", self.lightLevel)
        self.rainEventsGreater0 = int(uuid[12]) * 16 + int(uuid[13]) # %>0
        print('rain less 0: ', self.rainEventsGreater0)
        self.rainEventsLess0 = int(uuid[14]) * 16 + int(uuid[15]) # %<0
        print("rain greater 0: ", self.rainEventsLess0)
        self.rainEvents = self.rainEventsGreater0 + (self.rainEventsLess0 * 0.01)
        print("rain: ", self.rainEvents)

        if self.battVoltage <= 50:
            popup = Popup(title = 'uh oh', content = Label(text = 'Low Battery'), size_hint = (None, None), size = (400,200))

    def getData(self):
        self.dataList = []

        self.dataList.append(self.outsideTemp)
        self.dataList.append(self.humidity)
        self.dataList.append(self.moistureLevel)
        self.dataList.append(self.battVoltage)
        self.dataList.append(self.picoTemp)
        self.dataList.append(self.lightLevel)
        self.dataList.append(self.rainEvents)
        print("data list: ",  self.dataList)

        ##notify user if there is a data issue
        # if self.dataList[0] > 120:
        #     popup = Popup(title='Uh oh',
        #                   content=Label(text='Temperature is higher than 120. Check your sensors.'),
        #                   size_hint=(None, None), size=(400, 200))
        #     popup.open()
        # elif self.dataList[1] > 100:
        #     popup = Popup(title='Uh oh',
        #                   content=Label(text='Humidity is higher than 100%. Check your sensors.'),
        #                   size_hint=(None, None), size=(400, 200))
        #     popup.open()
        # elif self.dataList[5] >= 185:
        #     popup = Popup(title='Uh oh',
        #                   content=Label(text='PICO temperature is at or above 185 degrees Fahrenheit!! Please move PICO now!!'),
        #                   size_hint=(None, None), size=(500, 200))
        #     popup.open()

        return self.dataList

    def writeToFile(self, mac, rssi):
        self.MAC = mac
        self.rssi = rssi
        readingsFile = open('HistoricalReadings.csv', 'a')
        readDate = datetime.date.today()
        now = time.localtime()
        readTime = time.strftime("%H : %M: %S", now)

        readingsFile.write(str(readDate) + ' ,')
        readingsFile.write(readTime + ' ,')

        readingsFile.write(str(self.MAC) + ' ,')
        readingsFile.write(str(self.rssi) + ' ,')

        readingsFile.write(str(self.humidity) + ' ,')
        readingsFile.write(str(self.moistureLevel) + ' ,')
        readingsFile.write(str(self.outsideTemp) + ' ,')
        readingsFile.write(str(self.picoTemp) + ' ,')
        readingsFile.write(str(self.rainEvents) + ',')
        readingsFile.write(str(self.lightLevel) + ',')
        readingsFile.write(str(self.battVoltage) + ',')
        #readingsFile.write(str(self.packetType) + ' ,')
        readingsFile.write(',' + "\n")
        readingsFile.close()

