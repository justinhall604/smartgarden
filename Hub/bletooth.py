from adafruit_ble import BLERadio
import binascii
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from adafruit_ble.advertising import Advertisement
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.advertising.standard import ServiceData
from adafruit_ble.characteristics import StructCharacteristic

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

        scan_responses = set()
        for advertisement in ble.start_scan(ProvideServicesAdvertisement, Advertisement):
            self.byteList.append(bytes(advertisement))
            print(len(advertisement))
            #print(advertisement.raw_data)
            addr = advertisement.address
            self.macList.append(addr)
            self.rssiList.append(advertisement.rssi)
            #print(type(advertisement))
            print(advertisement)
            print(type(advertisement.address))
            #print("ad: " , advertisement)
            print("Complete name: " , advertisement.complete_name)

            print("mac: ", addr)
            print("rssi ", advertisement.rssi)
            print(addr, advertisement)
            print("\t" + repr(advertisement))
            print("String{}" , str(advertisement))
            print("Bytes{}", bytes(advertisement))
            #if advertisement.address == "Address(string='A5:A5:A5:A5:A5:A5')":
               # print("here")
                #print(advertisement)

               # print("string: " , str(advertisement))
               # ble.stop_scan()
            #print(advertisement.name)
            if advertisement.scan_response and addr not in scan_responses:
                scan_responses.add(addr)
                #print("Addr: ", addr)

            elif not advertisement.scan_response and addr not in found:
                found.add(addr)
                found.add(advertisement)
            else:
                continue
            print()



            #ble.stop_scan()

    def getAdvertisement(self):
        #try:
        i = 0
        for adBytes in self.byteList:
            print(adBytes)
            print()
            print()
            if len(adBytes) == 24:#27:
                self.targetButes = adBytes
                self.targetBytes = binascii.b2a_hex(adBytes)
                self.address = self.macList[i]
                self.rssi = self.rssiList[i]

                #print("MAC: ", self.address)
                break
            i = i+1

        if self.rssi <= -80:
            popup = Popup(title='Uh oh',
                            content=Label(text='BLE beacon signal is very weak.'),
                            size_hint=(None, None), size=(200, 200))
            popup.open()
            return False

        print("not bytes: " , self.targetButes)
        print("target: ", self.targetBytes)
        bArray = bytearray(self.targetBytes)
        self.uuid = bArray[12:44]
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