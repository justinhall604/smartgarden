from adafruit_ble import BLERadio
import binascii

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
            print()
            print()
            if len(adBytes) == 27:
                self.targetBytes = binascii.b2a_hex(adBytes)
                break
        print("target: ", self.targetBytes)
        bArray = bytearray(self.targetBytes)
        self.uuid = bArray[12:44]
        return self.uuid
