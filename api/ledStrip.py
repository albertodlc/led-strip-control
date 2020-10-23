from bluepy.btle import UUID, Peripheral, Scanner, DefaultDelegate
import time, flask, json
from flask import request

# Flask Web App definition

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# API definition

MAC_ADDR = [
            "85:58:1B:08:AD:ED", # Mesa 1
            "85:58:1B:08:97:4D", # Mesa 2
            "85:58:1B:08:C6:67", # Mesa 3
            "52:14:00:00:C6:A9" # Techo
            ]

# LED STRIP SERVICES (Depend of the strip, maybe you have to CHANGE THIS)
LED_SERVICES = [
                UUID(0x1800), # Generic Access
                UUID(0x1801), # Generic Attribute
                UUID(0x180A), # Device Info
                UUID(0xFFD0), # Unknown
                UUID(0xFFD5)  # Unknown
                ]

LED_CHARACTERISTICS = [UUID(0xFFD9)]

# Class override to handle notifications from the devices
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

class ScanDevices:
    def __init__(self, sd = None, scan_time = 10.0):
        self.scan_time = scan_time
        self.device_array = []

        if sd == None:
            self.sc = Scanner() # Init without HandleDiscovery
        else:
            self.sc = sc = Scanner().withDelegate(sd) # Init with HandleDiscovery

        # Scan for devices and return a list of ScanEntry
        scan_entry_array = self.sc.scan(self.scan_time)

        # Check if any of the detected devices is a LED STRIP
        for se in scan_entry_array:
            if any(word in se.addr.upper() for word in MAC_INIT):
                self.device_array.append(se.addr.upper())

    def show_devices(self):
        print("**AVAILABLE LED STRIPS**\n")
        for dev in self.device_array:
            print(dev)

class LedStripMessages:
    # Format of the MESSSAGES
    FIRST_HEX = "56"
    FINAL_HEX = "00F0AA"
    TURN_ON = "CC2333"
    TURN_OFF = "CC2433"

    @staticmethod
    def on_message():
        return bytearray.fromhex(LedStripMessages.TURN_ON)

    @staticmethod
    def off_message():
        return bytearray.fromhex(LedStripMessages.TURN_OFF)

    @staticmethod
    def color_message(R,G,B):
        return bytearray.fromhex(LedStripMessages.FIRST_HEX + Utils.rgb_to_hex(R, G, B) + LedStripMessages.FINAL_HEX)

class Utils():
    @staticmethod
    def rgb_to_hex(R, G, B):
        return '{:02x}{:02x}{:02x}'.format(R, G, B)

    @staticmethod
    def file_creation(name, mac_addr):
        try:
            f = open(mac_addr + ".json", "r")
                led_status = json.load()

        except FileNotFoundError:

            led_status = {
                            "MAC": mac_addr,
                            "R" : 255,
                            "G" : 255,
                            "B" : 255
            }

            with open(mac_addr + ".json", "w") as file:
                json.dump(led_status, f, indent = 1)
            file.close()
        finally:
            f.close()
            return led_status

class DeviceControl:
    def __init__(self, mac_addr):



        # Init LED STRIP with white color
        self.R = 255
        self.G = 255
        self.B = 255

        self.mac_addr = mac_addr

        self.p = Peripheral(self.mac_addr)

        self.s = self.p.getServiceByUUID(LED_SERVICES[4])
        self.ch_W = self.s.getCharacteristics(LED_CHARACTERISTICS[0])[0]
        self.ch_W.write(LedStripMessages.color_message(self.R, self.G, self.B))

    def show_perif_services_char(self):
        print("\n\tDevice:" + self.p.addr)
        print("\t\t", end = '')
        print(self.s)
        print("\t\t\t", end = '')
        print(self.ch)

    def show_perif(self):
        print("\nDevice: " + self.p.addr)

    def show_services(self):
        print("Services:")
        for s in self.p.getServices():
            print("\tUUID", s.uuid.getCommonName(), s.uuid.binVal)

    def show_charac(self):
        print("Characteristics")
        for s in self.p.getServices():
            for ch in s.getCharacteristics():
                print("\tUUID", ch.uuid.getCommonName(), s.uuid.binVal)

    def turn_on(self):
        self.ch_W.write(LedStripMessages.on_message())
        self.p.disconnect()
        return ""

    def turn_off(self):
        self.ch_W.write(LedStripMessages.off_message())
        self.p.disconnect()

    def modify_intensity(self, intensity):
        self.R = int(self.R*intensity)
        self.G = int(self.G*intensity)
        self.B = int(self.B*intensity)
        self.ch_W.write(LedStripMessages.color_message(self.R, self.G, self.B))

        self.p.disconnect()


class API():
    @app.route('/led/mesa/on', methods=['POST'])
    def turn_on_1():
        dc = DeviceControl(MAC_ADDR[0]);
        dc1 = DeviceControl(MAC_ADDR[1]);
        dc2 = DeviceControl(MAC_ADDR[2]);

        dc.turn_on()
        dc1.turn_on()
        dc2.turn_on()
        return ""

    @app.route('/led/techo/on', methods=['POST'])
    def turn_on_2():
        dc = DeviceControl(MAC_ADDR[3]);
        dc.turn_on()
        return ""

    @app.route('/led/all/on', methods=['POST'])
    def turn_on_3():
        dc = DeviceControl(MAC_ADDR[0]);
        dc1 = DeviceControl(MAC_ADDR[1]);
        dc2 = DeviceControl(MAC_ADDR[2]);
        dc3 = DeviceControl(MAC_ADDR[3]);

        dc.turn_on()
        dc1.turn_on()
        dc2.turn_on()
        dc3.turn_on()
        return ""

    @app.route('/led/mesa/off', methods=['POST'])
    def turn_off_1():
        dc = DeviceControl(MAC_ADDR[0]);
        dc1 = DeviceControl(MAC_ADDR[1]);
        dc2 = DeviceControl(MAC_ADDR[2]);

        dc.turn_off()
        dc1.turn_off()
        dc2.turn_off()
        return ""

    @app.route('/led/techo/off', methods=['POST'])
    def turn_off_2():
        dc = DeviceControl(MAC_ADDR[3]);
        dc.turn_off()
        return ""

    @app.route('/led/all/off', methods=['POST'])
    def turn_off_3():
        dc = DeviceControl(MAC_ADDR[0]);
        dc1 = DeviceControl(MAC_ADDR[1]);
        dc2 = DeviceControl(MAC_ADDR[2]);
        dc3 = DeviceControl(MAC_ADDR[3]);

        dc.turn_off()
        dc1.turn_off()
        dc2.turn_off()
        dc3.turn_off()
        return ""

    @app.route('/led/all/intensity', methods=['POST'])
    def modify_intensity():
        intensity_f = int(request.args.get("intensity"))/100

        if intensity_f > 1.0:
            intensity_f = 1.0
        elif intensity_f < 0.0:
            intensity_f = 0.0

        dc = DeviceControl(MAC_ADDR[0]);
        dc1 = DeviceControl(MAC_ADDR[1]);
        dc2 = DeviceControl(MAC_ADDR[2]);
        dc3 = DeviceControl(MAC_ADDR[3]);

        dc.modify_intensity(intensity_f)
        dc1.modify_intensity(intensity_f)
        dc2.modify_intensity(intensity_f)
        dc3.modify_intensity(intensity_f)
        return ""
#sd = ScanDevices()

#for dev in sd.device_array:
#    dc = DeviceControl(dev)
#    dc.close_connection()
dc = DeviceControl(MAC_ADDR[0])
#app.run(host='0.0.0.0')
