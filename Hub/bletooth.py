import binascii
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from adafruit_ble.advertising import Advertisement
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

class bletooth():
    def scanForBle(self):

        ble = BLERadio()
        #ble._adapter.ble_backend = "bleak"  # Forces bleak even if hcitool works.
        #ble._adapter.ble_backend = "hcitool" # Forces hcitool. Raises exception if unavailable.
        print("scanning")
        found = set()

        self.byteList = []
        self.macList = []
        self.rssiList = []
        self.nameList = []
        scan_responses = set()
        for advertisement in ble.start_scan(ProvideServicesAdvertisement, Advertisement):
            self.byteList.append(bytes(advertisement))
            addr = advertisement.address
            self.macList.append(addr)
            self.rssiList.append(advertisement.rssi)
            self.nameList.append(advertisement.complete_name)
            print("Complete name: " , advertisement.complete_name)

            print("mac: ", addr)

            print("\t" + repr(advertisement))
            print("length ", len(advertisement))
            print()
            if advertisement.scan_response and addr not in scan_responses:
                scan_responses.add(addr)
                #print("Addr: ", addr)

            elif not advertisement.scan_response and addr not in found:
                found.add(addr)
                found.add(advertisement)
            else:
                continue
            if advertisement.complete_name == "Garden":
                ble.stop_scan()

            print()

    def getAdvertisement(self):
        #try:
        i = 0
        j = 0
        for adBytes in self.byteList:
            print(adBytes)
            print()
            print()
            if len(adBytes) == 13 and self.nameList[j] == "Garden":# and self.:#27:
                self.targetBytes = binascii.b2a_hex(adBytes)
                self.address = self.macList[i]
                self.rssi = self.rssiList[i]
                break
            i = i+1
            j = j+1

        if self.rssi <= -80:
            popup = Popup(title='Uh oh',
                            content=Label(text='BLE beacon signal is very weak.'),
                            size_hint=(None, None), size=(200, 200))
            popup.open()
            return False

        print("target: ", self.targetBytes)
        bArray = bytearray(self.targetBytes)
        self.uuid = bArray[5:12]

        return self.uuid
        # except:
        #     popup = Popup(title='Uh oh',
        #                   content=Label(text='BLE beacon is out of range'),
        #                   size_hint=(None, None), size=(200, 200))
        #     popup.open()
        #     return False

    def getAddress(self):
        return self.address

    def getRssi(self):
        return self.rssi