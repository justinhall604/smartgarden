import time

class decodeAndWriteData(bytearray):

    def decodeData(self, uuid):

        self.uuid = uuid
        uuidDecoded = self.uuid.decode()
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

        self.outsideTemp = int(uuid[0]) * 16 + int(uuid[1])

        self.humidity = int(uuid[2]) * 16 + int(uuid[3])

        self.moistureLevel = int(uuid[4]) * 16 + int(uuid[5])

        self.battVoltage = int(uuid[6]) * 16 + int(uuid[7])

        self.lightLevel = int(uuid[8]) * 16 + int(uuid[9])

        self.picoTemp = int(uuid[10]) * 16 + int(uuid[11])

        self.rainEvents = int(uuid[12]) * 16 + int(uuid[13])


    def getData(self):
        self.dataList = []
        self.dataList.append(self.outsideTemp)
        self.dataList.append(self.humidity)
        self.dataList.append(self.moistureLevel)
        self.dataList.append(self.battVoltage)
        self.dataList.append(self.lightLevel)
        self.dataList.append(self.picoTemp)
        self.dataList.append(self.rainEvents)
        return self.dataList

    def writeToFile(self):

        readingsFile = open("HistoricalReadings.txt", 'a')
        readTime = time.asctime()
        readingsFile.write(readTime + "\t")
        readingsFile.write(str(self.outsideTemp) + "\t\t\t\t\t\t\t")
        readingsFile.write(str(self.humidity) + "\t\t\t\t")
        readingsFile.write(str(self.moistureLevel) + "\t\t\t\t\t\t\t")
        readingsFile.write(str(self.battVoltage) + "\t\t\t\t\t")
        readingsFile.write(str(self.lightLevel) + "\t\t\t\t\t")
        readingsFile.write(str(self.picoTemp) + "\t\t\t\t\t\t")
        readingsFile.write(str(self.rainEvents) + "\n")
        readingsFile.close()