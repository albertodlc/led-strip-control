from bluepy.btle import UUID, Peripheral, Scanner, DefaultDelegate
import bluepy.btle as btle
import utils as Utils
import ledStripMessages as LedStripMessages

# LED STRIP SERVICES (Depend of the strip, maybe you have to CHANGE THIS)
LED_SERVICES = [
                UUID(0x1800), # Generic Access
                UUID(0x1801), # Generic Attribute
                UUID(0x180A), # Device Info
                UUID(0xFFD0), # Unknown 
                UUID(0xFFD5)  # Unknown 
                ]

LED_CHARACTERISTICS = [UUID(0xFFD9) # 
                       
                       ]

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

class DeviceControl:
    def __init__(self, mac_addr):
        # Save/Load the status of the LED
        self.led_status = Utils.file_creation(mac_addr)

        self.p = Peripheral(self.led_status["MAC"])
        self.s = self.p.getServiceByUUID(LED_SERVICES[4])
        self.ch_W = self.s.getCharacteristics(LED_CHARACTERISTICS[0])[0]

    def turn_on(self):
        # Avoid turning on the light in case it is on
        if self.led_status["POWER"] == "off":
            # Turn ON the light
            self.ch_W.write(LedStripMessages.on_message())

            # Update status
            self.led_status["POWER"] = "on"
            Utils.file_modification(self.led_status)

    def turn_off(self):
        # Avoid turning off the light in case it is off
        if self.led_status["POWER"] == "on":
            # Turn OFF the light
            self.ch_W.write(LedStripMessages.off_message())

            # Update status
            self.led_status["POWER"] = "off"
            Utils.file_modification(self.led_status)

    def set_color(self, R, G, B):
        # Avoid changing color of the light in case it is off
        if self.led_status["POWER"] == "on":
            # SET color of the LED
            self.ch_W.write(LedStripMessages.color_message(R, G, B))

            # Update status
            self.led_status["R"] = R
            self.led_status["G"] = G
            self.led_status["B"] = B

            Utils.file_modification(self.led_status)
    
    def close_connection(self):
        self.p.disconnect()

