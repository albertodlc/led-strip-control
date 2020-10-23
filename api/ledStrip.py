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

JSON_FORMAT = {
                "MAC": "",
                "R" : 0,
                "G" : 0,
                "B" : 0,
                "POWER" : ""
}

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
    def file_creation(mac_addr):
        try:
            # Initilize message format
            led_status = JSON_FORMAT
            led_status["MAC"] = mac_addr

            f = open(led_status["MAC"] + ".json", "r")
            led_status = json.load(f)

        except FileNotFoundError:
            led_status["R"] = 255
            led_status["G"] = 255
            led_status["B"] = 255
            led_status["POWER"] = "on"

            with open(led_status["MAC"] + ".json", "w") as f:
                json.dump(led_status, f, indent = 1)

        finally:
            f.close()
            return led_status

    @staticmethod
    def file_modification(led_status):
        f = open(led_status["MAC"] + ".json", "r")
        led_status_updated = json.load(f)
        f.close()

        led_status_updated["R"] = led_status["R"]
        led_status_updated["G"] = led_status["G"]
        led_status_updated["B"] = led_status["B"]

        led_status_updated["POWER"] = led_status["POWER"]

        with open(led_status_updated["MAC"] + ".json", "w") as f:
            json.dump(led_status_updated, f, indent = 1)
            f.close()

class DeviceControl:
    def __init__(self, mac_addr):
        # Save/Load the status of the LED
        self.led_status = Utils.file_creation(mac_addr)

        self.p = Peripheral(self.led_status["MAC"])
        self.s = self.p.getServiceByUUID(LED_SERVICES[4])
        self.ch_W = self.s.getCharacteristics(LED_CHARACTERISTICS[0])[0]

        if self.led_status["POWER"] == "off":
            self.turn_on()
            self.set_color(self.led_status["R"], self.led_status["G"], self.led_status["B"])

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
        # Avoid turning on the light in case it is on
        if self.led_status["POWER"] == "off":
            # Turn ON the light
            self.ch_W.write(LedStripMessages.on_message())
            self.p.disconnect()

            # Update status
            self.led_status["POWER"] = "on"
            Utils.file_modification(self.led_status)

    def turn_off(self):
        # Avoid turning off the light in case it is off
        if self.led_status["POWER"] == "on":
            # Turn OFF the light
            self.ch_W.write(LedStripMessages.off_message())
            self.p.disconnect()

            # Update status
            self.led_status["POWER"] = "on"
            Utils.file_modification(self.led_status)

    def modify_intensity(self, intensity):
        self.R = int(self.R*intensity)
        self.G = int(self.G*intensity)
        self.B = int(self.B*intensity)
        self.ch_W.write(LedStripMessages.color_message(self.R, self.G, self.B))

        self.p.disconnect()

    def set_color(self, R, G, B):
        # Avoid changing color of the light in case it is off
        if self.led_status["POWER"] == "on":
            # SET color of the LED
            self.ch_W.write(LedStripMessages.color_message(R, G, B))
            self.p.disconnect()

            # Update status
            self.led_status["R"] = R
            self.led_status["G"] = G
            self.led_status["B"] = B

            Utils.file_modification(self.led_status)


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
dc = DeviceControl(MAC_ADDR[0]);
dc1 = DeviceControl(MAC_ADDR[1]);
dc2 = DeviceControl(MAC_ADDR[2]);
dc3 = DeviceControl(MAC_ADDR[3]);

dc.turn_on()
dc1.turn_on()
dc2.turn_on()
dc3.turn_on()
#app.run(host='0.0.0.0')
