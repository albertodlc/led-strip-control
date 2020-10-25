import json

JSON_FORMAT = {
                "MAC": "",
                "R" : 0,
                "G" : 0,
                "B" : 0,
                "POWER" : ""
}

def rgb_to_hex(R, G, B):
    return '{:02x}{:02x}{:02x}'.format(R, G, B)

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
        led_status["POWER"] = "off"

        with open(led_status["MAC"] + ".json", "w") as f:
            json.dump(led_status, f, indent = 1)

    finally:
        f.close()
        return led_status

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
